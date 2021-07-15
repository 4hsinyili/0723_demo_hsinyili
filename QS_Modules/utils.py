from selenium import webdriver
import os


class Chrome():
    def __init__(self,
                 driver_path='lambda',
                 headless=False,
                 auto_close=False,
                 inspect=False):
        self.driver = self.chrome_create(driver_path, headless, auto_close,
                                         inspect)

    def chrome_create(self, driver_path, headless, auto_close, inspect):
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
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
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

            # chrome_options.add_argument('--disable-gpu')
            for argument in lambda_options:
                options.add_argument(argument)

            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--disable-blink-features=AutomationControlled")
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
            options.add_argument(f'user-agent={user_agent}')
            driver = webdriver.Chrome(
                chrome_options=options)
            driver.implicitly_wait(8)
            return driver

    def chrome_end(self, driver):
        driver.quit()
