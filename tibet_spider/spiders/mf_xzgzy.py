# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from tibet_spider.items import CrawlItem

import re

class XzgzySpider(scrapy.Spider):
    name = 'xzgzy'
    allowed_domains = ['www.xzgzy.cn']
    start_urls = ['http://www.xzgzy.cn/list/58.html/']

    def parse(self, response):
        urls = response.xpath('//ul[@class="e2"]/li/a/@href').extract()
        for url in urls:
            yield Request(url=response.urljoin(url), callback=self.parse_news, dont_filter=True, meta={'url':response.urljoin(url)})
        number = response.xpath('//div[@class="pagination"]/ul/li[1]/span/text()').extract_first().split('/')
        this_page = int(number[0].split(' ')[3])
        total_page = int(number[1].split(' ')[0])
        if this_page < total_page:
            if this_page > 1:
                next_url = response.xpath('//div[@class="pagination"]/ul/li[3]/a/@href').extract_first()
                yield Request(url=response.urljoin(next_url), callback=self.parse, dont_filter=True)
            else:
                next_url = response.xpath('//div[@class="pagination"]/ul/li[2]/a/@href').extract_first()
                yield Request(url=response.urljoin(next_url), callback=self.parse, dont_filter=True)
            print(response.urljoin(next_url))
        else:
            return None
        
    def parse_news(self, response):
        item = CrawlItem()
        title = response.xpath('//div[@class="title"]/h2/text()').extract_first()
        release_time = response.xpath('//div[@class="info"]/text()').extract()[1]
        read_count = response.xpath('//span[@id="hits"]/text()').extract_first()
        content = response.xpath('//div[@class="content"]/table').extract_first()
        for pt in PATTEN:
            content = re.sub(pt, '', content)
        for word in SPLIT_WORDS:
            content = ''.join(content.split(word))
        item['url'] = response.meta['url']
        item['title'] = title
        item['release_time'] = release_time
        item['read_count'] = read_count
        item['content'] = content
        item['classify'] = '文化'
        yield item

        
