# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import re
import time


class TibetSpiderPipeline(object):

    def clean_item(self, content):
        content = re.sub('本网记者....', '', content)
        content = re.sub('（.*?记者.*?）', '', content)
        content = re.sub('（.*?编辑.*?）', '', content)
        content = re.sub('\t', '', content)
        clean_list = [' ', '\r', '\n', '\\"', '\t', '\u3000', '\xa0', '&nbsp;']
        for s in clean_list:
            content = content.replace(s, '')
        return content

    def process_item(self, item, spider):
        if item["title"] and item["content"]:
            item["content"] = self.clean_item(item["content"])
            self.file = codecs.open(str(spider.name) + '-' + str(time.strftime('%Y%m%d', time.localtime(time.time())))
                                    + '.json', 'a', encoding="utf-8")
            lines = json.dumps(dict(item), ensure_ascii=False) + ",\n"
            self.file.write(lines)
            self.file.close()
        return item

    def close_spider(self, spider):
        with codecs.open(str(spider.name) + '-' + str(time.strftime('%Y%m%d', time.localtime(time.time())))
                                    + '.json', 'r', encoding="utf-8") as f1:
            content = '[' + f1.read()[:-2] + ']'
            with codecs.open(str(spider.name) + '-' + str(time.strftime('%Y%m%d', time.localtime(time.time())))
                                    + '.json', 'w', encoding="utf-8") as f2:
                f2.write(content)
