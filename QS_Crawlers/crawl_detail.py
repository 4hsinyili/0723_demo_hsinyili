# avoid import error on lambda get_ue_detail
from datetime import datetime

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

    def main(self):
        urls = QUERY.get_urls(self.offset, self.limit)
        tracks = []
        loop_count = 0
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
                loop_count += 1
            except Exception:
                error = {
                    'url': url,
                    'topic_id': int(url.split('&t=')[-1]),
                    'triggered_at': self.triggered_at
                }
                QUERY.insert_track_error(error)
        self.driver.quit()
        QUERY.insert_track(tracks)
        return len(urls), loop_count


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
