"""Crawling news on Tibet Discipline Inspection Commission website."""
# -*- coding: utf-8 -*-
import re
import scrapy
from tibet_spider.items import CrawlItem
from tibet_spider.middlewares import url_test


class XzjjwSpider(scrapy.Spider):
    """Crawling news on Tibet Discipline Inspection Commission website.

    Result include:
    title -- title of the news(default '')
    author -- who write the news(default '')
    date -- when the news was posted(default '')
    source -- where the news come from(default '')
    content -- main body of the news(default '')
    """

    name = 'xzjjw'
    allowed_domains = ['xzjjw.gov.cn']
    start_urls = ['http://www.xzjjw.gov.cn/yw.php?type=17']
    page_n = 1
    total_page = 1
    base_url = 'http://www.xzjjw.gov.cn/yw.php?type=17&page='

    def parse_news(self, response):
        def deal_para(paras):
            str = "".join(paras)
            str = re.sub('\\n|\\t|\\r', '', str)
            str = str.replace('\xa0', ' ').replace('\u3000', ' ')
            return str

        # m = re.search(u'发布时间：\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}',
        #               time_source)
        # m = re.search('\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', m.group(0))
        # time = m.group(0)
        #
        # m = re.search(u'来源：[^\s]*', time_source)
        # source = m.group(0).split(u'：')[1]

        time_source = response.css('.title .time::text').extract_first()

        item = CrawlItem()
        item["title"] = deal_para(response.css('.title1 h4::text').extract())
        item["raw_type"] = response.meta["type"]
        item["type"] = item["raw_type"]
        item["publish_time"] = time_source.split(u"\xa0")[3].split(u'：')[1]
        item["source"] = time_source.split(u"\xa0")[0].split(u'：')[1]
        item["url"] = response.url
        item["content"] = deal_para(response.css('.main p span::text').extract())

        return item

    def parse(self, response):
        """Parse news list page and relink to every news page."""
        # 解析文章页面
        news_links = response.css('.new_title li a::attr(href)').extract()
        data_type = "廉政要闻"
        for news_link in news_links:
            yield scrapy.Request(response.urljoin(news_link), meta={"type": data_type}, callback=self.parse_news)

        # 获取总页数
        if self.page_n == 1:
            script_con = response.css('.list_pages script').extract_first()
            m = re.search('pageCount\s=\d*', script_con)
            m = re.search('\d+', m.group(0))
            self.total_page = int(m.group(0))

        # 定位到下一页
        next_page = self.page_n + 1
        self.page_n = next_page
        next_page_link = self.base_url + str(next_page)
        if next_page <= self.total_page:
            yield scrapy.Request(next_page_link, callback=self.parse)
