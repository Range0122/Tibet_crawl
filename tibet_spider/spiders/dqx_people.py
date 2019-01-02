"""Crawling news on people website."""
# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tibet_spider.items import CrawlItem


class PeopleSpider(CrawlSpider):
    """Crawling news on people website.

    Result include:
    title -- title of the news(default '')
    author -- who write the news(default '')
    date -- when the news was posted(default '')
    source -- where the news come from(default '')
    content -- main body of the news(default '')
    """

    name = 'people'
    allowed_domains = ['xz.people.com.cn']
    start_urls = ['http://xz.people.com.cn/']

    rules = (
        Rule(LinkExtractor(allow=('index\.html'),
                           restrict_css=('h3 i')), callback='parse_classify'),
    )

    def parse_news(self, response):
        """Parse news and output news content."""
        def deal_para(paras):
            str = "".join(paras)
            str = re.sub('\\n|\\t|\\r', '', str)
            str = str.replace('\xa0', '').replace('\u3000', '')
            return str

        item = CrawlItem()

        item["title"] = deal_para(response.css('h1::text').extract())
        item["raw_type"] = response.meta["item_type"]
        item["type"] = item["raw_type"]
        item["publish_time"] = response.css('.fl::text').re('\d{4}年\d{2}月\d{2}日\d{2}[:]\d{2}')[0]
        item["source"] = response.css('.text_title .fl a::text').extract_first()
        item["url"] = response.url
        item["content"] = deal_para(response.css('.box_con p::text').extract())

        return item

    def parse_classify(self, response):
        """Parse news list page and relink to every news page."""
        news_links = response.css('.ej_list_box a::attr(href)').re('.*/n2.*')
        item_type = response.css('.lujing a::text').extract()[-1]
        for news_link in news_links:
            request = scrapy.Request(response.urljoin(news_link), meta={"item_type": item_type},
                                     callback=self.parse_news)
            yield request
        current_page = response.css('.page_n .common_current_page::text').extract_first()
        next_page = int(current_page) + 1
        re_string = 'index' + str(next_page) + '\.html'
        next_page_link = response.css('.page_n a::attr(href)').re(re_string)

        if len(next_page_link):
            yield scrapy.Request(response.urljoin(next_page_link[0]), callback=self.parse_classify)
