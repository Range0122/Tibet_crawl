# -*- coding: utf-8 -*-
import re
import scrapy
from tibet_spider.items import CrawlItem
from tibet_spider.middlewares import url_test


class ZgxzqwSpider(scrapy.Spider):
    name = 'zgxzqw'
    allowed_domains = ['zgxzqw.gov.cn']
    start_urls = ['http://www.zgxzqw.gov.cn/xwzx/']

    def parse_news(self, response):
        def deal_para(paras):
            str = "".join(paras)
            str = re.sub('\\n|\\t|\\r|<.*?>', '', str)
            str = str.replace('\xa0', ' ').replace('\u3000', ' ')
            return str

        sub = response.css('.sub span').extract()
        cont = response.xpath("//div[@class='TRS_Editor']/child::*").extract()
        if cont[0].find('<style') == 0:
            cont = cont[1:]

        item = CrawlItem()
        item["title"] = deal_para(response.css('.det-tit::text').extract())
        item["raw_type"] = response.meta["type"]
        item["type"] = item["raw_type"]
        item["publish_time"] = deal_para(sub[2])
        item["source"] = deal_para(sub[0])
        item["url"] = response.url
        item["content"] = deal_para(cont)

        return item

    def parse(self, response):
        news_links = response.css('.mt10 a::attr(href)').extract()
        data_type = "新闻中心"
        for news_link in news_links:
            yield scrapy.Request(response.urljoin(news_link), meta={"type": data_type}, callback=self.parse_news)

        temp = response.css('.page-box script').re('createPageHTML(.*)')
        temp = temp[1].strip('(|);').split(',')
        total_page = int(temp[0])
        page_num = int(temp[1])
        if page_num + 1 < total_page:
            next_link = 'index_' + str(page_num + 1) + '.htm'
            yield scrapy.Request(response.urljoin(next_link),
                                 callback=self.parse)
