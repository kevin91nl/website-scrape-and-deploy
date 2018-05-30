# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
try:
    # Python 3
    from urllib.parse import unquote
except:
    # Python 2
    from urllib import unquote


class WebPipeline(object):

    def process_item(self, item, spider):
        relative_path = item['url']
        if relative_path.startswith(spider.root_url):
            relative_path = relative_path[len(spider.root_url):]
        if '?' in relative_path:
            relative_path = relative_path.split('?')[0]
        while relative_path.startswith('/'):
            relative_path = relative_path[1:]
        relative_path = unquote(relative_path)
        if relative_path.endswith('/'):
            relative_path += '/index.html'

        relative_dir = os.path.join(spider.output_path, os.path.dirname(relative_path))
        if not os.path.exists(relative_dir):
            os.makedirs(relative_dir)

        path = os.path.join(spider.output_path, relative_path)
        if os.path.isdir(path):
            path += '/index.html'
        with open(path, 'wb') as file:
            file.write(item['content'])
