# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
from tibet_spider.items import CrawlItem
from tibet_spider.middlewares import url_test


class XzlssfSpider(scrapy.Spider):
    name = 'xzlssf'
    allowed_domains = ['www.xzlssf.org']
    start_urls = ['http://www.xzlssf.org/ziyuan/news/']

    def parse(self, response):
        urls = response.xpath('//div[@class="nltit"]/a/@href').extract()
        for url in urls:
            yield Request(url=response.urljoin(url), 
            callback=self.parse_news, 
            dont_filter=True)
        total_page = int(response.xpath('//span[@class="pageinfo"]/strong[1]/text()').extract_first())
        this_page = int(response.xpath('//li[@class="thisclass"]/text()').extract_first())
        if this_page < total_page:
            next_url = 'http://www.xzlssf.org/ziyuan/news/list_24_{page}.html'.format(page=str(this_page + 1))
            # print(next_url)
            yield Request(url=next_url,
            callback=self.parse,
            dont_filter=True)

    def parse_news(self, response):
        item = CrawlItem()

        item['url'] = response.url
        item['title'] = response.xpath('//div[@class="wtitle"]/text()').extract_first()
        item['content'] = response.xpath('//div[@class="contt"]/div[2]').extract_first()
        item['raw_type'] = '校园新闻'
        item["type"] = item["raw_type"]
        item["source"] = '拉萨师范高等专科学校'
        temp = re.findall(r'\d+', item['url'])
        item['publish_time'] = temp[0] + '-' + temp[1][0:2] + '-' + temp[1][2:]

        return item
