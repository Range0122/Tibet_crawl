# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json


class TibetSpiderPipeline(object):
    def process_item(self, item, spider):
        if item["title"] != "None" and item["content"]:
            self.file = codecs.open(str(spider.name) + '.json', 'a', encoding="utf-8")
            lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(lines)
            self.file.close()
        return item
