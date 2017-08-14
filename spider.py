# -*- coding: utf-8 -*-
import os
import re
import urllib
import urllib2
import settings
import time
import json
import logging
import traceback

class spider:
    def __init__(self):
        self.url = settings._SPIDER_URL
        self.path = settings._PICTURE_PATH
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            logging.info('Create dir %s finish:' % self.path)

    def get_page(self, page_index):
        try:
            response = urllib2.urlopen(urllib2.Request(self.url + str(page_index) + '.html'))
            return response.read().decode('gbk')
        except urllib2.URLError, e:
            logging.error('Connection failed:', e.reason)
        except SystemError:
            logging.error('Error: get page index %s %s', page_index, traceback.format_exc())
        return None

    def get_page_items(self, page_index):
        page_code = self.get_page(page_index)
        if not page_code:
            logging.warn('Index page %s load failed' % page_index)
            return None
        pattern = re.compile(settings._RE_COMPILE, re.S)
        items = re.findall(pattern, page_code)
        return self.download(items)

    def download(self, items):
        result = {}
        for item in items:
            suffix = item[1][item[1].rfind('.'):]
            suffix = suffix if suffix == '.gif' else '.png'
            path_name = self.path + str(int(time.time())) + suffix
            urllib.urlretrieve(item[1], path_name)
            result.update({item[0]: path_name})
        return result

    def start(self, page_index=1):
        logging.info('Crawling page index %s' % page_index)
        items = self.get_page_items(page_index)
        if not items:
            logging.warn('Index page %s get data failed' % page_index)
            return page_index < 800
        for item in items.items():
            settings._REDIS.lpush(settings._QUEUE, json.dumps(item, ensure_ascii=False))
        return True
