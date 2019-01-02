# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TestSpiderItem(scrapy.Item):
    # 测试
    title = scrapy.Field()
    type = scrapy.Field()
    publish_time = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()
    pass


class CrawlItem(scrapy.Item):
    title = scrapy.Field()
    raw_type = scrapy.Field()
    type = scrapy.Field()
    publish_time = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    pass
