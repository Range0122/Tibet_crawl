# -*- coding: utf-8 -*-
from scrapy import Spider, Request
import re
from tibet_spider.items import CrawlItem


class UtibetSpider(Spider):
    name = 'utibet'
    allowed_domains = ['utibet.edu.cn/']
    start_urls = ['http://www.utibet.edu.cn/news/article_3_5_0.html']
    # stop_next = False

    def parse(self, response):
        url_lists = response.xpath('//div[@class="new_title_list"]/a/@href').extract()
        # 暂时先不用管



        for url in url_lists:
            yield Request(url=response.urljoin(url), 
            callback=self.parse_pages, 
            dont_filter=True)
        #     res_url = TibetItem('utibet').get_url_search(response.urljoin(url))
        #     if res_url:
        #         print('更新结束')
        #         self.stop_next = True
        #         break
        #     else:
        #         res_url = TibetItem('spider').get_url_search(response.urljoin(url))
        #         if res_url:
        #             print('更新结束')
        #             self.stop_next = True
        #             break
        #         else:

        number = response.xpath('//div[@id="page"]/text()').extract_first().strip().split(' ')[0].split('：')[1].split('\r')[0]
        this_num = int(number.split('/')[0])
        total = int(number.split('/')[1].split('页')[0])
        try:
            # if self.stop_next is False:
            if this_num < total:
                next_url = 'http://www.utibet.edu.cn/news/article_3_5____{page}.html'.format(page=str(this_num + 1))
                print('next_url: ', next_url)
                yield Request(url=next_url, 
                callback=self.parse, 
                dont_filter=True)
        except Exception as e:
            print(e)

    def parse_pages(self, response):
        item = CrawlItem()

        item['url'] = response.url
        item['title'] = response.xpath('//*[@class="text"]/table/tr[1]/td/div[2]/text()').extract_first()
        item["raw_type"] = '校园新闻'
        item["type"] = item["raw_type"]
        item['publish_time'] = response.xpath('//*[@class="text"]/table/tr[2]/td/div/text()').extract_first().strip().split('：')[2]
        item['content'] = response.xpath('//*[@class="text"]/div').extract_first()
        item["source"] = '西藏大学'

        return item
