import spider, weibo, thread, time, random, json, logging, traceback
from settings import _REDIS, _PAGE_INDEX, _QUEUE

logging.basicConfig(level=logging.INFO)


def spider_task():
    _REDIS.setnx(_PAGE_INDEX, 1)
    page_index = _REDIS.get(_PAGE_INDEX)
    task = spider.spider()
    while task.start(page_index):
        page_index = _REDIS.incr(_PAGE_INDEX)
        logging.info('Crawl the index page %s to finish' % page_index)
    while task.start():
        logging.info('Crawl the first page to finish, sleep one day')
        time.sleep(60 * 60 * 24)


try:
    thread.start_new_thread(spider_task)
    time.sleep(10)
    while True:
        data = _REDIS.rpop(_QUEUE)
        if data:
            data = json.loads(data)
            status_code = weibo.send(data[0], data[1])
            if status_code == 200:
                logging.info('Send success: [%s], sleep 1~3 hour' % data[0])
            else:
                logging.warn('Send failed, status_code %s ' % status_code)
        else:
            logging.info('No content send, sleep 1~3 hour')
        time.sleep(60 * random.randint(60, 90) * random.randint(1, 2))
except thread.error:
    logging.error("Error: unable to start thread. %s", traceback.format_exc())
except SystemError:
    logging.error('Error: %s', traceback.format_exc())
