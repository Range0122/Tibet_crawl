# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider, Rule
from tibet_spider.items import CrawlItem
from tibet_spider.middlewares import url_test


class XzgovSpider(CrawlSpider):
    name = 'xzgov'
    allowed_domains = ['xizang.gov.cn']
    start_urls = ['http://www.xizang.gov.cn/xwzx/']

    rules = (
        Rule(LinkExtractor(restrict_css=('.xz-news-fxgl .more')),
             callback='parse_classify'),
    )

    def parse_news(self, response):
        def deal_para(paras):
            str = "".join(paras)
            str = re.sub('\\n|\\t|\\r|<.*?>', '', str)
            str = str.replace('\xa0', '').replace('\u3000', '')
            return str

        # 获取文章来源
        source_span = response.css('.xz-xl-info p span::text').extract()
        if len(source_span) > 1:
            source = source_span[1]
        else:
            source = ''

        date_p = response.css('.xz-xl-info').re('\d{4}-\d{2}-\d{2}')
        if len(date_p) > 0:
            date = date_p[0]
        else:
            date = ''

        item = CrawlItem()
        item["title"] = deal_para(response.css('.xz-xl-tit h3::text').extract())
        item["raw_type"] = response.meta["type"]
        item["type"] = item["raw_type"]
        item["publish_time"] = date
        item["source"] = source
        item["url"] = response.url
        item["content"] = deal_para(response.xpath("//div[@class='xz-xl-article']/child::*").extract()[0:-3])

        return item

    def parse_classify(self, response):
        news_links = response.css('.zx-wdsyw-con li a::attr(href)').extract()
        data_type = response.css('.xz-news-bumb a::text').extract()[-1]
        for news_link in news_links:
            yield scrapy.Request(response.urljoin(news_link), meta={"type":data_type}, callback=self.parse_news)
        temp = response.css('.xz-page script').extract_first()
        temp = temp.split('createPageHTML')[-1].strip('(|);\n</script>')
        page_num = int(temp.split(', ')[1])
        total_num = int(temp.split(', ')[0])
        if page_num + 1 < total_num:
            next_link = 'index_' + str(page_num + 1) + '.html'
            yield scrapy.Request(response.urljoin(next_link), callback=self.parse_classify)
