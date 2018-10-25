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
        "时政要闻 ": " 政治 ",
        "工会动态 ": " 保留 ",
        " 基层工会 ": " 保留 ",
        " 西藏风情 ": " 文化 ",
        " 社会民生 ": " 社会 ",
        " 职工文化 ": " 保留 ",
        # 中国西藏网
        "原创": "保留",
        "资讯": "保留",
        "藏区动态": "保留",
        "时政": "政治",
        "民俗": "文化",
        "工艺": "文化",
        "藏学": "文化",
        "资讯": "保留",
        "资讯": "保留",
        "人物": "	 保留",
        "行业动态": "社会",
        "疾病诊疗": "文化",
        "四季养生": "保留",
        "宗教": "政治",
        "生态": "保留",
        # 中国西藏新闻网
        "西藏要闻": "	保留",
        "民生新闻": "	社会",
        "科技新闻": "	保留",
        "法制西藏": "	社会",
        "科教文卫": "	保留",
        "政务要闻": "	政治",
        "新闻发布会": "保留",
        "权威发布": "	保留",
        "人事任免": "	保留",
        "政府公告": "	保留",
        "西藏日报": "	保留",
        "西藏观察": "保留",
        "珠峰快见": "保留",
        "教育要闻": "	文化",
        "考试中心": "	文化",
        "培训导学": "	文化",
        "人才就业": "	文化",
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
        "生态环保": "	保留",
        # 西藏之声
        "要闻": "保留",
        "时政": "政治",
        "社会": "社会",
        "经济": "保留",
        # 西藏在线
        "本网原创": "保留",
        "其他藏区": "保留",
        "西藏要闻": "保留",
        "相关报道": "保留",
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
        # if item["title"] and item["content"] and item["type"] != 'None':
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
