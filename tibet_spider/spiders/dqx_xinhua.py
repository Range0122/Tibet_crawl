"""Crawling news from xinhua website."""
# -*- coding: utf-8 -*-
import json
import re
import scrapy
from tibet_spider.items import CrawlItem
from tibet_spider.middlewares import url_test


class XinhuaSpider(scrapy.Spider):
    """
    Crawling news from xinhua website.
    Result include:
    title -- title of the news(default '')
    author -- who write the news(default '')
    date -- when the news was posted(default '')
    source -- where the news come from(default '')
    content -- main body of the news(default '')
    """

    name = 'xinhua'
    allowed_domains = ['tibet.news.cn']

    def start_requests(self):
        """Do X and return a list."""
        url_head = 'http://qc.wa.news.cn/nodeart/list?nid=111'
        url_center = '&pgnum='
        url_tail = '&cnt=10&tp=1&orderby=1'
        type_ids = ['837', '801', '802', '808', '798',
                    '832', '810', '830', '846', '834', '811']

        for type_id in type_ids:
            url = url_head + type_id + url_center
            for i in range(1, 100):
                yield scrapy.Request(url=url + str(i) + url_tail, meta={"type_id": type_id}, callback=self.parse)

    def parse_news(self, response):
        """Parse news and output news content."""
        def deal_para(paras):
            str = "".join(paras)
            str = re.sub('\\n|\\t|\\r', '', str)
            str = str.replace('\xa0', '').replace('\u3000', '')
            return str

        type_mapping = {'837': "要闻",
                        '801': "政情",
                        '802': "时评",
                        '808': "援藏",
                        '798': "原创",
                        '832': "藏医药",
                        '810': "驻村",
                        '830': "旅游",
                        '846': "文化",
                        '834': "教育",
                        '811': "环保"
        }
        type_id = response.meta["type_id"]

        item = CrawlItem()

        item["title"] = deal_para(response.css('#ArticleTit::text').extract())
        item["raw_type"] = type_mapping[type_id]
        item["type"] = item["raw_type"]
        item["publish_time"] = response.css('.laiyuan::text').re('\d{4}-\d{2}-\d{2}')[0]
        item["source"] = response.css('.laiyuan a::text').extract_first()
        item["url"] = response.url
        item["content"] = deal_para(response.css('.content p::text').extract())

        return item

    def parse(self, response):
        """Parse news list page and relink to every news page."""
        type_id = response.meta["type_id"]
        text = response.text.strip('(').strip(')').strip('\n')
        datas = json.loads(text)
        if datas['status'] == 0:
            for item in datas['data']['list']:
                url = item['LinkUrl']

                if url_test(url) == 1:
                    return None

                yield scrapy.Request(url, meta={"type_id": type_id}, callback=self.parse_news)
