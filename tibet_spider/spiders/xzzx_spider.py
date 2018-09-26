# -*- coding:utf-8 -*-

import scrapy
import re
from tibet_spider.items import XZZXSpiderItem
from scrapy.spiders import CrawlSpider


class XZZXSpider(CrawlSpider):
    # 西藏在线
    name = 'xzzx_spider'
    # 本网原创，其他藏区，西藏要闻，相关报道
    start_urls = [
        'http://www.tibetol.cn/html/zixun/bwyc/',
        'http://www.tibetol.cn/html/zixun/qitazangqu/',
        'http://www.tibetol.cn/html/zixun/xizangyaowen/',
        'http://www.tibetol.cn/html/zixun/xgbd/'
    ]

    def parse(self, response):
        """
        解析子目录的文章列表的首页
        例如：http://www.tibetol.cn/html/zixun/bwyc/
        使用page变量记录当前的页数
        """
        url_list = response.selector.xpath('//div[@class="col-left"]/ul/li/a/@href').extract()

        for i in range(0, len(url_list)):
            request = scrapy.Request(url=url_list[i], callback=self.parse_pages)
            yield request

        next_url = response.url + '2.html'
        page = 2
        request = scrapy.Request(url=next_url, meta={"url_list": url_list, "page": page},
                                 callback=self.get_url_list)
        yield request

    def get_url_list(self, response):
        """
        解析子目录的文章列表的非首页
        例如：http://www.tibetol.cn/html/zixun/bwyc/2.html
        非首页的url带有index标记页数
        """
        url_list = response.selector.xpath('//div[@class="col-left"]/ul/li/a/@href').extract()
        for i in range(0, len(url_list)):
            request = scrapy.Request(url=url_list[i], callback=self.parse_pages)
            yield request

        page = response.meta["page"]
        page += 1
        next_url = re.sub(r"([\d]+)", str(page), response.url)
        request = scrapy.Request(url=next_url, meta={"page": page}, callback=self.get_url_list)
        yield request

    def parse_pages(self, response):
        """
        解析单个文章的网页，
        例如：http://www.tibetol.cn/html/zixun/bwyc/2018/0904/39671.html
        包括标题、文章类型、发表时间、来源、正文内容，
        """
        # print(response.body.decode('utf-8'))
        item = XZZXSpiderItem()
        item["title"] = response.selector.xpath('//div[@class="col-left"]/div[2]/h1/text()').extract_first(
            default="None")
        item["type"] = response.selector.xpath('//div[@class="col-left"]/div[1]/a[3]/text()').extract_first(
            default="None")
        temp = response.selector.xpath('//div[@class="col-left"]/div[2]/h1/span/text()').extract_first(default="None")
        item["publish_time"] = temp[:19]
        item["source"] = temp[19:]
        item["content"] = ''.join(response.selector.xpath('//div[@class="content"]/table/tr/td/p/text()').extract())
        item["content"] += ''.join(response.selector.xpath('//div[@class="content"]/table/tr/td/div/text()').extract())
        item["content"] += ''.join(response.selector.xpath('//div[@class="content"]/table/tr/td/div/div/text()'
                                                           ).extract())
        item["content"] += ''.join(response.selector.xpath('//div[@class="content"]/table/tr/td/div/div/div/text()'
                                                            ).extract())
        item["content"] += ''.join(response.selector.xpath('//div[@class="content"]/table/tbody/tr/td/p/text()'
                                                           ).extract())
        item["content"] += ''.join(response.selector.xpath('//div[@class="content"]/table/tbody/tr/td/div/text()'
                                                           ).extract())
        item["content"] += ''.join(response.selector.xpath('//div[@class="content"]/table/tbody/tr/td/div/div/text()'
                                                           ).extract())
        item["content"] += ''.join(response.selector.xpath('//div[@class="content"]/table/tbody/tr/td/div/div/div/'
                                                           'text()').extract())
        return item
