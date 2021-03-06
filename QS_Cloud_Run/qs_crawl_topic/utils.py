from datetime import datetime
import time


def output_dt_str(dt_obj):
    dt_str = datetime.strftime(dt_obj, '%Y-%m-%d-%H:%M:%S')
    return dt_str


def parse_dt_str(dt_str):
    dt_obj = datetime.strptime(dt_str, '%Y-%m-%d-%H:%M:%S')
    return dt_obj


def login_mobile01(driver, account, pwd):
    from selenium.webdriver.common.keys import Keys

    url = 'https://www.mobile01.com/login.php'

    driver.get(url)
    driver.find_element_by_xpath('//input[@id="regEmail"]').send_keys(account)
    driver.find_element_by_xpath('//input[@id="regPassword"]').send_keys(pwd)
    driver.find_element_by_xpath('//input[@id="remember_me"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//button[@id="submitBtn"]').send_keys(Keys.ENTER)
    time.sleep(2)
    try:
        driver.find_element_by_xpath('//a[contains(.,"確認")]').send_keys(Keys.ENTER)
    except Exception:
        pass


class Chrome():
    def __init__(self,
                 driver_path='lambda',
                 headless=False,
                 auto_close=False,
                 inspect=False):
        self.driver = self.chrome_create(driver_path, headless, auto_close,
                                         inspect)

    def chrome_create(self, driver_path, headless, auto_close, inspect):
        from selenium import webdriver
        if driver_path != 'lambda':
            chrome_options = webdriver.ChromeOptions()
            if headless:
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--window-size=1920,1080")
                chrome_options.add_argument("--start-maximized")
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--ignore-certificate-errors')
            if not auto_close:
                chrome_options.add_experimental_option("detach", True)
            if inspect:
                chrome_options.add_argument("--auto-open-devtools-for-tabs")
            chrome_options.add_experimental_option(
                'prefs', {'intl.accept_languages': 'en,en_US'})
            chrome_options.add_experimental_option("excludeSwitches",
                                                   ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension',
                                                   False)
            chrome_options.add_argument(
                "--disable-blink-features=AutomationControlled")
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
            chrome_options.add_argument(f'user-agent={user_agent}')
            driver = webdriver.Chrome(driver_path, options=chrome_options)
            driver.delete_all_cookies()
            driver.implicitly_wait(2)
            return driver
        else:
            options = webdriver.ChromeOptions()
            lambda_options = [
                '--autoplay-policy=user-gesture-required',
                '--disable-background-networking',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-breakpad',
                '--disable-client-side-phishing-detection',
                '--disable-component-update', '--disable-default-apps',
                '--disable-dev-shm-usage', '--disable-domain-reliability',
                '--disable-extensions',
                '--disable-features=AudioServiceOutOfProcess',
                '--disable-hang-monitor', '--disable-ipc-flooding-protection',
                '--disable-notifications',
                '--disable-offer-store-unmasked-wallet-cards',
                '--disable-popup-blocking', '--disable-print-preview',
                '--disable-prompt-on-repost',
                '--disable-renderer-backgrounding', '--disable-setuid-sandbox',
                '--disable-speech-api', '--disable-sync',
                '--disk-cache-size=33554432', '--hide-scrollbars',
                '--ignore-gpu-blacklist', '--ignore-certificate-errors',
                '--metrics-recording-only', '--mute-audio',
                '--no-default-browser-check', '--no-first-run', '--no-pings',
                '--no-sandbox', '--no-zygote', '--password-store=basic',
                '--use-gl=swiftshader', '--use-mock-keychain',
                '--single-process', '--headless'
            ]

            for argument in lambda_options:
                options.add_argument(argument)
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument(
                "--disable-blink-features=AutomationControlled")
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
            options.add_argument(f'user-agent={user_agent}')
            driver = webdriver.Chrome(chrome_options=options)
            driver.implicitly_wait(8)
            return driver

    def chrome_end(self, driver):
        driver.quit()
