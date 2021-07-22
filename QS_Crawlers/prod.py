# datetime and time
from datetime import datetime
import time

# API calling and parsing
from flask import jsonify, request
import urllib.request
import json

# for email error
import logging
import logging.handlers

# homemade modules
from QS_Crawlers.crawl_detail import DetailCrawler
from QS_Crawlers.crawl_list import ListCrawler
from QS_Modules import utils
from QS_Modules import env
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

LIST_URL = 'https://www.mobile01.com/newtopics.php'
CRAWL_TOPIC_API = env.CRAWL_TOPIC_API
TRACK_TOPIC_API = env.TRACK_TOPIC_API
API_PWD = env.API_PWD


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='log.log')

logger = logging.getLogger(__name__)

smtp_handler = logging.handlers.SMTPHandler(mailhost=('smtp.gmail.com', 587),
                                            fromaddr=env.ERROR_EMAIL,
                                            toaddrs=[env.MY_GMAIL],
                                            subject='Error',
                                            credentials=(env.ERROR_EMAIL,
                                                         env.ERROR_PWD),
                                            secure=())
logger.addHandler(smtp_handler)


def warn(err_name):
    """Log Errors"""
    print("Something's wrong, check your mail.")
    logger.info(err_name)


def get_topic_lambda():
    end_point = f'{CRAWL_TOPIC_API}?pwd={API_PWD}'
    result = urllib.request.urlopen(end_point).read()
    data = json.loads(result)
    return data


def get_topic_cloud_run():
    pwd = request.args.get('pwd')
    if (not pwd) or (pwd != API_PWD):
        return jsonify({'message': 'not allowed'})
    chrome = utils.Chrome(headless=True, auto_close=True, inspect=False)
    list_crawler = ListCrawler(LIST_URL, chrome.driver)
    indexes = list_crawler.main()
    return jsonify({'statusCode': 200, 'data': indexes})


def track_topic_lambda(event):
    offset = event['offset']
    limit = event['limit']
    triggered_at_str = event['triggered_at_str']

    time.sleep(event['sleep'])

    end_point = f'{TRACK_TOPIC_API}?pwd={API_PWD}&offset={offset}&limit={limit}&triggered_at_str={triggered_at_str}'
    result = urllib.request.urlopen(end_point).read()
    data = json.loads(result)
    return data


def track_topic_cloud_run():
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


def log_lambda(event):
    triggered_at_str = event[0]['data']['triggered_at_str']
    results = event
    target_topics_count = 0
    execution_count = 0
    for result in results:
        target_topics_count += result['data']['target_topics_count']
        execution_count += result['data']['execution_count']
    triggered_at = utils.parse_dt_str(triggered_at_str)
    end_at = datetime.utcnow()
    QUERY.update_monitor(triggered_at, target_topics_count, end_at, execution_count)
    if ((target_topics_count - execution_count) > 10) or (execution_count <= 5):
        warn('numbers abnormal')


def main():
    data = get_topic_lambda()
    result = track_topic_lambda(data[0])
    log_lambda([result])


if __name__ == '__main__':
    main()
