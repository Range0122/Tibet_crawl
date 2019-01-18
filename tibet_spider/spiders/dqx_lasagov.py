"""Crawling news on Lhasa government website."""
# -*- coding: utf-8 -*-
import re
import scrapy
from tibet_spider.items import CrawlItem
from tibet_spider.middlewares import url_test


class LasagovSpider(scrapy.Spider):
    """Crawling news on Lhasa government website.

    Result include:
    title -- title of the news(default '')
    author -- who write the news(default '')
    date -- when the news was posted(default '')
    source -- where the news come from(default '')
    content -- main body of the news(default '')
    """

    name = 'lasagov'
    allowed_domains = ['lasa.gov.cn']
    start_urls = [
        'http://www.lasa.gov.cn/lasa/xwzx/lsyw/index.shtml',
        'http://www.lasa.gov.cn/lasa/xwzx/bmxw.shtml',
        'http://www.lasa.gov.cn/lasa/xwzx/qxxw.shtml',
        'http://www.lasa.gov.cn/lasa/xwzx/xzyw.shtml'
    ]

    def parse_news(self, response):
        """Parse news and output news content."""
        def deal_para(paras):
            str = "".join(paras)
            str = re.sub('\\n|\\t|\\r', '', str)
            str = str.replace('\xa0', '').replace('\u3000', '')
            return str

        paras = response.css('.text_content p').extract()
        content = ""
        for para in paras:
            content = content + re.sub('<.*?>', '', para)

        item = CrawlItem()

        item["title"] = deal_para(response.css('.detai_title::text').extract())
        item["raw_type"] = response.meta["type"]
        item["type"] = item["raw_type"]
        item["publish_time"] = response.css('.detail_extend span::text').extract()[1]
        item["source"] = response.css('.detail_extend span::text').extract()[2].replace('来源：', '')
        item["url"] = response.url
        item["content"] = deal_para(content)

        return item

    def parse(self, response):
        """Parse news list page and relink to every news page."""
        m = re.search('\w*\.shtml$', response.url)
        if m is not None:
            for i in range(2, 10):
                next_page = re.sub(
                    '\.shtml', '_' + str(i) + '.shtml', m.group(0))
                yield scrapy.Request(response.urljoin(next_page),
                                     callback=self.parse)
        news_links = response.css('.list li a::attr(href)').extract()
        data_type = response.css('.breadcrumb span::text').extract()[-1]
        for news_link in news_links:

            if url_test(news_link) == 1:
                return None

            yield scrapy.Request(response.urljoin(news_link), meta={"type": data_type}, callback=self.parse_news)
