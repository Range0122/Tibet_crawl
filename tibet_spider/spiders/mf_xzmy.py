# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Request, FormRequest
from tibet_spider.items import CrawlItem


class XzmySpider(scrapy.Spider):
    name = 'xzmy'
    allowed_domains = ['www.xzmy.edu.cn/']
    start_urls = ['http://www.xzmy.edu.cn/contentlist']
    column_ids = ['1', '381', '2', '380', '994'] # 民大新闻，媒体看民大，通知公告，校园短波，学术活动    

    def start_requests(self):
        for _column_id in self.column_ids:
            formdata = {
                'dept_id':'1',
                'column_id':_column_id,
                'column_type':'1',
                'per':'15',
                'url':'list',
                'page':'1'
            }
            yield FormRequest(url=self.start_urls[0], formdata= formdata, callback=self.get_news_list, meta={'formdata':formdata})

    def get_news_list(self, response):
        formdata = response.meta['formdata']
        urls = response.xpath('//div[@class="gnlist"]/ul/li/a/@href').extract()
        for url in urls:
            yield Request(url=response.urljoin(url), callback=self.parse_news, dont_filter=True, meta={'url':response.urljoin(url)})
        total_page = int(response.xpath('//div[@class="page"]/text()').extract_first().split(' ')[3])
        for i in range(2, total_page + 1):
            formdata['page'] = str(i)
            yield FormRequest(url=self.start_urls[0], formdata= formdata, callback=self.get_news_list, meta={'formdata':formdata})
            
    def parse_news(self, response):
        item = CrawlItem()
        title = response.xpath('//h2[@class="tith2"]/text()').extract_first()
        release_time = response.xpath('//div[@class="time"]/span[2]/text()').extract_first().split('：')[1]
        read_count = response.xpath('//div[@class="time"]/span[3]/text()').extract_first().split('\r\n')[1].split(' ')[0]
        content = response.xpath('//div[@class="MainNewsContent"]').extract_first()
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
