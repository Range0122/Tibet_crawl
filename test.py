# -*- coding:utf-8 -*-

import re
import json
import random
import time
import codecs
import operator
from pymongo import MongoClient


def clean_item(content):
    content = re.sub('本网记者....', '', content)
    content = re.sub('（.*?记者.*?）', '', content)
    content = re.sub('（.*?编辑.*?）', '', content)
    content = re.sub('（.*?文.*?）', '', content)
    content = re.sub('（.*?来源.*?）', '', content)
    content = re.sub('（.*?责编.*?）', '', content)
    content = re.sub('责任编辑(.){,10}', '', content)
    content = re.sub('编辑(.){,10}', '', content)
    content = re.sub('责编(.){,10}', '', content)
    content = re.sub('\t', '', content)
    content = re.sub('[a-zA-Z]', '', content)

    clean_list = [' ', '\r', '\n', '\\"', '\t', '\u3000', '\xa0', '&nbsp;']
    for s in clean_list:
        content = content.replace(s, '')

    if len(content) < 66:
        content = ''

    return content


def divide_json(json_path, result_path1, result_path2):
    with open(result_path1, 'a+', encoding='utf-8') as f:
        f.write('[')
    with open(result_path2, 'a+', encoding='utf-8') as f:
        f.write('[')

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            result = json.dumps(item, ensure_ascii=False)
            n = random.randint(1, 10)
            if n <= 3:
                with open(result_path1, 'a+', encoding='utf-8') as f1:
                    f1.write(result + ',\n')
            else:
                with open(result_path2, 'a+', encoding='utf-8') as f2:
                    f2.write(result + ',\n')

    with open(result_path1, 'a+', encoding='utf-8') as f2:
        f2.write(']')
    with open(result_path2, 'a+', encoding='utf-8') as f2:
        f2.write(']')


def clean_json(sour_path, dest_path):
    with open(dest_path, 'w', encoding='utf-8') as f2:
        f2.write('[')
    with open(sour_path, 'r', encoding='utf-8') as f1:
        data = json.load(f1)
        for item in data:
            item["content"] = clean_item(item["content"])
            if item["content"]:
                result = json.dumps(item, ensure_ascii=False)
                with open(dest_path, 'a+', encoding='utf-8') as f2:
                    f2.write(result + ',\n')
    with open(dest_path, 'r', encoding='utf-8') as f2:
        content = f2.read()[:-2]
    with open(dest_path, 'w', encoding='utf-8') as f2:
        f2.write(content + ']')


def test_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            try:
                test_content = item["content"]
                test_type = item["type"]
                test_title = item["title"]
                if not test_content or not test_type or not test_title:
                    print("Something is empty!")
            except Exception as e:
                print("something is wrong!")
                print(item["title"])
                print(e)
        print("finished!")
            # print(temp)


def select_json(path):
    with open(path, 'r', encoding='utf-8') as f1:
        data = json.load(f1)
        for item in data:
            if item["type"] == "经济":
                with open("economic.json", 'a+', encoding='utf-8') as f2:
                    result = json.dumps(item, ensure_ascii=False)
                    f2.write(result + ',\n')


if __name__ == '__main__':
    client = MongoClient('mongodb://localhost:27017/')
    db = client['']
    collection = db['']


    # print(collection)
    # url = 'http://www.xzlssf.org/ziyuan/news/2018/0317/2523.html'
    #
    # result = re.findall(r'\d+', url)
    #
    # publish_time = '  ' + result[0] + '-' + result[1][0:2] + '-' + result[1][2:] + ' 12:12:46'
    #
    # publish_time = '2018年12月22日 12点 唔溜十分'
    #
    # publish = re.findall(r'([\d]{4}).*?([\d]{2}).*?([\d]{2})', publish_time)[0]
    #
    # publish = publish[0] + '-' + publish[1] + '-' + publish[2]
    #
    # print(publish)

    # path = 'society.json'
    # with open(path, 'r', encoding='utf-8') as f:
    #     # data = json.load(f)
    #     test_json(path)

    # clean_json('society.json', 'test_society.json')
    # test_json('test_society.json')

    # with open('tibet_spider/xzzs_spider-20181026.json', 'r') as f:
    # # with open('tibet_spider/result/xzzx_spider-20181012.json', 'r') as f:
    #     data = json.load(f)
    #     data_type = []
    #     type_list = []
    #     i = 0
    #
    #     for item in data:
    #         i += 1
    #         type_list.append(item["type"])
    #         if item["type"] not in data_type:
    #             data_type.append(item["type"])
    #
    #     for item in data_type:
    #         print(item, type_list.count(item))
    #     print('\n')
    #
    #     print('total %d' % i)
    #     print('\n')
    #
    #     print(data_type, len(data_type))

    # sour_path = [
    #     'tibet_spider/result/total/xzgh_spider-20181026.json',
    #     'tibet_spider/result/total/xzw_spider-20181026.json',
    #     'tibet_spider/result/total/xzxw_spider-20181027.json',
    #     'tibet_spider/result/total/xzzs_spider-20181026.json',
    #     'tibet_spider/result/total/xzzx_spider-20181026.json',
    # ]
    #
    # test_json('economic.json')

    # for path in sour_path:
    #     select_json(path)

    # dest_path = [
    #     'data_test.json',
    #     'data_train.json'
    # ]
    #
    # for i in range(len(sour_path)):
    #     clean_json(sour_path=sour_path[i], dest_path=dest_path[i])
    #     test_json(dest_path[i])

    #     with open(path, 'r') as f:
    #         data = json.load(f)
    #         for item in data:
    #             if item["type"] == "政治":
    #                 with open('politics.json', 'a') as f1:
    #                     result = json.dumps(item, ensure_ascii=False)
    #                     f1.write(result + ',\n')
    #
    #             elif item["type"] == "文化":
    #                 with open('culture.json', 'a') as f2:
    #                     result = json.dumps(item, ensure_asciis=False)
    #                     f2.write(result + ',\n')
    #
    #             elif item["type"] == "社会":
    #                 with open('society.json', 'a') as f3:
    #                     result = json.dumps(item, ensure_ascii=False)
    #                     f3.write(result + ',\n')

    # test_dic = {'A': 'a', 'B': 'b', }
    # result = test_dic.get('a', 'none')
    # print(result)

    # dic = {"a": "aa"}

    # result = clean_item(test)
    # print(result)

    # clean_json("./tibet_spider/result/xzw/xzw_total.json")
    # clean_json("./tibet_spider/result/xzw/xzw_new.json")
    # test_json("./tibet_spider/result/xzw/xzw_total-0927.json")

    # clean_json("./tibet_spider/result/xzgh/xzgh-0926.json", "./tibet_spider/result/xzgh/xzgh_new.json")
    # test_json('./tibet_spider/xzzs_spider-20181011.json')

    # test_string = "Nonedasdjkascbdqwhduqwkdah"
    # t = test_string[:19]
    # s = test_string[19:] or "None"
    # print(t)
    # print(s)
