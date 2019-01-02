# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re, time
from tibet_spider.items import CrawlItem


class XzlssfSpider(scrapy.Spider):
    name = 'xzlssf'
    allowed_domains = ['www.xzlssf.org']
    start_urls = ['http://www.xzlssf.org/ziyuan/news/']

    def parse(self, response):
        urls = response.xpath('//div[@class="nltit"]/a/@href').extract()
        for url in urls:
            yield Request(url=response.urljoin(url), callback=self.parse_news, dont_filter=True, meta={'url':response.urljoin(url)})
        total_page = int(response.xpath('//span[@class="pageinfo"]/strong[1]/text()').extract_first())
        this_page = int(response.xpath('//li[@class="thisclass"]/text()').extract_first())
        if this_page < total_page:
            next_url = response.xpath('//ul[@class="pagelist"]/li[13]/a/@href').extract_first()
            yield Request(url=response.urljoin(next_url), callback=self.parse, dont_filter=True)

    def parse_news(self, response):
        item = CrawlItem()
        title = response.xpath('//div[@class="wtitle"]/text()').extract_first()
        content = response.xpath('//div[@class="contt"]/div[2]').extract_first()
        for pt in PATTEN:
            content = re.sub(pt, '', content)
        for word in SPLIT_WORDS:
            content = ''.join(content.split(word))
        item['url'] = response.meta['url']
        item['title'] = title
        item['content'] = content
        item['classify'] = '文化'
        item['read_count'] = self._rand.r_number()
        item['release_time'] = time.strftime('%Y-%m-%d %H:%M',time.localtime())
        yield item