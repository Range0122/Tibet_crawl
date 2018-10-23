# -*- coding:utf-8 -*-

import scrapy
import codecs
import re
import time
import traceback
import json
from tibet_spider.items import XZXWSpiderItem
from scrapy.spiders import CrawlSpider


class XZXWSpider(CrawlSpider):
    # 中国西藏新闻网
    name = 'xzxw_spider'
    start_urls = [
        # 西藏新闻：西藏要闻，民生新闻，科技新闻，法制西藏，科教文卫
        'http://www.xzxw.com/xw/xzyw/',
        'http://www.xzxw.com/xw/msxw/',
        'http://www.xzxw.com/xw/cjxw/',
        'http://www.xzxw.com/xw/fzxz/',
        'http://www.xzxw.com/xw/kjww/',
        # 政务要闻：政务要闻，新闻发布会，权威发布，人事任免，政府公告
        'http://www.xzxw.com/zw/zwyw/',
        'http://www.xzxw.com/zw/xwfbh/',
        'http://www.xzxw.com/zw/qwfb/',
        'http://www.xzxw.com/zw/rsrm/',
        'http://www.xzxw.com/zw/zfgg/',
        # 九眼时评：西藏日报，西藏观察，珠峰快见
        'http://www.xzxw.com/jysp/xzrbpl/',
        'http://www.xzxw.com/jysp/xzgc/',
        'http://www.xzxw.com/jysp/zfkj/',
        # 教育文化：教育要闻，考试中心，培训导学，人才就业，西藏班
        'http://www.xzxw.com/wh/jyyw/',
        'http://www.xzxw.com/wh/kszx/',
        'http://www.xzxw.com/wh/pxdx/',
        'http://www.xzxw.com/wh/rcjy/',
        'http://www.xzxw.com/wh/xzb/',
        # 旅游人文：资讯空间，触摸西藏，旅游伴侣，藏地生活，人文笔记，西藏艺术，高原视野
        'http://www.xzxw.com/lyrw/zxkj/',
        'http://www.xzxw.com/lyrw/cmxz/',
        'http://www.xzxw.com/lyrw/lybl/',
        'http://www.xzxw.com/lyrw/zdsh/',
        'http://www.xzxw.com/lyrw/rwbj/',
        'http://www.xzxw.com/lyrw/xzys/',
        'http://www.xzxw.com/lyrw/gysy/',
        # 公益：公益新闻，公益动态，公益救助
        'http://www.xzxw.com/gongyi_5554/gyxw/',
        'http://www.xzxw.com/gongyi_5554/dongtai/',
        'http://www.xzxw.com/gongyi_5554/help/',
        # 生态：生态环保
        'http://www.xzxw.com/xw/shengthb/'
    ]

    def parse(self, response):
        """
        解析子目录的文章列表的首页
        例如：http://www.xzxw.com/xw/xzyw/
        使用page变量记录当前的页数
        """
        basic_url1 = response.url
        basic_url2 = re.search(r'(http://www.xzxw.com/.*?/)', response.url)[0]
        url_list = response.selector.xpath('//div[@class="wt695 left visit"]/div/ul/li/a/@href').extract()

        for i in range(0, len(url_list)):
            if url_list[i][1] == '/':
                url_list[i] = basic_url1 + url_list[i][2:]
            else:
                url_list[i] = basic_url2 + url_list[i][3:]

            request = scrapy.Request(url=url_list[i], callback=self.parse_pages)
            yield request

        next_url = response.url + 'index_1.html'
        page = 1
        request = scrapy.Request(url=next_url, meta={"url_list": url_list, "basic_url1": basic_url1,
                                                     "basic_url2": basic_url2, "page": page}, callback=self.get_url_list)
        yield request

    def get_url_list(self, response):
        """
        解析子目录的文章列表的非首页
        例如：http://www.xzxw.com/xw/xzyw/index_2.html
        非首页的url带有index标记页数
        获取到的文章url缺少前缀部分
        用basic_url补充完整
        """
        page = response.meta["page"]
        url_list = response.selector.xpath('//div[@class="wt695 left visit"]/div/ul/li/a/@href').extract()

        for i in range(0, len(url_list)):
            if url_list[i][1] == '/':
                url_list[i] = response.meta["basic_url1"] + url_list[i][2:]
            else:
                url_list[i] = response.meta["basic_url2"] + url_list[i][3:]

            request = scrapy.Request(url=url_list[i], callback=self.parse_pages)
            yield request

        page += 1
        next_url = re.sub(r"index_([\d]+)", 'index_' + str(page), response.url)
        request = scrapy.Request(url=next_url, meta={"basic_url1": response.meta["basic_url1"],
                                                     "basic_url2": response.meta["basic_url2"],
                                                     "page": page}, callback=self.get_url_list)
        yield request

    def parse_pages(self, response):
        """
        解析单个文章的网页，
        例如：http://www.xzxw.com/xw/201809/t20180906_2356154.html
        包括标题、文章类型、发表时间、来源、正文内容，
        并使用replace、join函数
        对获得的数据进行了简单的清洗
        """
        item = XZXWSpiderItem()
        item["title"] = response.selector.xpath('//div[@class="xw_content_title"]/h3/text()').extract_first(default='').replace('\n', '') + \
                     response.selector.xpath('//div[@class="tbig_title"]/h1/text()').extract_first(default='').replace('\n', '')
        item["type"] = response.selector.xpath('//div[@class="nszw"]/p/a[2]/text()').extract_first(default="None")
        item["publish_time"] = response.selector.xpath(
            '//div[@class="xw_content_title"]/p/span[1]/text()').extract_first(default="None").replace('\n', '').replace(' ', '')
        item["source"] = response.selector.xpath('//div[@class="xw_content_title"]/p/span[2]/text()').extract_first(
            default="None").replace('\n', '').replace(' ', '')
        item["source"] = ''.join(item["source"].split())
        item["content"] = ''.join(response.selector.xpath('//div[@class="xw_daodu_detail"]').xpath('string(.)').extract())

        return item
