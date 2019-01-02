# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
from tibet_spider.items import CrawlItem


class TtmcSpider(scrapy.Spider):
    name = 'ttmc'
    allowed_domains = ['www.ttmc.edu.cn']
    start_urls = ['http://www.ttmc.edu.cn/zwb/shouye/xyyw.htm', 
                  'http://www.ttmc.edu.cn/zwb/shouye/bmdt.htm',
                  'http://www.ttmc.edu.cn/zwb/shouye/tzgg.htm',
                  'http://www.ttmc.edu.cn/zwb/shouye/mtjj.htm',
                  'http://www.ttmc.edu.cn/zwb/shouye/zcrj.htm']

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.get_news_list, dont_filter=True)

    def get_news_list(self, response):
        num = 20
        try:
            this_num = response.xpath('//*[@id="fanye42162"]/text()').extract_first().split('\xa0')[2].split('/')[0]
            this_num = int(this_num)
            for i in range(20 * (this_num - 1 ), num * this_num):
                news_id = 'line42162_{id}'.format(id=i)
                url = response.xpath('//tr[@id="{id}"]/td[1]/a/@href'.format(id=news_id)).extract_first()
                yield Request(url=response.urljoin(url), callback=self.parse_news, dont_filter=True, meta={'url':response.urljoin(url)})
            next_url = response.xpath('//a[@class="Next"]/@href').extract_first()            
            yield Request(url=response.urljoin(next_url), callback=self.get_news_list, dont_filter=True)
            print(response.urljoin(next_url))
        except Exception as e:
            print('get_news_list', e)
        
    def parse_news(self, response):
        title = response.xpath('//*[@class="titlestyle42165"]/text()').extract_first().strip()
        release_time = response.xpath('//*[@class="timestyle42165"]/text()').extract_first().strip()
        content = response.xpath('//*[@id="vsb_content"]').extract_first()
        for pt in PATTEN:
            content = re.sub(pt, '', content)
        for word in SPLIT_WORDS:
            content = ''.join(content.split(word))
        item = CrawlItem()
        item['url'] = response.meta['url']
        item['title'] = title
        item['release_time'] = release_time
        item['content'] = content
        item['classify'] = '文化'
        item['read_count'] = self._rand.r_number()
        yield item
