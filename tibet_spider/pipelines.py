# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import re
import time
from pymongo import MongoClient


class TibetSpiderPipeline(object):

    # 类别名映射表
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

    reg_exp = [
        '本网记者....',
        '（.*?记者.*?）',
        '（.*?编辑.*?）',
        '（.*?文.*?）',
        '（.*?来源.*?）',
        '（.*?责编.*?）',
        '责任编辑(.){,10}',
        '编辑(.){,10}',
        '责编(.){,10}',
        '[a-zA-Z]',
        "新闻( )?(图片 )?来源.+?\n",
        r'\d{4}( )?年[度初底末]',
        r'\d{4}年\d+月\d+ [日晚]',
        r'\d{4}( )?年\d+月(\d+[日号])?(\d+[时点])?(\d+分)?',
        r'\d{4}( )?年(\d+)?',
        r'\d+月\d+-\d+[日号]',
        r'\d+月( )?\d+[日号](\d+[时点])?(\d+分)?',
        r'\d+日',
        r'(今年)?\d+月(\d+)?',
        r'(上午)?\d+[时点](\d+分)?',
        r'([上下]午)?\d+:\d+',
        '[A-Za-z][0-9]+',
        '[A-Za-z_&#*()+=.:：【】"“”]',
        '(<.*?>)',
        '(（.*?）)',
        '(\(.*?\）)',
        '(\(.*?\))',
        '(http.*?\.com)',
        '(http.*?\.cn)',
        '(http.*?\.html)'
    ]

    clean_list = [' ', '\r', '\n', '\\"', '\t', '\u3000', '\xa0', '&nbsp;', '&lt', '&gt']

    def clean_item(self, content):
        # 循环匹配去除

        for item in self.reg_exp:
            content = re.sub(item, '', content)

        for item in self.clean_list:
            content = content.replace(item, '')

        # 去除正文字数太少的数据
        if len(content) < 66:
            content = ''

        return content

    def process_item(self, item, spider):
        # 将知乎抓取评论爬虫与其他爬虫区分
        if spider.name != 'zh':
            item["content"] = self.clean_item(item["content"])

            # 判断抓取的数据是否有效（是否包含标题和正文）
            if item["title"] and item["content"]:
                item["type"] = self.mapping_table.get(item["raw_type"], item["type"])
                # item["type"] = self.mapping_table.get(item["raw_type"], "未分类")

                # 调整publish_time的格式为"yyyy-mm-dd"
                try:
                    temp = re.findall(r'([\d]{4}).*?([\d]{2}).*?([\d]{2})', item["publish_time"])[0]
                    item["publish_time"] = temp[0] + '-' + temp[1] + '-' + temp[2]
                except Exception as e:
                    print(e)

                # 保存数据到mongodb数据库
                client = MongoClient('mongodb://localhost:27017/')
                db = client['spider_db']
                collection = db['items']
                collection.insert_one(dict(item))
        else:
            client = MongoClient('mongodb://localhost:27017/')
            db = client['spider_db']
            collection = db['zh_spider']
            collection.insert_one(dict(item))

    #         # 保存数据到json文件中
    #         with codecs.open(str(spider.name) + '_' + str(time.strftime('%Y%m%d', time.localtime(time.time())))
    #                                 + '.json', 'a', encoding="utf-8") as f:
    #             lines = json.dumps(dict(item), ensure_ascii=False) + ",\n"
    #             f.write(lines)
    #
        return item

    # def close_spider(self, spider):
    #     # 对已经添加完数据的json文件的首尾添加中括号，使形成完整可用的json文件
    #     try:
    #         with codecs.open(str(spider.name) + '_' + str(time.strftime('%Y%m%d', time.localtime(time.time())))
    #                                     + '.json', 'r', encoding="utf-8") as f1:
    #             content = '[' + f1.read()[:-2] + ']'
    #             with codecs.open(str(spider.name) + '_' + str(time.strftime('%Y%m%d', time.localtime(time.time())))
    #                                     + '.json', 'w', encoding="utf-8") as f2:
    #                 f2.write(content)
    #     except Exception as e:
    #         print(e)
