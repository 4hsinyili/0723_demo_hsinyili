# dateteime, time and random
import time
import random
from datetime import datetime, timedelta
import pytz

# homemade modules
from QS_Modules import env
from QS_Modules import utils
from QS_Modules.utils import Chrome
from QS_Modules.models import Query

LIST_URL = 'https://www.mobile01.com/newtopics.php'
DRIVER_PATH = env.DRIVER_PATH

MYSQL_PWD = env.MYSQL_PWD
MYSQL_ACCOUNT = env.MYSQL_ACCOUNT
MYSQL_ROUTE = env.MYSQL_ROUTE
MYSQL_PORT = env.MYSQL_PORT
MYSQL_DB = env.MYSQL_DB

LOCAL_TZ = pytz.timezone('Asia/Taipei')
UTC_TZ = pytz.utc

QUERY = Query(
    host=MYSQL_ROUTE,
    user=MYSQL_ACCOUNT,
    pwd=MYSQL_PWD,
    port=MYSQL_PORT,
    db_name=MYSQL_DB
)


class ListCrawler():
    def __init__(self, url, driver):
        self.url = url
        self.driver = driver
        triggered_at = datetime.utcnow()
        self.triggered_at_str = utils.output_dt_str(triggered_at)
        self.triggered_at = utils.parse_dt_str(self.triggered_at_str)
        self.stop_track_at = self.triggered_at + timedelta(hours=7)

    def parse(self, url):
        from lxml import etree
        driver = self.driver
        driver.get(url)
        # driver.get_screenshot_as_file("screenshot.png")
        html = driver.page_source
        selector = etree.HTML(html)
        try:
            page_title = selector.xpath('//div[@class="l-heading__title"]/h1[@class="t1"]')[0].text
        except Exception:
            page_title = '被擋了'
        if page_title != "新進文章":
            raise ValueError
        rows_with_top = selector.xpath('//div[@class="l-listTable__tr"]')
        rows = rows_with_top[1:]
        content = []
        for row in rows:
            href = row.xpath('.//div[@class="c-listTableTd__title"]/a')[0].get('href')
            link = f'https://www.mobile01.com/{href}'
            topic_id = int(link.split('&t=')[-1])
            title = row.xpath('.//div[@class="c-listTableTd__title"]/a')[0].text
            post_time_raw = row.xpath('.//div[@class="l-listTable__td l-listTable__td--time"]')[0]\
                .xpath('./div')[1].text
            # post_time_raw doesn't contain second!
            post_time = datetime.strptime(post_time_raw, '%Y-%m-%d %H:%M')
            post_time = LOCAL_TZ.localize(post_time)
            post_time = post_time.astimezone(UTC_TZ)
            stop_track_at = self.stop_track_at
            author = row.xpath('.//div[@class="l-listTable__td l-listTable__td--time"]')[0]\
                .xpath('./div/a')[0].text
            content.append((link, title, topic_id, post_time, stop_track_at, author))
        return content

    def log(self, topics_count):
        record = {
            'triggered_at': self.triggered_at,
            'new_topics_count': topics_count,
        }
        QUERY.insert_monitor(record)

    def dispatch(self, records_count):
        divider = 9
        lamdas_count = records_count // divider
        print('Now each tracker will track ', divider, ' results.')
        offsets = [i * divider for i in range(lamdas_count)]
        limits = [divider for i in range(lamdas_count - 1)]
        remainder = records_count - offsets[-1]
        limits.append(remainder)
        sleep_list = [0 for i in range(lamdas_count)]
        indexes = [{
            'offset': offsets[i],
            'limit': limits[i],
            'sleep': sleep_list[i],
            'triggered_at_str': self.triggered_at_str
        } for i in range(lamdas_count)]
        return indexes

    def main(self):
        url = self.url
        # QUERY.update_stop_track()
        page = 1
        latest_id = QUERY.get_latest_topic_id()
        topics = set()
        end = False
        while not end:
            time.sleep(random.randint(1, 3))
            content = self.parse(f'{url}?p={page}')
            for pair in content:
                if latest_id < pair[2]:
                    topics.add(pair)
                else:
                    end = True
                    break
            if page == 5 or end:
                break
            page += 1

        records = []
        for topic in topics:
            record = {
                'url': topic[0],
                'title': topic[1],
                'topic_id': topic[2],
                'post_time': topic[3],
                'stop_track_at': topic[4],
                'stop_track': False,
                'post_by': topic[5],
                'created_at': datetime.utcnow(),
                'triggered_at': self.triggered_at
                }
            records.append(record)
        self.driver.quit()

        QUERY.insert_topic(records)
        QUERY.update_stop_track()

        records_count = len(records)
        self.log(records_count)

        urls_count = QUERY.get_urls_count()
        indexes = self.dispatch(urls_count)

        return indexes


if __name__ == '__main__':
    start = time.time()
    chrome = Chrome(DRIVER_PATH, False, False, False)
    list_crawler = ListCrawler(LIST_URL, chrome.driver)
    list_crawler.main()
    stop = time.time()
    print(stop - start)
