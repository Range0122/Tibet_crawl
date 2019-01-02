"""Crawling news on people website."""
# -*- coding: utf-8 -*-
import json
import re
from urllib import request
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider, Rule
from tibet_spider.items import CrawlItem


class XzgatSpider(CrawlSpider):
    """Crawling news on people website.

    Result include:
    title -- title of the news(default '')
    author -- who write the news(default '')
    date -- when the news was posted(default '')
    source -- where the news come from(default '')
    content -- main body of the news(default '')
    """

    name = 'xzgat'
    allowed_domains = ['xzgat.gov.cn']
    start_urls = ['http://www.xzgat.gov.cn/']

    rules = (
        Rule(LinkExtractor(allow=('index\.jhtml$'),
                           restrict_css=('.cr .more')),
             callback='parse_classify'),
    )

    def parse_news(self, response):
        """Parse news and output news content."""
        def deal_para(paras):
            str = "".join(paras)
            str = re.sub('\\n|\\t|\\r', '', str)
            str = str.replace('\xa0', '').replace('\u3000', '')
            return str

        # 获取文章来源
        a = response.css('.cvhinfo a::text').extract()
        if len(a):
            source = a[0].strip()
        else:
            source = response.css(
                '.cvhinfo span::text').extract()[0].split(u'：')[1].strip()

        # 获取点击次数
        # contentId = response.url.split('/')[-1].split('.')[0]
        # base = "http://www.xzgat.gov.cn/content_view.jspx?contentId="
        # count_url = base + contentId
        # count_req = request.Request(url=count_url)
        # count_res = request.urlopen(count_req)
        # count_res = count_res.read()
        # count = json.loads(count_res.decode(encoding='utf-8'))[0]

        item = CrawlItem()
        item["title"] = deal_para(response.css('.cvhtitle h1::text').extract())
        item["raw_type"] = response.meta["type"]
        item["type"] = item["raw_type"]
        item["publish_time"] = response.css('.cvhinfo span').re('\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}')[0]
        item["source"] = source
        item["url"] = response.url
        item["content"] = deal_para(response.css('.cvbody span::text').extract())

        return item

    def parse_list(self, response):
        """Parse other news list page and relink to every news page."""
        news_links = response.css('.rlist a::attr(href)').extract()
        data_type = response.css('.location a::text').extract()[-1]
        for news_link in news_links:
            yield scrapy.Request(response.urljoin(news_link), meta={"type": data_type}, callback=self.parse_news)

    def parse_classify(self, response):
        """Parse every first news list page and relink to every news page."""
        news_links = response.css('.rlist a::attr(href)').extract()
        data_type = response.css('.location a::text').extract()[-1]
        for news_link in news_links:
            yield scrapy.Request(response.urljoin(news_link), meta={"type": data_type}, callback=self.parse_news)
        temp = response.css(".list_pagegrade").extract_first()
        total_page = int(temp.split(u'页')[0].split('/')[1])
        for i in range(2, total_page):
            next_link = 'index_' + str(i) + '.jhtml'
            yield scrapy.Request(response.urljoin(next_link),
                                 callback=self.parse_list)
