# -*- coding:utf-8 -*-

import scrapy
import re
from tibet_spider.items import CrawlItem
from scrapy.spiders import CrawlSpider
from tibet_spider.middlewares import url_test


class XZZSSpider(CrawlSpider):
    # 西藏之声
    name = 'xzzs'
    # 要闻，时政，社会，经济
    start_urls = [
        'http://www.vtibet.com/xw_702/yw_705/',
        'http://www.vtibet.com/xw_702/sz_704/',
        'http://www.vtibet.com/xw_702/sh_709/',
        'http://www.vtibet.com/xw_702/jj_710/'
    ]

    def parse(self, response):
        """
        解析子目录的文章列表的首页
        例如：http://www.vtibet.com/xw_702/yw_705/
        使用page变量记录当前的页数
        """
        url_list = response.selector.xpath('//table[@class=" tt"]/tbody/tr[1]/td/a/@onclick').extract()

        for i in range(0, len(url_list)):
            url_list[i] = url_list[i][:-5].replace('openurl(\'./', response.url)

            if url_test(url_list[i]) == 1:
                return None

            request = scrapy.Request(url=url_list[i], callback=self.parse_pages)
            yield request

        next_url = response.url + 'index_1.html'
        page = 1
        request = scrapy.Request(url=next_url, meta={"basic_url": response.url, "page": page},
                                 callback=self.get_url_list)
        yield request

    def get_url_list(self, response):
        """
        解析子目录的文章列表的非首页
        例如：http://www.vtibet.com/xw_702/yw_705/index_1.html
        非首页的url带有index标记页数
        获取到的文章url缺少前缀部分
        用basic_url补充完整
        """
        page = response.meta["page"]
        url_list = response.selector.xpath('//table[@class=" tt"]/tbody/tr[1]/td/a/@onclick').extract()
        for i in range(0, len(url_list)):
            try:
                url_list[i] = url_list[i][:-5].replace('openurl(\'./', response.meta["basic_url"])

                if url_test(url_list[i]) == 1:
                    return None

                request = scrapy.Request(url=url_list[i], callback=self.parse_pages)
                yield request

            except Exception as e:
                print(e)

        if url_list:
            page += 1
            next_url = re.sub(r"index_([\d]+)", 'index_' + str(page), response.url)
            request = scrapy.Request(url=next_url, meta={"basic_url": response.meta["basic_url"],
                                                         "page": page}, callback=self.get_url_list)
            yield request

    def parse_pages(self, response):
        """
        解析单个文章的网页，
        例如：http://www.vtibet.com/xw_702/yw_705/201809/t20180907_743217.html
        包括标题、文章类型、发表时间、来源、正文内容，
        并使用replace、join函数
        对获得的数据进行了简单的清洗
        """
        item = CrawlItem()
        item["title"] = response.selector.xpath('//div[@class="ne_cont_l"]/h1/text()').extract_first(default="")
        item["raw_type"] = response.selector.xpath('//div[@class="ne_cont_l"]/div[1]/a[3]/text()'
                                               ).extract_first(default="None")
        item["type"] = item["raw_type"]
        item["publish_time"] = response.selector.xpath('//div[@class="ne_cont_l"]/div[2]/div[1]/text()')\
            .extract_first(default="None")
        item["source"] = response.selector.xpath('//div[@class="ne_cont_l"]/div[2]/div[1]/em/text()').extract_first(
            default="None").replace('\n', '').replace(' ', '')
        item["content"] = ''.join(response.selector.xpath('//div[@class="ne_cont_show"]/p').xpath('string()').extract()) \
                          + ''.join(response.selector.xpath('//div[@class="ne_cont_show"]/span').xpath('string()').extract())
        item["url"] = response.url

        return item
