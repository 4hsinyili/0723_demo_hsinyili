from flask import Flask, jsonify, request
import chromedriver_binary  # noqa
import env
import utils
from models import Query
import pytz
from datetime import datetime
import time
import random
import traceback

MYSQL_PWD = env.MYSQL_PWD
MYSQL_ACCOUNT = env.MYSQL_ACCOUNT
MYSQL_ROUTE = env.MYSQL_ROUTE
MYSQL_PORT = env.MYSQL_PORT
MYSQL_DB = env.MYSQL_DB
API_PWD = env.API_PWD
MOBILE01_EMAIL = env.MOBILE01_EMAIL
MOBILE01_PWD = env.MOBILE01_PWD

LOCAL_TZ = pytz.timezone('Asia/Taipei')
UTC_TZ = pytz.utc

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
                time.sleep(random.randint(3, 10))
                view_count = self.crawl(url)
                track = {
                    'url': url,
                    'topic_id': int(url.split('&t=')[-1]),
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


app = Flask(__name__)


@app.route("/")
def main():
    pwd = request.args.get('pwd')
    if (not pwd) or (pwd != API_PWD):
        return jsonify({'message': 'not allowed'})

    offset = int(request.args.get('offset'))
    limit = int(request.args.get('limit'))
    triggered_at_str = request.args.get('triggered_at_str')

    if limit == 0:
        result = {
            'target_topics_count': 0,
            'execution_count': 0,
            'triggered_at_str': triggered_at_str
        }
        return jsonify({"data": result})

    chrome = utils.Chrome(headless=True, auto_close=True, inspect=False)
    detail_crawler = DetailCrawler(chrome.driver, offset, limit, triggered_at_str)
    target_topics_count, execution_count = detail_crawler.main()
    result = {
        'target_topics_count': target_topics_count,
        'execution_count': execution_count,
        'triggered_at_str': triggered_at_str
    }
    return jsonify({"data": result})
