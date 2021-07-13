from datetime import datetime
from QS_Crawlers.crawl_detail import DetailCrawler
from QS_Crawlers.crawl_list import ListCrawler
from QS_Modules import utils
from QS_Modules import env
from QS_Modules.models import Query
import time

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


def get_topic():
    chrome = utils.Chrome(headless=True, auto_close=True, inspect=False)
    list_crawler = ListCrawler(LIST_URL, chrome.driver)
    indexes = list_crawler.main()
    return {'statusCode': 200, 'data': indexes}


def track_topic(event):
    offset = event['offset']
    limit = event['limit']
    triggered_at_str = event['triggered_at_str']

    time.sleep(event['sleep'])

    chrome = utils.Chrome(headless=True, auto_close=True, inspect=False)
    detail_crawler = DetailCrawler(chrome.driver, offset, limit, triggered_at_str)
    target_topics_count, execution_count = detail_crawler.main()
    result = {
        'target_topics_count': target_topics_count,
        'execution_count': execution_count,
        'triggered_at_str': triggered_at_str
    }
    return result


def step_function_log(event):
    triggered_at_str = event[0]['triggered_at_str']
    results = event
    target_topics_count = 0
    execution_count = 0
    for result in results:
        target_topics_count += result['target_topics_count']
        execution_count += result['execution_count']
    triggered_at = datetime.strptime(triggered_at_str, '%Y-%m-%d %H:%M:%S')
    end_at = datetime.utcnow()
    QUERY.update_monitor(triggered_at, target_topics_count, end_at, execution_count)


def main():
    data = get_topic()
    result = track_topic(data[0])
    step_function_log([result])


if __name__ == '__main__':
    main()
