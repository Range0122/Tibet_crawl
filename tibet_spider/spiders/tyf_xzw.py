# -*- coding:utf-8 -*-

import scrapy
import re
from tibet_spider.items import CrawlItem
from scrapy.spiders import CrawlSpider


class XZWSpider(CrawlSpider):
    # 中国西藏网
    name = 'xzw'
    start_urls = [
        # 新闻：原创，资讯，藏区动态
        'http://www.tibet.cn/cn/news/yc/',
        'http://www.tibet.cn/cn/news/zx/',
        'http://www.tibet.cn/cn/news/zcdt/',
        # 时政
        'http://www.tibet.cn/cn/politics/',
        # 文化：民俗，工艺，藏学，资讯
        'http://www.tibet.cn/cn/culture/ms/',
        'http://www.tibet.cn/cn/culture/gy/',
        'http://www.tibet.cn/cn/culture/zx/',
        'http://www.tibet.cn/cn/culture/wx/',
        # 援藏：资讯，人物
        'http://www.tibet.cn/cn/aid_tibet/news/',
        'http://www.tibet.cn/cn/aid_tibet/rw/',
        # 藏医药：行业动态，疾病诊疗，四季养生
        'http://www.tibet.cn/cn/medicine/news/',
        'http://www.tibet.cn/cn/medicine/jbzl/',
        'http://www.tibet.cn/cn/medicine/sjys/',
        # 宗教
        'http://www.tibet.cn/cn/religion/',
        # 生态
        'http://www.tibet.cn/cn/ecology/'
    ]

    def parse(self, response):
        """
        解析子目录的文章列表的首页
        例如：http://www.tibet.cn/cn/news/yc/
        使用page变量记录当前的页数
        """
        url_list = response.selector.xpath('//div[@class="listnews"]/ul/li/h4/a/@href').extract()

        for i in range(0, len(url_list)):
            url_list[i] = url_list[i].replace('./', response.url)
            request = scrapy.Request(url=url_list[i], callback=self.parse_pages)
            yield request

        next_url = response.url + 'index_1.html'
        page = 2
        request = scrapy.Request(url=next_url, meta={"url_list": url_list, "basic_url": response.url, "page": page},
                                 callback=self.get_url_list)
        yield request

    def get_url_list(self, response):
        """
        解析子目录的文章列表的非首页
        例如：http://www.tibet.cn/cn/news/yc/index_2.html
        非首页的url带有index标记页数
        获取到的文章url缺少前缀部分
        用basic_url补充完整
        """
        page = response.meta["page"]
        url_list = response.selector.xpath('//div[@class="listnews"]/ul/li/h4/a/@href').extract()
        for i in range(0, len(url_list)):
            url_list[i] = url_list[i].replace('./', response.meta["basic_url"])
            request = scrapy.Request(url=url_list[i], callback=self.parse_pages)
            yield request

        if url_list:
            page += 1
            next_url = re.sub(r"([\d]+)", str(page), response.url)
            request = scrapy.Request(url=next_url, meta={"basic_url": response.meta["basic_url"], "page": page},
                                     callback=self.get_url_list)
            yield request

    def parse_pages(self, response):
        """
        解析单个文章的网页，
        例如：http://www.tibet.cn/cn/aid_tibet/news/201808/t20180829_6215689.html
        包括标题、文章类型、发表时间、来源、正文内容，
        并使用replace、join函数
        对获得的数据进行了简单的清洗
        """
        item = CrawlItem()
        item["title"] = response.selector.xpath('//div[@class="title_box"]/h2/text()').extract_first(
            default="")
        temp_type = response.selector.xpath('//body/div[@class="wrap"]/div[1]/a[2]/text()').extract_first(default="None")
        item["raw_type"] = response.selector.xpath('//body/div[@class="wrap"]/div[1]/a[3]/text()').extract_first(default=temp_type)
        item["type"] = item["raw_type"]
        item["publish_time"] = response.selector.xpath('//div[@class="title_box"]/div[1]/span[2]/text()')\
            .extract_first(default="None").replace('\n', '').replace(' ', '')
        item["source"] = response.selector.xpath('//div[@class="title_box"]/div[1]/span[3]/text()').extract_first(
            default="None").replace('\n', '').replace(' ', '')
        item["content"] = ''.join(response.selector.xpath('//div[@class="text botborder"]/p').xpath('string(.)').extract())

        return item
