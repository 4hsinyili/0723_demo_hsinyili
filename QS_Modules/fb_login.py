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


def str_base(num, b=36, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and numerals[0]) or (str_base(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])


headers = {
    "Content-Length": "467",
    "User-Agent":
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "*/*",
    "Origin": "https://www.messenger.com",
    "Referer": "https://www.messenger.com/",
}

email = 'bnxmhpbgmb_1626509584@tfbnw.net'
pwd = "fbtest1626509584"
email = 'yidon62086@godpeed.com'
pwd = 'fbtest0718'
qsearch_thread = 430401096982804


session = requests.session()

co = session.get('https://www.messenger.com').text
lsd_token = co.split('LSD')[1].split('"token":"')[1].split('"')[0]
initreqid = co.split('initialRequestID":"', 1)[1].split('"', 1)[0]
timezone = -480
lgnrnd = co.split('name="lgnrnd" value="', 1)[1].split('"', 1)[0]
lgnjs = int(time.time())
identifier = co.split('identifier":"', 1)[1].split('"', 1)[0]
datr = co.split('"_js_datr","', 1)[1].split('"', 1)[0]
session.cookies.update({'_js_datr': datr})

session.get(
    'https://www.facebook.com/login/messenger_dot_com_iframe/',
    params={
        'redirect_uri':
        'https://www.messenger.com/login/fb_iframe_target/?initial_request_id={}'
        .format(initreqid),
        'identifier':
        identifier,
        'initial_request_id':
        initreqid
    })

r = session.post('https://www.messenger.com/login/password/', {
    'lsd': lsd_token,
    'initial_request_id': initreqid,
    'timezone': timezone,
    'lgnrnd': lgnrnd,
    'lgnjs': lgnjs,
    'email': email,
    'pass': pwd,
    'default_persistent': 0
},
                 headers=headers)

print(r)
print(r.url)

data = r.text

dtsg_token = data.split('"token":"', 1)[1].split('"', 1)[0]
ttstamp = '2'
for w in range(len(dtsg_token)):
    ttstamp += str(ord(dtsg_token[w]))
reqid = 0
uploadid = 1023
sessid = str_base(random.randint(0, 2147483647), 16)

rev = data.split('revision":', 1)[1].split(',', 1)[0]
uid = data.split('USER_ID":"', 1)[1].split('"', 1)[0]

# thread_id = 100070719168616
thread_id = qsearch_thread

msg = '測試'

thread_id = str(thread_id)
msg = str(msg)

_id = random.randint(0, 999999999999999999)
data = {'action_type': 'ma-type:user-generated-message',
        'author': 'fbid:' + uid,
        'source': 'source:messenger:web',
        'body': msg,
        'has_attachment': 'false',
        'html_body': 'false',
        'timestamp': int(time.time() * 1000),
        'offline_threading_id': _id,
        'message_id': _id,
        'client': 'mercury', 'fb_dtsg': dtsg_token, 'ttstamp': ttstamp}
userdata = {'specific_to_list[0]': 'fbid:' + thread_id,
            'specific_to_list[1]': 'fbid:' + uid,
            'other_user_fbid': thread_id}
data.update(userdata)
reqid = 0


def send_req(url, reqtype, data, sess):
    defurl = 'https://www.messenger.com'
    defdata = {'__user': uid, '__a': 1, '__req': str_base(0), '__rev': rev}
    data.update(defdata)

    if reqtype:
        resp = sess.post(defurl + url, data, headers={'Referer': defurl})
    else:
        resp = sess.get(defurl + url, params=data, headers={'Referer': defurl})

    return resp


req = send_req('/messaging/send/', 1, data, session)
print(req)
result = json.loads(req.text[9:])['payload']
print(result)


# Reference
# https://www.gushiciku.cn/dc_tw/352818
# https://stephensclafani.com/2017/03/21/stealing-messenger-com-login-nonces/