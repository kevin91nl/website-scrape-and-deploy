# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WebItem(scrapy.Item):
    url = scrapy.Field()
    output_path = scrapy.Field()
    root_url = scrapy.Field()
    content = scrapy.Field()
