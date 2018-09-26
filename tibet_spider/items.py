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


class XZXWSpiderItem(scrapy.Item):
    # 中国西藏新闻网
    title = scrapy.Field()
    type = scrapy.Field()
    publish_time = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()
    pass


class XZWSpiderItem(scrapy.Item):
    # 中国西藏网
    title = scrapy.Field()
    type = scrapy.Field()
    publish_time = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()
    pass


class XZZXSpiderItem(scrapy.Item):
    # 西藏在线
    title = scrapy.Field()
    type = scrapy.Field()
    publish_time = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()
    pass


class XZGHSpiderItem(scrapy.Item):
    # 西藏工会新闻网
    title = scrapy.Field()
    type = scrapy.Field()
    publish_time = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()
    pass


class XZZSSpiderItem(scrapy.Item):
    # 西藏之声
    title = scrapy.Field()
    type = scrapy.Field()
    publish_time = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()
    pass


class SNWSpiderItem(scrapy.Item):
    # 山南网
    title = scrapy.Field()
    type = scrapy.Field()
    publish_time = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()
    pass
