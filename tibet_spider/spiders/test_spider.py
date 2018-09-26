# -*- coding:utf-8 -*-

import scrapy
import re
from tibet_spider.items import TestSpiderItem
from scrapy.spiders import CrawlSpider


class TestSpider(CrawlSpider):
    # 山南网
    name = 'test_spider'
    # 要闻，时政，社会，经济
    start_urls = [
        # 新闻：社会民生，山南经济，文明法治，科教文卫，环境保护，西藏新闻
        'http://www.xzsnw.com/xw/shms/',
        'http://www.xzsnw.com/xw/snjj/',
        'http://www.xzsnw.com/xw/wmfz/',
        'http://www.xzsnw.com/xw/kjww/',
        'http://www.xzsnw.com/xw/hjbh/',
        'http://www.xzsnw.com/xw/xzxw/',
        # 政务：领导活动，部门动态，山南党建，公示公告，新闻发布
        'http://www.xzsnw.com/gov/ldhd/',
        'http://www.xzsnw.com/gov/bmdt/',
        'http://www.xzsnw.com/gov/sndj/',
        'http://www.xzsnw.com/gov/gsgg/',
        'http://www.xzsnw.com/gov/xwfb/',
        # 援藏：援藏新闻
        'http://www.xzsnw.com/yz/yzxw/',
        # 旅游：旅游资讯
        'http://www.xzsnw.com/lvyou/lyzx/'
    ]

    def parse(self, response):
        """
        解析子目录的文章列表的首页
        例如：http://www.xzsnw.com/yz/yzxw/
        使用page变量记录当前的页数
        """
        url_list = response.selector.xpath('//ul[@class="txtlist"]/li/span/a/@href').extract()
        next_url = response.url + 'index_2.html'
        page = 2
        request = scrapy.Request(url=next_url, meta={"url_list": url_list, "page": page}, callback=self.get_url_list)
        yield request

    def get_url_list(self, response):
        """
        解析子目录的文章列表的非首页
        例如：http://www.xzsnw.com/yz/yzxw/index_2.html
        非首页的url带有index标记页数
        获取到的文章url缺少前缀部分
        用basic_url补充完整
        """
        url_list = response.meta["url_list"]
        page = response.meta["page"]
        temp_url_list = response.selector.xpath('//ul[@class="txtlist"]/li/span/a/@href').extract()
        if temp_url_list and page != 3:
            url_list += temp_url_list
            page += 1
            next_url = re.sub(r"index_([\d]+).html", 'index_' + str(page) + '.html', response.url)
            request = scrapy.Request(url=next_url, meta={"url_list": url_list, "page": page}, callback=self.get_url_list)
            yield request
        else:
            for i in range(0, len(url_list)):
                print(url_list[i])
                request = scrapy.Request(url=url_list[i], callback=self.parse_pages)
                yield request

    def parse_pages(self, response):
        """
        解析单个文章的网页，
        例如：http://www.xzsnw.com/gov/ldhd/141953.html
        包括标题、文章类型、发表时间、来源、正文内容，
        并使用replace、join函数
        对获得的数据进行了简单的清洗
        """
        item = TestSpiderItem()
        item["title"] = response.selector.xpath('//div[@class="xituw"]/h1/text()').extract_first(
            default="None")
        item["type"] = response.selector.xpath('//div[@class="wzdh"]/span/a[2]/text()').extract_first(default="None")
        temp = response.selector.xpath('//div[@class="xituw"]/div[1]/div[1]/span/text()'
                                       ).extract_first(default="None")
        item["publish_time"] = temp[:19]
        item["source"] = temp[19:]
        item["content"] = ''.join(response.selector.xpath('//div[@class="xituw"]/div[2]/p/text()').extract())
        return item
