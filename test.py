# -*- coding:utf-8 -*-

import re
import json
import random
import time
import codecs
import operator


def clean_item(content):
    content = re.sub('本网记者....', '', content)
    content = re.sub('（.*?记者.*?）', '', content)
    content = re.sub('（.*?编辑.*?）', '', content)
    content = re.sub('\t', '', content)
    clean_list = [' ', '\r', '\n', '\\"', '\t', '\u3000', '\xa0', '&nbsp;']
    for s in clean_list:
        content = content.replace(s, '')
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
            result = json.dumps(item, ensure_ascii=False)
            with open(dest_path, 'a+', encoding='utf-8') as f2:
                f2.write(result + ',\n')
    with open(dest_path, 'a+', encoding='utf-8') as f2:
        f2.write(']')


def test_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            temp = item["content"]
            # print(temp)


if __name__ == '__main__':
    # with open('tibet_spider/xzw_spider-20181025.json', 'r') as f:
    with open('tibet_spider/result/xzzx_spider-20181012.json', 'r') as f:
        data = json.load(f)
        data_type = []

        for item in data:
            if item["type"] not in data_type:
                data_type.append(item["type"])

        print(len(data_type))
        print(data_type)

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
