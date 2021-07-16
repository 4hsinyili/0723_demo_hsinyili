# avoid import error on lambda get_ue_detail
from datetime import datetime
import traceback

# for timing and not to get caught
import time

from QS_Modules import env
from QS_Modules import utils
from QS_Modules.utils import Chrome
from QS_Modules.models import Query

DRIVER_PATH = env.DRIVER_PATH

MYSQL_PWD = env.MYSQL_PWD
MYSQL_ACCOUNT = env.MYSQL_ACCOUNT
MYSQL_ROUTE = env.MYSQL_ROUTE
MYSQL_PORT = env.MYSQL_PORT
MYSQL_DB = env.MYSQL_DB
MOBILE01_EMAIL = env.MOBILE01_EMAIL
MOBILE01_PWD = env.MOBILE01_PWD

QUERY = Query(
    host=MYSQL_ROUTE,
    user=MYSQL_ACCOUNT,
    pwd=MYSQL_PWD,
    port=MYSQL_PORT,
    db_name=MYSQL_DB
)


class DetailCrawler():
    def __init__(self, driver, offset, limit, dt_str):
        self.driver = driver
        self.offset = offset
        self.limit = limit
        self.triggered_at = utils.parse_dt_str(dt_str)

    def crawl(self, url):
        from lxml import etree
        driver = self.driver
        driver.get(url)
        html = driver.page_source
        selector = etree.HTML(html)
        view_count = int(
            selector.xpath('//i[@class="c-icon c-icon--viewGy"]/following-sibling::span[1]')[0].text
            )
        return view_count

    def log_error(self, error_pair):
        message = traceback.format_exc()
        error = {
            'url': error_pair[0],
            'topic_id': error_pair[1],
            'triggered_at': error_pair[2],
            'loop_count': error_pair[3],
            'offset': error_pair[4],
            'message': message
        }
        QUERY.insert_track_error(error)

    def main(self):
        urls = QUERY.get_urls(self.offset, self.limit)
        tracks = []
        need_login = []
        loop_count = 0
        execution_count = 0
        for url in urls:
            try:
                view_count = self.crawl(url)
                track = {
                    'url': url,
                    'created_at': datetime.utcnow(),
                    'triggered_at': self.triggered_at,
                    'view_count': view_count
                }
                tracks.append(track)
                execution_count += 1
            except Exception:
                topic_id = int(url.split('&t=')[-1])
                tmp = (url, topic_id, self.triggered_at, loop_count, self.offset)
                need_login.append(tmp)
            loop_count += 1

        if need_login != []:
            utils.login_mobile01(self.driver, MOBILE01_EMAIL, MOBILE01_PWD)
            for error_pair in need_login:
                try:
                    time.sleep(random.randint(3, 10))
                    view_count = self.crawl(error_pair[0])
                    track = {
                        'url': error_pair[0],
                        'topic_id': error_pair[0][1],
                        'created_at': datetime.utcnow(),
                        'triggered_at': self.triggered_at,
                        'view_count': view_count
                    }
                    tracks.append(track)
                except Exception:
                    self.log_error(error_pair)

        self.driver.quit()
        QUERY.insert_track(tracks)
        return len(urls), execution_count


if __name__ == '__main__':
    offset = 0
    limit = 10
    dt_str = '2021-07-13 04:00'
    start = time.time()
    chrome = Chrome(DRIVER_PATH, True, True, False)
    detail_crawler = DetailCrawler(chrome.driver, offset, limit, dt_str)
    detail_crawler.main()
    stop = time.time()
    print(stop - start)
