# -*- coding:utf-8 -*-

import scrapy
import re
from tibet_spider.items import CrawlItem
from scrapy.spiders import CrawlSpider
from tibet_spider.middlewares import url_test


class XZGHSpider(CrawlSpider):
    # 西藏工会新闻网
    name = 'xzgh'
    # 时政要闻，工会动态，基层工会，西藏风情，社会民生，职工文化
    start_urls = [
        'http://xz.workercn.cn/10930/10930.shtml',
        # 'http://xz.workercn.cn/10850/10850.shtml',
        # 'http://xz.workercn.cn/10858/10858.shtml',
        # 'http://xz.workercn.cn/29369/29369.shtml',
        # 'http://xz.workercn.cn/10864/10864.shtml',
        # 'http://xz.workercn.cn/29556/29556.shtml'
    ]
    basic_url = 'http://xz.workercn.cn'

    def parse(self, response):
        """
        解析子目录的文章列表的首页
        例如：http://xz.workercn.cn/10930/10930.shtml
        使用page变量记录当前的页数
        """
        url_list = response.selector.xpath('//div[@class="list_left"]/div[2]/div/ul/li/a/@href').extract()

        for i in range(0, len(url_list)):
            url = self.basic_url + url_list[i]

            if url_test(url) == 1:
                return None

            request = scrapy.Request(url=url, callback=self.parse_pages)
            yield request

        next_url = response.url[:-6] + '_2.shtml'
        page = 2
        request = scrapy.Request(url=next_url, meta={"page": page}, callback=self.get_url_list)
        yield request

    def get_url_list(self, response):
        """
        解析子目录的文章列表的非首页
        例如：http://xz.workercn.cn/10930/10930_2.shtml
        非首页的url带有index标记页数
        获取到的文章url缺少前缀部分
        用basic_url补充完整
        """
        page = response.meta["page"]
        url_list = response.selector.xpath('//div[@class="list_left"]/div[2]/div/ul/li/a/@href').extract()

        for i in range(0, len(url_list)):
            url = self.basic_url + url_list[i]

            if url_test(url) == 1:
                return None

            request = scrapy.Request(url=url, callback=self.parse_pages)
            yield request

        if url_list:
            page += 1
            next_url = re.sub(r"_([\d]+)\.", '_' + str(page) + '.', response.url)
            request = scrapy.Request(url=next_url, meta={"url_list": url_list, "page": page}, callback=self.get_url_list)
            yield request

    def parse_pages(self, response):
        """
        解析单个文章的网页，
        例如：http://xz.workercn.cn/10930/201804/26/180426092830870.shtml
        包括标题、文章类型、发表时间、来源、正文内容，
        """

        item = CrawlItem()
        item["title"] = response.selector.xpath('//div[@class="list_left"]/div[2]/div[1]/span/text()').extract_first(
            default="")
        item["raw_type"] = response.selector.xpath('//div[@class="list_left"]/div[1]/div[1]/span/a[2]/text()').extract_first(
            default="None")
        item["type"] = item["raw_type"]
        item["publish_time"] = response.selector.xpath('//div[@class="list_left"]/div[2]/div[2]/span[1]/text()'
                                                       ).extract_first(default="None")
        item["source"] = response.selector.xpath('//div[@class="list_left"]/div[2]/div[2]/span[2]/text()'
                                                 ).extract_first(default="None")
        item["url"] = response.url
        item["content"] = ''.join(response.selector.xpath('//div[@class="list_left"]/div[2]/div[3]/p/text()').extract())

        return item
