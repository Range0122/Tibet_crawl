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

    mapping_table = {
        # 西藏工会新闻网
        "时政要闻": "政治",
        "工会动态": "工会动态",
        "基层工会": "基层工会",
        "西藏风情": "文化",
        "社会民生": "社会",
        "职工文化": "职工文化",
        # 中国西藏网
        "原创": "原创",
        "资讯": "资讯",
        "藏区动态": "藏区动态",
        "民俗": "文化",
        "工艺": "文化",
        "藏学": "文化",
        "人物": "人物",
        "行业动态": "社会",
        "疾病诊疗": "文化",
        "四季养生": "四季养生",
        "宗教": "政治",
        "生态": "生态",
        # 中国西藏新闻网
        "西藏要闻": "西藏要闻",
        "民生新闻": "社会",
        "财经新闻": "财经新闻",
        "法治西藏": "社会",
        "科教文卫": "科教文卫",
        "政务要闻": "政治",
        "新闻发布会": "新闻发布会",
        "权威发布": "权威发布",
        "人事任免": "人事任免",
        "政府公告": "政府公告",
        "西藏日报评论": "西藏日报评论",
        "西藏观察": "西藏观察",
        "珠峰快见": "珠峰快见",
        "教育要闻": "文化",
        "考试中心": "文化",
        "培训导学": "文化",
        "人才就业": "文化",
        "西藏班": "文化",
        "资讯空间": "文化",
        "触摸西藏": "文化",
        "旅游伴侣": "文化",
        "藏地生活": "文化",
        "人文笔记": "文化",
        "西藏艺术": "文化",
        "高原视野": "文化",
        "公益新闻": "社会",
        "公益动态": "社会",
        "公益救助": "社会",
        "生态环保": "生态环保",
        # 西藏之声
        "要闻": "要闻",
        "时政": "政治",
        "社会": "社会",
        "经济": "经济",
        # 西藏在线
        "本网原创": "本网原创",
        "其他藏区": "其他藏区",
        "相关报道": "相关报道",
        "藏地往事": "藏地往事",
        "人与自然": "文化",
        "高原民俗": "文化",
        "雪域文化": "文化",
        "圣地之旅": "文化",
        "文物考古": "文化",
        "学术理论": "文化",
        "古今人物": "文化",
        "书讯": "文化",
        "书评": "文化"
    }

    def clean_item(self, content):
        content = re.sub('本网记者....', '', content)
        content = re.sub('（.*?记者.*?）', '', content)
        content = re.sub('（.*?编辑.*?）', '', content)
        content = re.sub('（.*?文.*?）', '', content)
        content = re.sub('\t', '', content)
        clean_list = [' ', '\r', '\n', '\\"', '\t', '\u3000', '\xa0', '&nbsp;']
        for s in clean_list:
            content = content.replace(s, '')
        return content

    def process_item(self, item, spider):
        item["content"] = self.clean_item(item["content"])
        item["type"] = self.clean_item(item["type"])

        # item["type"] = self.mapping_table.get(item["type"], item["type"])
        item["type"] = self.mapping_table.get(item["type"], "未分类")

        if item["title"] and item["content"]:
            self.file = codecs.open(str(spider.name) + '-' + str(time.strftime('%Y%m%d', time.localtime(time.time())))
                                    + '.json', 'a', encoding="utf-8")
            lines = json.dumps(dict(item), ensure_ascii=False) + ",\n"
            self.file.write(lines)
            self.file.close()
        return item

    def close_spider(self, spider):
        try:
            with codecs.open(str(spider.name) + '-' + str(time.strftime('%Y%m%d', time.localtime(time.time())))
                                        + '.json', 'r', encoding="utf-8") as f1:
                content = '[' + f1.read()[:-2] + ']'
                with codecs.open(str(spider.name) + '-' + str(time.strftime('%Y%m%d', time.localtime(time.time())))
                                        + '.json', 'w', encoding="utf-8") as f2:
                    f2.write(content)
        except Exception as e:
            print(e)
