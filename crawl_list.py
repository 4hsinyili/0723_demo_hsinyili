# avoid import error on lambda get_ue_detail
try:
    # for crawling from js-website
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By

    # for html parsing
    from lxml import etree
except Exception:
    pass

# for crawling from API
import requests

# for file handling
import os
import json


# for timing and not to get caught
import time
import random
from datetime import datetime

# for preview
import pprint

import requests

LIST_URL = 'https://www.mobile01.com/newtopics.php'
STOP_URL = 'https://www.mobile01.com/topicdetail.php?f=246&t=6408448'
DRIVER_PATH = '/Users/4hsinyili/Documents/GitHub/QSearch_2nd_Round/chromedriver'


class Chrome():
    def __init__(self,
                 driver_path,
                 headless=False,
                 auto_close=False,
                 inspect=False):
        self.driver = self.chrome_create(driver_path, headless, auto_close,
                                         inspect)

    def chrome_create(self, driver_path, headless, auto_close, inspect):
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

    def chrome_close(self, driver):
        driver.close()


class ListCrawler():
    def __init__(self, url, driver):
        self.url = url
        self.driver = driver

    def parse(self, url):
        driver = self.driver
        driver.get(url)
        driver.get_screenshot_as_file("screenshot.png")
        html = driver.page_source
        selector = etree.HTML(html)
        rows_with_top = selector.xpath('//div[@class="l-listTable__tr"]')
        rows = rows_with_top[1:]
        content = []
        for row in rows:
            href = row.xpath('.//div[@class="c-listTableTd__title"]/a')[0].get('href')
            link = f'https://www.mobile01.com/{href}'
            title = row.xpath('.//div[@class="c-listTableTd__title"]/a')[0].text
            post_time = row.xpath('.//div[@class="l-listTable__td l-listTable__td--time"]')[0]
            post_time = row.xpath('.//div[@class="l-listTable__td l-listTable__td--time"]')[0].xpath('./div')[1].text
            author = row.xpath('.//div[@class="l-listTable__td l-listTable__td--time"]')[0].xpath('./div/a')[0].text
            content.append((link, title, post_time, author))
        return content

    def main(self):
        url = self.url
        page = 1
        stop_url = STOP_URL  # should be mysql cursor
        results = []
        end = False
        while not end:
            content = self.parse(f'{url}?p={page}')
            for pair in content:
                if stop_url != pair[0]:
                    results.append(pair)
                else:
                    end = True
                    break
            if page == 5 or end:
                break
            page += 1

        return results


if __name__ == '__main__':
    start = time.time()
    chrome = Chrome(DRIVER_PATH, True, True, False)
    list_crawler = ListCrawler(LIST_URL, chrome.driver)
    list_crawler.main()
    stop = time.time()
    print(stop - start)
