from collections import defaultdict
from copy import deepcopy
import csv
from datetime import datetime, date
import os
from pprint import pformat
import re
import string
import time

from mintamazontagger.algorithm_u import algorithm_u
from mintamazontagger import category
from mintamazontagger.currency import float_usd_to_micro_usd
from mintamazontagger.currency import micro_usd_nearly_equal
from mintamazontagger.currency import micro_usd_to_usd_string
from mintamazontagger.currency import parse_usd_as_micro_usd
from mintamazontagger.currency import CENT_MICRO_USD, MICRO_USD_EPS
from mintamazontagger.mint import truncate_title
from mintamazontagger.my_progress import NoProgress, no_progress_factory

PRINTABLE = set(string.printable)


def rm_leading_qty(item_title):
    """Removes the '2x Item Name' from the front of an item title."""
    return re.sub(r'^\d+x ', '', item_title)


def get_title(amzn_obj, target_length):
    # Also works for a Refund record.
    qty = amzn_obj.quantity
    base_str = None
    if qty > 1:
        base_str = str(qty) + 'x'
    # Remove non-ASCII characters from the title.
    clean_title = ''.join(filter(lambda x: x in PRINTABLE, amzn_obj.title))
    return truncate_title(clean_title, target_length, base_str)


CURRENCY_FIELD_NAMES = set([
    'Item Subtotal',
    'Item Subtotal Tax',
    'Item Total',
    'List Price Per Unit',
    'Purchase Price Per Unit',
    'Refund Amount',
    'Refund Tax Amount',
    'Shipping Charge',
    'Subtotal',
    'Tax Charged',
    'Tax Before Promotions',
    'Total Charged',
    'Total Promotions',
])

DATE_FIELD_NAMES = set([
    'Order Date',
    'Refund Date',
    'Shipment Date',
])

RENAME_FIELD_NAMES = {
    'Carrier Name & Tracking Number': 'tracking',
}


def num_lines_csv(csv_file):
    return sum([1 for r in csv.DictReader(
        open(csv_file.name, encoding='utf-8'))])


def is_empty_csv(csv_file, num_records, key='Buyer Name'):
    # Amazon likes to put "No data found for this time period" in the first
    # row.
    # Amazon appears to be giving 0 sized CSVs now!
    if os.stat(csv_file.name).st_size == 0:
        return True
    return (num_records <= 1 and next(csv.DictReader(
        open(csv_file.name, encoding='utf-8')))[key] is None)


def parse_from_csv_common(
        cls,
        csv_file,
        progress_label='Parse from csv',
        progress_factory=no_progress_factory):
    num_records = num_lines_csv(csv_file)
    if is_empty_csv(csv_file, num_records):
        return []

    progress = progress_factory(progress_label, num_records)
    reader = csv.DictReader(csv_file)
    result = []
    for raw_dict in reader:
        result.append(cls(raw_dict))
        progress.next()
    progress.finish()
    return result


def pythonify_amazon_dict(raw_dict):
    keys = set(raw_dict.keys())

    # Convert to microdollar ints
    for ck in keys & CURRENCY_FIELD_NAMES:
        raw_dict[ck] = parse_usd_as_micro_usd(raw_dict[ck])

    # Convert to datetime.date
    for dk in keys & DATE_FIELD_NAMES:
        raw_dict[dk] = parse_amazon_date(raw_dict[dk])

    # Rename long or unpythonic names:
    for old_key in keys & RENAME_FIELD_NAMES.keys():
        new_key = RENAME_FIELD_NAMES[old_key]
        raw_dict[new_key] = raw_dict[old_key]
        del raw_dict[old_key]

    if 'Quantity' in keys:
        raw_dict['Quantity'] = int(raw_dict['Quantity'])

    if 'Shipping Charge' in keys:
        raw_dict['Original Shipping Charge'] = raw_dict['Shipping Charge']

    return dict([
        (k.lower().replace(' ', '_').replace('/', '_'), v)
        for k, v in raw_dict.items()
    ])


def parse_amazon_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%m/%d/%Y').date()
    except ValueError:
        return datetime.strptime(date_str, '%m/%d/%y').date()


def get_invoice_url(order_id):
    return (
        'https://www.amazon.com/gp/css/summary/print.html?ie=UTF8&'
        f'orderID={order_id}')


def associate_items_with_orders(
        all_orders, all_items, item_progress=NoProgress()):
    items_by_oid = defaultdict(list)
    for i in all_items:
        items_by_oid[i.order_id].append(i)
    orders_by_oid = defaultdict(list)
    for o in all_orders:
        orders_by_oid[o.order_id].append(o)

    for oid, orders in orders_by_oid.items():
        oid_items = items_by_oid[oid]

        if not micro_usd_nearly_equal(
                Order.sum_subtotals(orders),
                Item.sum_subtotals(oid_items)):
            # This is likely due to reports being pulled before all outstanding
            # orders have shipped. Just skip this order for now.
            continue

        if len(orders) == 1:
            orders[0].set_items(oid_items, assert_unmatched=True)
            item_progress.next(len(oid_items))
            continue

        # First try to divy up the items by tracking.
        items_by_tracking = defaultdict(list)
        for i in oid_items:
            items_by_tracking[i.tracking].append(i)

        # It is never the case that multiple orders with the same order id will
        # have the same tracking number. Try using tracking number to split up
        # the items between the orders.
        for order in orders:
            items = items_by_tracking[order.tracking]
            if micro_usd_nearly_equal(
                    Item.sum_subtotals(items),
                    order.subtotal):
                # A perfect fit.
                order.set_items(items, assert_unmatched=True)
                item_progress.next(len(items))
                # Remove the selected items.
                oid_items = [i for i in oid_items if i not in items]
        # Remove orders that have items.
        orders = [o for o in orders if not o.items]
        if not orders and not oid_items:
            continue

        orders = sorted(orders, key=lambda o: o.subtotal)

        # Partition the remaining items into every possible arrangement and
        # validate against the remaining orders.
        # TODO: Make a custom algorithm with backtracking.

        # The number of combinations are factorial, so limit the number of
        # attempts (by a 1 sec timeout) before giving up.
        # Also catch any recursion depth exceptions.
        try:
            start_time = time.time()
            for item_groupings in algorithm_u(oid_items, len(orders)):
                if time.time() - start_time > 1:
                    break
                subtotals_with_groupings = sorted(
                    [(Item.sum_subtotals(itms), itms)
                     for itms in item_groupings],
                    key=lambda g: g[0])
                if all([micro_usd_nearly_equal(
                        subtotals_with_groupings[i][0],
                        orders[i].subtotal) for i in range(len(orders))]):
                    for idx, order in enumerate(orders):
                        items = subtotals_with_groupings[idx][1]
                        order.set_items(items,
                                        assert_unmatched=True)
                        item_progress.next(len(items))
                    break
        except RecursionError:
            break
    item_progress.finish()


ORDER_MERGE_FIELDS = {
    'original_shipping_charge',
    'shipping_charge',
    'subtotal',
    'tax_before_promotions',
    'tax_charged',
    'total_charged',
    'total_promotions',
}


class Order:
    is_refund = False
    matched = False
    items_matched = False
    trans_id = None
    items = []

    def __init__(self, raw_dict):
        self.__dict__.update(pythonify_amazon_dict(raw_dict))
        if self.has_hidden_shipping_fee():
            self.shipping_charge += self.hidden_shipping_fee()
            self.total_charged += self.hidden_shipping_fee()

    @classmethod
    def parse_from_csv(cls, csv_file, progress_factory=no_progress_factory):
        return parse_from_csv_common(
            cls, csv_file, 'Parsing Amazon Orders', progress_factory)

    @staticmethod
    def sum_subtotals(orders):
        return sum([o.subtotal for o in orders])

    def has_hidden_shipping_fee(self):
        # Colorado - https://tax.colorado.gov/retail-delivery-fee
        # "Effective July 1, 2022, Colorado imposes a retail delivery fee on
        # all deliveries by motor vehicle to a location in Colorado with at
        # least one item of tangible personal property subject to state sales
        # or use tax."
        # Rate July 2022 to June 2023: $0.27
        # This is not the case as of 8/31/2022 for Amazon Order Reports.
        # "Retailers that make retail deliveries must show the total of the
        # fees on the receipt or invoice as one item called “retail delivery
        # fees”."
        return (
            self.shipping_address_state == 'CO'
            and self.tax_charged > 0
            and self.shipment_date >= date(2022, 7, 1))

    def hidden_shipping_fee(self):
        return float_usd_to_micro_usd(0.27)

    def hidden_shipping_fee_note(self):
        return 'CO Retail Delivery Fee'

    def total_by_items(self):
        return (
            Item.sum_totals(self.items)
            + self.shipping_charge - self.total_promotions)

    def total_by_subtotals(self):
        return (
            self.subtotal + self.tax_charged
            + self.shipping_charge - self.total_promotions)

    def transact_date(self):
        return self.shipment_date

    def transact_amount(self):
        return -self.total_charged

    def match(self, trans):
        self.matched = True
        self.trans_id = trans.id

    def set_items(self, items, assert_unmatched=False):
        self.items = items
        self.items_matched = True
        for i in items:
            if assert_unmatched:
                assert not i.matched
            i.matched = True
            i.order = self

    def get_notes(self):
        return (
            f'Amazon order id: {self.order_id}\n'
            f'Buyer: {self.buyer_name} ({self.ordering_customer_email})\n'
            f'Order date: {self.order_date}\n'
            f'Ship date: {self.shipment_date}\n'
            f'Tracking: {self.tracking}\n'
            f'Invoice url: {get_invoice_url(self.order_id)}')

    def attribute_subtotal_diff_to_misc_charge(self):
        diff = self.total_charged - self.total_by_subtotals()
        if diff < MICRO_USD_EPS:
            return False

        self.subtotal += diff

        adjustment = deepcopy(self.items[0])
        adjustment.title = 'Misc Charge (Gift wrap, etc)'
        adjustment.category = 'Shopping'
        adjustment.quantity = 1
        adjustment.item_total = diff
        adjustment.item_subtotal = diff
        adjustment.item_subtotal_tax = 0

        self.items.append(adjustment)
        return True

    def attribute_itemized_diff_to_shipping_tax(self):
        # Shipping [sometimes] has tax. Include this in the shipping charge.
        # Unfortunately Amazon doesn't provide this anywhere; it must be
        # inferred as of now.
        if not self.shipping_charge:
            return False

        diff = self.total_charged - self.total_by_items()
        if diff < MICRO_USD_EPS:
            return False

        self.shipping_charge += diff

        self.tax_charged -= diff
        self.tax_before_promotions -= diff

        return True

    def attribute_itemized_diff_to_per_item_tax(self):
        itemized_diff = self.total_charged - self.total_by_items()
        if abs(itemized_diff) < MICRO_USD_EPS:
            return False

        tax_diff = self.tax_charged - Item.sum_subtotals_tax(self.items)
        if abs(itemized_diff - tax_diff) > MICRO_USD_EPS:
            return False

        # The per-item tax was not computed correctly; the tax miscalculation
        # matches the itemized difference. Sometimes AMZN is bad at math (lol),
        # and most of the time it's simply a rounding error. To keep the line
        # items adding up correctly, spread the tax difference across the
        # items.
        tax_rate_per_item = [i.tax_rate() for i in self.items]
        while abs(tax_diff) > MICRO_USD_EPS:
            if abs(tax_diff) < CENT_MICRO_USD:
                # If the difference is under a penny, round that
                # partial cent to the first item.
                adjust_amount = tax_diff
                adjust_idx = 0
            elif tax_diff > 0:
                # The order has more tax than the sum of all items.
                # Find the lowest taxed item (by rate) and add a penny. Try to
                # ignore items that have no tax (a rate of zero) however
                # default to the first item if no items were taxed.
                adjust_amount = CENT_MICRO_USD
                adjust_idx = 0
                min_rate = None
                for (idx, rate) in enumerate(tax_rate_per_item):
                    if rate != 0 and (not min_rate or rate < min_rate):
                        adjust_idx = idx
                        min_rate = rate
            else:
                # The order has less tax than the sum of all items.
                # Find the highest taxed item (by rate) and discount it
                # a penny.
                (adjust_idx, _) = max(
                    enumerate(tax_rate_per_item), key=lambda x: x[1])
                adjust_amount = -CENT_MICRO_USD

            adjust_item = self.items[adjust_idx]
            adjust_item.item_subtotal_tax += adjust_amount
            adjust_item.item_total += adjust_amount
            tax_diff -= adjust_amount
            tax_rate_per_item[adjust_idx] = adjust_item.tax_rate()
        return True

    def to_mint_transactions(self,
                             t,
                             skip_free_shipping=False):
        new_transactions = []

        # More expensive items are always more interesting when it comes to
        # budgeting, so show those first (for both itemized and concatted).
        items = sorted(
            self.items, key=lambda item: item.item_total, reverse=True)

        # Itemize line-items:
        for i in items:
            new_cat = category.get_mint_category_from_unspsc(i.unspsc_code)
            item = t.split(
                amount=-i.item_total,
                category_name=new_cat,
                description=i.get_title(88),
                notes=self.get_notes())
            new_transactions.append(item)

        if self.has_hidden_shipping_fee():
            ship_fee = t.split(
                amount=-self.hidden_shipping_fee(),
                category_name='Shipping',
                description=self.hidden_shipping_fee_note(),
                notes=self.get_notes())
            new_transactions.append(ship_fee)

        # Itemize the shipping cost, if any.
        is_free_shipping = (
            self.original_shipping_charge
            and self.total_promotions
            and micro_usd_nearly_equal(
                self.total_promotions, self.original_shipping_charge))

        if is_free_shipping and skip_free_shipping:
            return new_transactions

        if self.original_shipping_charge:
            ship = t.split(
                amount=-self.original_shipping_charge,
                category_name='Shipping',
                description='Shipping',
                notes=self.get_notes())
            new_transactions.append(ship)

        # All promotion(s) as one line-item.
        if self.total_promotions:
            # If there was a promo that matches the shipping cost, it's nearly
            # certainly a Free One-day/same-day/etc promo. In this case,
            # categorize the promo instead as 'Shipping', which will cancel out
            # in Mint trends.
            cat = ('Shipping' if is_free_shipping else
                   category.DEFAULT_MINT_CATEGORY)
            promo = t.split(
                amount=self.total_promotions,
                category_name=cat,
                description='Promotion(s)',
                notes=self.get_notes())
            new_transactions.append(promo)

        return new_transactions

    @classmethod
    def merge(cls, orders):
        if len(orders) == 1:
            result = orders[0]
            result.set_items(Item.merge(result.items))
            return result

        result = deepcopy(orders[0])
        result.set_items(Item.merge([i for o in orders for i in o.items]))
        for key in ORDER_MERGE_FIELDS:
            result.__dict__[key] = sum([o.__dict__[key] for o in orders])
        return result

    def __repr__(self):
        return (
            f'Order ({self.order_id}): {self.shipment_date or self.order_date}'
            f' Total {micro_usd_to_usd_string(self.total_charged)}\t'
            f'Subtotal {micro_usd_to_usd_string(self.subtotal)}\t'
            f'Tax {micro_usd_to_usd_string(self.tax_charged)}\t'
            f'Promo {micro_usd_to_usd_string(self.total_promotions)}\t'
            f'Ship {micro_usd_to_usd_string(self.shipping_charge)}\t'
            f'Items: \n{pformat(self.items)}')


class Item:
    matched = False
    order = None

    def __init__(self, raw_dict):
        self.__dict__.update(pythonify_amazon_dict(raw_dict))
        self.__dict__['original_item_subtotal_tax'] = self.item_subtotal_tax

    @classmethod
    def parse_from_csv(cls, csv_file, progress_factory=no_progress_factory):
        return parse_from_csv_common(
            cls, csv_file, 'Parsing Amazon Items', progress_factory)

    @staticmethod
    def sum_subtotals(items):
        return sum([i.item_subtotal for i in items])

    @staticmethod
    def sum_totals(items):
        return sum([i.item_total for i in items])

    @staticmethod
    def sum_subtotals_tax(items):
        return sum([i.item_subtotal_tax for i in items])

    def tax_rate(self):
        return round(self.item_subtotal_tax * 100.0 / self.item_subtotal, 1)

    def get_title(self, target_length=100):
        return get_title(self, target_length)

    def is_cancelled(self):
        return self.order_status == 'Cancelled'

    def set_quantity(self, new_quantity):
        """Sets the quantity of this item and updates all prices."""
        original_quantity = self.quantity

        assert new_quantity > 0
        subtotal_equal = micro_usd_nearly_equal(
            self.purchase_price_per_unit * original_quantity,
            self.item_subtotal)
        assert subtotal_equal < MICRO_USD_EPS

        self.item_subtotal = self.purchase_price_per_unit * new_quantity
        self.item_subtotal_tax = (
            self.item_subtotal_tax / original_quantity) * new_quantity
        self.item_total = self.item_subtotal + self.item_subtotal_tax
        self.quantity = new_quantity

    def split_by_quantity(self):
        """Splits this item into 'quantity' items."""
        if self.quantity == 1:
            return [self]
        orig_qty = self.quantity
        self.set_quantity(1)
        return [deepcopy(self) for i in range(orig_qty)]

    @classmethod
    def merge(cls, items):
        """Collapses identical items by using quantity."""
        if len(items) < 2:
            return items
        unique_items = defaultdict(list)
        for i in items:
            key = f'{i.title}-{i.asin_isbn}-{i.item_subtotal}'
            unique_items[key].append(i)
        results = []
        for same_items in unique_items.values():
            qty = sum([i.quantity for i in same_items])
            if qty == 1:
                results.extend(same_items)
                continue

            item = deepcopy(same_items[0])
            item.set_quantity(qty)
            results.append(item)
        return results

    def __repr__(self):
        return (
            f'{self.quantity} of Item: '
            f'Total {micro_usd_to_usd_string(self.item_total)}\t'
            f'Subtotal {micro_usd_to_usd_string(self.item_subtotal)}\t'
            f'Tax {micro_usd_to_usd_string(self.item_subtotal_tax)} '
            f'{self.title}')


class Refund:
    matched = False
    trans_id = None
    is_refund = True

    def __init__(self, raw_dict):
        # Refunds are rad: AMZN doesn't total the tax + sub-total for you.
        fields = pythonify_amazon_dict(raw_dict)
        fields['total_refund_amount'] = (
            fields['refund_amount'] + fields['refund_tax_amount'])
        self.__dict__.update(fields)

    @staticmethod
    def sum_total_refunds(refunds):
        return sum([r.total_refund_amount for r in refunds])

    @classmethod
    def parse_from_csv(cls, csv_file, progress_factory=no_progress_factory):
        return parse_from_csv_common(
            cls, csv_file, 'Parsing Amazon Refunds', progress_factory)

    def match(self, trans):
        self.matched = True
        self.trans_id = trans.id

    def transact_date(self):
        return self.refund_date

    def transact_amount(self):
        return self.total_refund_amount

    def get_title(self, target_length=100):
        return get_title(self, target_length)

    def get_notes(self):
        return (
            f'Amazon refund for order id: {self.order_id}\n'
            f'Buyer: {self.buyer_name}\n'
            f'Order date: {self.order_date}\n'
            f'Refund date: {self.refund_date}\n'
            f'Refund reason: {self.refund_reason}\n'
            f'Invoice url: {get_invoice_url(self.order_id)}')

    def to_mint_transaction(self, t):
        # Refunds have a positive amount.
        result = t.split(
            description=self.get_title(88),
            category_name=category.DEFAULT_MINT_RETURN_CATEGORY,
            amount=self.total_refund_amount,
            notes=self.get_notes())
        return result

    @staticmethod
    def merge(refunds):
        """Collapses identical items by using quantity."""
        if len(refunds) <= 1:
            return refunds
        unique_refund_items = defaultdict(list)
        for r in refunds:
            key = (
                f'{r.refund_date}-{r.refund_reason}-{r.title}-'
                f'{r.total_refund_amount}-{r.asin_isbn}')
            unique_refund_items[key].append(r)
        results = []
        for same_items in unique_refund_items.values():
            qty = sum([i.quantity for i in same_items])
            if qty == 1:
                results.extend(same_items)
                continue

            refund = same_items[0]
            refund.quantity = qty
            refund.total_refund_amount *= qty
            refund.refund_amount *= qty
            refund.refund_tax_amount *= qty

            results.append(refund)
        return results

    def __repr__(self):
        return (
            f'{self.quantity} of Refund: '
            f'Total {micro_usd_to_usd_string(self.total_refund_amount)}\t'
            f'Subtotal {micro_usd_to_usd_string(self.refund_amount)}\t'
            f'Tax {micro_usd_to_usd_string(self.refund_tax_amount)} '
            f'{self.title}')
