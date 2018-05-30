import os

import scrapy
from scrapy.http import Response
from scrapy.spiders import Rule

from webscraper.items import WebItem
from scrapy.linkextractors import LinkExtractor

import re


class WebSpider(scrapy.Spider):
    name = "web"

    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=False,
            callback="parse"
        )
    ]

    def __init__(self, start_url=None, root_url=None, output_path=None, exclude=None, follow_links=True):
        assert output_path is not None
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        if start_url is None:
            assert root_url is not None
            base_url = '%s' % root_url
            while base_url.endswith('/'):
                base_url = base_url[:-1]
            sitemap_url = base_url + '/sitemap.xml'
            robots_url = base_url + '/robots.txt'
            self.start_urls = [base_url + '/', sitemap_url, robots_url]
        else:
            if root_url is None:
                root_url = start_url
            self.start_urls = [start_url]
        self.root_url = root_url
        self.output_path = output_path
        self.exclude = exclude.split(',') if exclude is not None else []
        self.follow_links = str(follow_links).lower().strip() == "true" or str(follow_links).strip() == "1"

    def parse(self, response):
        url = response.url
        content = response.body
        if url.startswith(self.root_url):
            yield WebItem(url=url, content=content)

        # Detect and follow links
        if self.follow_links:
            try:
                links = LinkExtractor(
                    canonicalize=True,
                    unique=True,
                    tags=('link', 'a', 'script', 'img', 'amp-img'),
                    attrs=('href', 'src'),
                    deny_extensions=[]
                ).extract_links(response)
                links = [link.url for link in links]
            except:
                links = []
            links += re.findall('<loc>(.*)</loc>', response.body)

            for link in links:
                if link.startswith(self.root_url):
                    is_valid = True
                    for exclude_item in self.exclude:
                        if exclude_item in link:
                            is_valid = False
                            break
                    if is_valid:
                        yield scrapy.Request(url=link, callback=self.parse)
