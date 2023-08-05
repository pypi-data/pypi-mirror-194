from datetime import datetime
import logging
import os
import random
import time

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException, NoSuchElementException,
    StaleElementReferenceException, TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from mintamazontagger.args import has_order_history_csv_files
from mintamazontagger.my_progress import no_progress_factory
from mintamazontagger.webdriver import (
    get_element_by_id, get_element_by_name, get_element_by_xpath, is_visible)

logger = logging.getLogger(__name__)

# Login and then go to https://www.amazon.com/gp/b2b/reports
ORDER_HISTORY_URL_VIA_SWITCH_ACCOUNT_LOGIN = (
    'https://www.amazon.com/ap/signin'
    '?openid.pape.max_auth_age=0'
    '&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fb2b%2Freports'
    '&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select'
    '&openid.assoc_handle=usflex'
    '&openid.mode=checkid_setup'
    '&switch_account=picker'
    '&ignoreAuthState=1'
    '&language=en_US'
    '&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select'
    '&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0')


class Report:
    def __init__(self, readable_type, type, username, args):
        self.type = type
        self.start_date = args.order_history_start_date
        self.end_date = args.order_history_end_date
        self.readable_type = readable_type
        self.name = (
            f'{username} {self.readable_type} from '
            f'{self.start_date:%d %b %Y} to {self.end_date:%d %b %Y}')
        self.path = os.path.join(
            args.report_download_location, f'{self.name}.csv')
        self.download_link_xpath = (
            f"//td[contains(text(), '{self.name}')]/.."
            "//td/a[contains(text(), 'Download')]")


def maybe_get_webdriver(
        webdriver, args, factory, progress_factory, mfa_input_callback=None):
    if webdriver:
        return webdriver

    if ((not args.amazon_email or not args.amazon_password)
            and not args.amazon_user_will_login):
        logger.error('No credentials provided for Amazon.com')
        return

    login_progress = progress_factory(
        'Signing into Amazon.com to request order reports.', 0)
    webdriver = factory()
    if args.amazon_user_will_login:
        login_success = nav_to_amazon_and_let_user_login(webdriver, args)
    else:
        login_success = nav_to_amazon_and_login(
            webdriver, args, mfa_input_callback)
    login_progress.finish()
    if not login_success:
        logger.critical('Failed to login to Amazon.com')
        return
    logger.info('Login to Amazon.com successful')
    return webdriver


def wait_for_report(webdriver, report, progress_factory, timeout):
    logger.info(f'Waiting for {report.readable_type} report to be ready')
    processing_progress = progress_factory(
        f'Waiting for {report.readable_type} report to be ready.', 0)

    click_refresh_interval_s = 30

    wait_start_time = datetime.now()
    while not get_element_by_xpath(webdriver, report.download_link_xpath):
        since_start = datetime.now() - wait_start_time
        if (since_start.total_seconds() > timeout):
            logger.critical(
                f'Cannot find {report.readable_type}  report download link after {timeout}s')
            processing_progress.finish()
            return False

        try:
            wait_cond = EC.presence_of_element_located(
                (By.XPATH, report.download_link_xpath))
            WebDriverWait(webdriver, click_refresh_interval_s).until(wait_cond)
        except TimeoutException:
            logger.info('Clicking "Refresh Reports" button')
            try:
                refresh_button = get_element_by_id(
                    webdriver, 'report-refresh-button')
                if is_visible(refresh_button):
                    refresh_button.click()
            except StaleElementReferenceException:
                pass
            except ElementClickInterceptedException:
                pass

    processing_progress.finish()
    return True


def fetch_order_history(args, webdriver_factory,
                        progress_factory=no_progress_factory,
                        mfa_input_callback=None):
    # Don't attempt a fetch if CSV files are already in the args.
    if has_order_history_csv_files(args):
        return True

    name = (
        args.amazon_email.split('@')[0]
        if args.amazon_email else 'mint_tagger_unknown_user')

    reports = [
        Report('Items', 'ITEMS', name, args),
        Report('Orders', 'SHIPMENTS', name, args),
        Report('Refunds', 'REFUNDS', name, args),
    ]
    os.makedirs(args.report_download_location, exist_ok=True)

    # Be lazy with getting the driver, as if no fetching is needed, then it's
    # all good.
    webdriver = None
    outstanding_reports = []
    for report in reports:
        if os.path.exists(report.path):
            # Report has already been fetched! Woot
            continue

        # The report is not already downloaded. Log into Amazon (only on the
        # first time).
        webdriver = maybe_get_webdriver(
            webdriver, args, webdriver_factory, progress_factory,
            mfa_input_callback)
        if not webdriver:
            logger.critical('Failed to login to Amazon.com')
            return False

        # Look to see if report is already requested and ready for download.
        if get_element_by_xpath(webdriver, report.download_link_xpath):
            logger.info(f'{report.readable_type} report already generated.')
            download_report(webdriver, report, progress_factory)
            continue

        request_report(webdriver, report, progress_factory)
        outstanding_reports.append(report)

    # Wait on each report to be ready for download.
    for report in outstanding_reports:
        if not wait_for_report(webdriver, report, progress_factory,
                               args.order_history_timeout):
            return False

    # Temporary workaround to avoid an Inspector.detached event.
    time.sleep(1)

    # Download the reports.
    for report in outstanding_reports:
        download_report(webdriver, report, progress_factory)

    args.items_csv = open(reports[0].path, 'r', encoding='utf-8')
    args.orders_csv = open(reports[1].path, 'r', encoding='utf-8')
    args.refunds_csv = open(reports[2].path, 'r', encoding='utf-8')
    return True


def nav_to_amazon_and_let_user_login(webdriver, args):
    logger.info('User logging in to Amazon.com')

    webdriver.get(ORDER_HISTORY_URL_VIA_SWITCH_ACCOUNT_LOGIN)
    try:
        wait_cond = EC.presence_of_element_located((By.ID, 'report-confirm'))
        WebDriverWait(webdriver, args.amazon_login_timeout).until(wait_cond)
    except TimeoutException:
        logger.critical('Cannot complete Amazon login!')
        return False
    return True


# Never attempt to enter the username/password more than 3 times to prevent locking an
# account out due to too many fail attempts. A valid MFA can require reentry
# of the password.
_MAX_LOGIN_ATTEMPTS = 3


def nav_to_amazon_and_login(webdriver, args, mfa_input_callback=None):
    logger.info('Starting automated login flow for Amazon.com')

    webdriver.get(ORDER_HISTORY_URL_VIA_SWITCH_ACCOUNT_LOGIN)
    webdriver.implicitly_wait(0)

    # Amazon login strategy: Work through the flow allowing for any order of
    # interstitials. Exit only when reaching the report page, as detected by
    # finding the element with id 'report-confirm' or if the Logging in to
    # amazon.com timeout has been exceeded.
    #
    # For each attempt section, note that the element must both be present AND
    # visible.
    login_start_time = datetime.now()
    num_login_attempts = 0
    while not get_element_by_id(webdriver, 'report-confirm'):
        since_start = datetime.now() - login_start_time
        if (args.amazon_login_timeout
                and since_start.total_seconds() > args.amazon_login_timeout):
            logger.error('Amazon Login Flow: Exceeded login timeout')
            return False

        if num_login_attempts > _MAX_LOGIN_ATTEMPTS:
            logger.error(
                'Amazon Login Flow: Too many login attempts - aborting.')
            return False

        try:
            if attempt_username_and_password(webdriver, args.amazon_email, args.amazon_password):
                num_login_attempts += 1
            else:
                attempt_otp(webdriver, mfa_input_callback) or attempt_account_switcher_for_email(
                    webdriver, args.amazon_email)
            _login_flow_advance(webdriver)
        except StaleElementReferenceException:
            logger.warning('Amazon Login Flow: '
                           'Page contents changed - trying again.')
        except ElementNotInteractableException:
            logger.warning('Amazon Login Flow: '
                           'Page contents not interactable - trying again.')

    logger.info('Amazon Login Flow: login successful.')
    # If you made it here, you must be good to go!
    return True


def attempt_username(webdriver, email):
    email_input = get_element_by_id(webdriver, 'ap_email')
    if not is_visible(email_input):
        return False
    email_input.clear()
    email_input.send_keys(email)
    logger.info('Amazon Login Flow: Entering email')
    return True


def attempt_password(webdriver, password):
    password_input = get_element_by_id(webdriver, 'ap_password')
    if not is_visible(password_input):
        return False
    password_input.clear()
    password_input.send_keys(password)
    logger.info('Amazon Login Flow: Entering password')
    return True


def attempt_username_and_password(webdriver, username, password):
    if not attempt_username(webdriver, username) and not attempt_password(webdriver, password):
        return False

    remember_me = get_element_by_name(webdriver, 'rememberMe')
    if is_visible(remember_me):
        remember_me.click()
        logger.info('Amazon Login Flow: Clicking Remember Me')

    continue_button = get_element_by_id(webdriver, 'continue')
    if is_visible(continue_button):
        continue_button.click()
        logger.info('Amazon Login Flow: Clicking Continue')
        return True
    # id "auth-signin-button" is a span that sits above input id=signInSubmit.
    auth_signin_button = get_element_by_id(webdriver, 'auth-signin-button')
    if is_visible(auth_signin_button):
        auth_signin_button.click()
        logger.info('Amazon Login Flow: Clicking Auth Sign In')
        return True
    sign_in_submit = get_element_by_id(webdriver, 'signInSubmit')
    if is_visible(sign_in_submit):
        sign_in_submit.click()
        logger.info('Amazon Login Flow: Clicking Sign in')
        return True


def attempt_otp(webdriver, mfa_input_callback):
    otp_code_input = get_element_by_id(webdriver, 'auth-mfa-otpcode')
    otp_continue = get_element_by_id(webdriver, 'auth-signin-button')
    if not is_visible(otp_code_input) or not is_visible(otp_continue):
        return False
    # Check "Don't require OTP on this browser"
    remember_me_otp = get_element_by_xpath(
        webdriver,
        '//span[contains(text(), '
        '"Don\'t require OTP on this browser")]')
    if is_visible(remember_me_otp):
        remember_me_otp.click()

    mfa_code = (mfa_input_callback or input)(
        'Please enter your 6-digit Amazon OTP code: ')
    otp_code_input.send_keys(mfa_code)
    otp_continue.click()
    return True


def attempt_account_switcher_for_email(webdriver, email):
    # Account switcher: look for the given email. If present, click on
    # it!
    account_switcher_choice = get_element_by_xpath(
        webdriver,
        f"//div[contains(text(), '{email}')]")
    if is_visible(account_switcher_choice):
        logger.info(
            'Amazon Login Flow: Found email in account switcher')
        account_switcher_choice.click()
        return True

    # Account switcher: Cannot find the desired account in the account
    # switcher. Click "Add Account".
    account_switcher_add_account = get_element_by_xpath(
        webdriver, '//div[text()="Add account"]')
    if is_visible(account_switcher_add_account):
        logger.info(
            'Amazon Login Flow: '
            'Email not in account switcher - Pressing "Add account"')
        account_switcher_add_account.click()
        return True
    return False


def _login_flow_advance(webdriver):
    time.sleep(random.randint(500, 1500) / 1000)


def request_report(webdriver, report, progress_factory):
    logger.info(f'Requesting {report.readable_type} report')
    request_progress = progress_factory(
        f'Requesting {report.readable_type} report ', 0)

    Select(get_element_by_id(webdriver, 'report-type-native')
           ).select_by_value(report.type)

    get_element_by_xpath(
        webdriver,
        '//*[@id="startDateCalendar"]/div[2]/div/div/div/input'
    ).send_keys(report.start_date.strftime('%m/%d/%Y'))
    get_element_by_xpath(
        webdriver,
        '//*[@id="endDateCalendar"]/div[2]/div/div/div/input'
    ).send_keys(report.end_date.strftime('%m/%d/%Y'))

    get_element_by_id(webdriver, 'report-name').send_keys(report.name)

    # Submit will not work as the input type is an image (nice Amazon)
    get_element_by_id(webdriver, 'report-confirm').click()
    request_progress.finish()


def download_report(webdriver, report, progress_factory):
    logger.info(f'Downloading {report.readable_type} report')
    download_progress = progress_factory(
        f'Downloading {report.readable_type} report', 0)
    # 1. Find the report download link
    report_url = None
    try:
        download_link = get_element_by_xpath(
            webdriver,
            report.download_link_xpath)
        report_url = download_link.get_attribute('href')
    except NoSuchElementException:
        logger.critical('Could not find the download link!')
        exit(1)

    # 2. Download the report to the AMZN Reports directory
    response = webdriver.request('GET', report_url, allow_redirects=True)
    response.raise_for_status()
    with open(report.path, 'w', encoding='utf-8') as fh:
        fh.write(response.text)
    download_progress.finish()
