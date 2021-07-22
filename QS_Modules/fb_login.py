from QS_Modules import env
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import json

DRIVER_PATH = env.DRIVER_PATH


def create_driver(headless=False):
    chrome_options = webdriver.ChromeOptions()
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_experimental_option(
        'prefs', {'intl.accept_languages': 'en,en_US'})
    chrome_options.add_experimental_option("excludeSwitches",
                                           ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled")
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(DRIVER_PATH, options=chrome_options)
    driver.delete_all_cookies()
    driver.implicitly_wait(2)
    return driver


def sele_login(driver):
    driver.get('https://www.messenger.com/t/100001752617744')
    driver.find_element_by_id('email').send_keys('log4hsinyili@gmail.com')
    driver.find_element_by_id('pass').send_keys('fbtest4hsinyili')
    driver.find_element_by_xpath(
        '//input[@name="persistent"]/following-sibling::span[1]').click()
    time.sleep(1)
    driver.find_element_by_id('loginbutton').send_keys(Keys.ENTER)
    time.sleep(2)

    for request in driver.requests:
        if request.url.startswith('https://www.facebook.com/login/'):
            request_header = request.headers
            headers = request_header
            print(headers)
            print('--')
            params = request.params
            print(params)
            print('++')

    return headers, params


def sele_send_text(driver, text):
    actions = ActionChains(driver)
    actions.send_keys(text)
    actions.send_keys(Keys.ENTER)
    actions.perform()

    for request in driver.requests:
        if request.url.startswith('wss://edge-chat.messenger.com/chat'):
            request_header = request.headers
            headers = request_header
            print(headers)
            print('--')
            params = request.params
            print(params)
            print('++')

    return headers, params


class HTTPFB():
    def __init__(self, headers, email, pwd, msg, thread_id):
        self.headers = headers
        self.session = requests.session()
        self.email = email
        self.pwd = pwd
        self.msg = msg
        self.thread_id = str(thread_id)

    def get_token(self):
        session = self.session
        co = session.get('https://www.messenger.com').text
        lsd_token = co.split('LSD')[1].split('"token":"')[1].split('"')[0]
        initreqid = co.split('initialRequestID":"', 1)[1].split('"', 1)[0]
        timezone = -480
        lgnrnd = co.split('name="lgnrnd" value="', 1)[1].split('"', 1)[0]
        lgnjs = int(time.time())
        identifier = co.split('identifier":"', 1)[1].split('"', 1)[0]
        datr = co.split('"_js_datr","', 1)[1].split('"', 1)[0]
        session.cookies.update({'_js_datr': datr})

        self.initreqid = initreqid
        self.identifier = identifier
        self.messenger_com_data = {
            'lsd': lsd_token,
            'initial_request_id': initreqid,
            'timezone': timezone,
            'lgnrnd': lgnrnd,
            'lgnjs': lgnjs,
        }

    def login(self):
        session = self.session
        r = session.get(
            'https://www.facebook.com/login/messenger_dot_com_iframe/',
            params={
                'redirect_uri':
                'https://www.messenger.com/login/fb_iframe_target/?initial_request_id={}'
                .format(self.initreqid),
                'identifier':
                self.identifier,
                'initial_request_id':
                self.initreqid
            })

        login_params = self.messenger_com_data
        login_params['email'] = self.email
        login_params['pass'] = self.pwd
        login_params['default_persistent'] = 0

        r = session.post('https://www.messenger.com/login/password/',
                         login_params,
                         headers=self.headers)
        data = r.text
        return data

    def parse_data(self, data):
        thread_id = self.thread_id
        msg = self.msg
        dtsg_token = data.split('"token":"', 1)[1].split('"', 1)[0]
        ttstamp = '2'
        for w in range(len(dtsg_token)):
            ttstamp += str(ord(dtsg_token[w]))

        rev = data.split('revision":', 1)[1].split(',', 1)[0]
        uid = data.split('USER_ID":"', 1)[1].split('"', 1)[0]

        _id = random.randint(0, 999999999999999999)
        data = {
            'action_type': 'ma-type:user-generated-message',
            'author': 'fbid:' + uid,
            'source': 'source:messenger:web',
            'body': msg,
            'has_attachment': 'false',
            'html_body': 'false',
            'timestamp': int(time.time() * 1000),
            'offline_threading_id': _id,
            'message_id': _id,
            'client': 'mercury',
            'fb_dtsg': dtsg_token,
            'ttstamp': ttstamp,
            'specific_to_list[0]': 'fbid:' + thread_id,
            'specific_to_list[1]': 'fbid:' + uid,
            'other_user_fbid': thread_id
        }
        return data, uid, rev

    # def str_base(self,
    #              num,
    #              b=36,
    #              numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    #     return ((num == 0) and numerals[0]) or (self.str_base(
    #         num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

    def send_req(self, data, uid, rev):
        session = self.session
        defurl = 'https://www.messenger.com'
        endpoint = 'https://www.messenger.com/messaging/send/'
        defdata = {
            '__user': uid,
            '__a': 1,
            '__req': '0',
            '__rev': rev
        }
        data.update(defdata)
        resp = session.post(endpoint, data, headers={'Referer': defurl})
        return resp

    def main(self):
        self.get_token()
        data = self.login()
        data, uid, rev = self.parse_data(data)
        response = self.send_req(data, uid, rev)
        print(response)


headers = {
    "Content-Length": "467",
    "User-Agent":
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "*/*",
    "Origin": "https://www.messenger.com",
    "Referer": "https://www.messenger.com/",
}

if __name__ == '__main__':
    QSEARCH_THREAD = 430401096982804
    thread_id = 100070719168616
    # thread_id = QSEARCH_THREAD
    msg = '測試0721'
    http_fb = HTTPFB(headers, FB_TEST_EMAIL, FB_TEST_PWD, msg, thread_id)
    http_fb.main()
