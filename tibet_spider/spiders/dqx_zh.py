# -*- coding: utf-8 -*-
import json
import scrapy
from tibet_spider.items import ZhihuItem
from pymongo import MongoClient

class ZhSpider(scrapy.Spider):
    name = 'zh'
    allowed_domains = ['zhihu.com']
    start_urls = ["https://www.zhihu.com/api/v4/topics/19559654/feeds/essence?include=data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp&data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.is_normal,comment_count,voteup_count,content,relevant_info,excerpt.author.badge[?(type=best_answerer)].topics&data[?(target.type=topic_sticky_module)].target.data[?(target.type=article)].target.content,voteup_count,comment_count,voting,author.badge[?(type=best_answerer)].topics&data[?(target.type=topic_sticky_module)].target.data[?(target.type=people)].target.answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&data[?(target.type=answer)].target.annotation_detail,content,hermes_label,is_labeled,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp&data[?(target.type=answer)].target.author.badge[?(type=best_answerer)].topics&data[?(target.type=article)].target.annotation_detail,content,hermes_label,is_labeled,author.badge[?(type=best_answerer)].topics&data[?(target.type=question)].target.annotation_detail,comment_count&limit=10&offset=100"]
    maxPage = 100
    currentPage = 0

    def start_requests(self):
        self.cookies = {
            "__utma": "51854390.1245842814.1543580590.1543580590.1543580590.1",
            "__utmc": "51854390",
            "__utmv": "51854390.100--|2=registration_date=20150913=1^3=entry_date=20150913=1",
            "__utmz": "51854390.1543580590.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/",
            "_xsrf": "MltZIX1GrGgZ1Hp6pGCz8w3XvZnmBfro",
            "_zap": "7542ec36-54c5-4667-a2a8-548b08845ef3",
            "capsion_ticket": "2|1:0|10:1543580540|14:capsion_ticket|44:NmU4Mjc1YjU1ZmNiNDNhZmE4M2E1YjFmNjg4YWJlN2M=|9e6efa10e652799aada59027ec45c714d7bf03579034336acc33f0a454d8fe48",
            "d_c0": "AJAmCCUW2Q2PTvjhBk6HXoSKNsLwTj_KDS0=|1530686727",
            "q_c1": "62074beeee89402fa75bf4be89355b1c|1543580587000|1530686727000",
            "tst": "r",
            "z_c0": "2|1:0|10:1543580584|4:z_c0|92:Mi4xX2lVV0FnQUFBQUFBa0NZSUpSYlpEU1lBQUFCZ0FsVk5wM251WEFBTUwydDB4cGF6RVFZVldxTTh3OXJmREFRam9B|38a5b3e23f40e9778cab938d0ec5f87db6433c3d996aafd4d9095c793db27c35"
        }
        self.headers = {
            'content-type': 'application/json',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
        }
        return [scrapy.FormRequest('https://www.zhihu.com/',
                                   headers=self.headers, cookies=self.cookies,
                                   callback=self.after_login)]

    def after_login(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True, headers=self.headers)

    def parse(self, response):
        text = response.text.strip('(').strip(')').strip('\n')
        datas = json.loads(text)
        for item in datas["data"]:
            if "question" in item["target"]:
                # 获取问题评论
                pass
                url = "www.zhihu.com/question/" + \
                    str(item["target"]["question"]["id"]) + \
                    "/answer/" + str(item["target"]["id"])
                # yield scrapy.Request(url, dont_filter=True, headers=self.headers, callback=self.parse_question)
            else:
                # 获取文章评论
                url = item["target"]["url"]
                id = item["target"]["id"]
                count = item["target"]["comment_count"]
                title = item["target"]["title"]
                limit = 20
                url = "https://www.zhihu.com/api/v4/articles/" + \
                    str(id) + "/root_comments?include=data[*].author,collapsed,reply_to_author,disliked,content,voting,vote_count,is_parent_author,is_author&order=normal&limit=" + str(
                        limit) + "&status=open"
                for i in range(0, int(count / limit) + 1):
                    nexturl = url + "&offset=" + str(i * limit)
                    yield scrapy.Request(nexturl, dont_filter=True, headers=self.headers,
                                         callback=lambda response, title=title: self.parse_comments(response, title))
        nextLink = datas["paging"]["next"]
        if self.currentPage <= self.maxPage and nextLink != response.url:
            self.currentPage += 1
            yield scrapy.Request(nextLink, dont_filter=True, headers=self.headers, callback=self.parse)

    def parse_comments(self, response, title=""):
        text = response.text.strip('(').strip(')').strip('\n')
        datas = json.loads(text)
        for item in datas['data']:
            author = item["author"]["member"]
            info = {
                "title": title,
                "name": author["name"] if "name" in author else "",
                "gender": author["gender"] if "gender" in author else "",
                "url_token": author["url_token"] if "url_token" in author else "",
                "content": item["content"]
            }
            nexturl = "https://www.zhihu.com/people/" + \
                info["url_token"]+"/activities"
            yield scrapy.Request(nexturl, dont_filter=True, headers=self.headers,
                                 callback=lambda response, info=info: self.parse_user(response, info))

    def parse_user(self, response, info):
        text = response.css("#js-initialData::text").extract_first()
        text = text.strip('(').strip(')').strip('\n')
        datas = json.loads(text)
        userAllInfo = datas["initialState"]["entities"]["users"][info["url_token"]]
        userInfo = {
            "majors": [],
            "business": "",
            "locations": []
        }
        if "educations" in userAllInfo:
            for item in userAllInfo["educations"]:
                if "major" in item:
                    userInfo["majors"].append(item["major"]["name"])
        if "business" in userAllInfo:
            userInfo["business"] = userAllInfo["business"]["name"]
        if "locations" in userAllInfo:
            for item in userAllInfo["locations"]:
                userInfo["locations"].append(item["name"])

        item = ZhihuItem()

        item["title"] = info["title"] or ''
        item["name"] = info["name"] or ''
        item["gender"] = info["gender"] or ''
        item["url_token"] = info["url_token"] or ''
        item["content"] = info["content"] or ''
        item["majors"] = userInfo["majors"] or ''
        item["business"] = userInfo["business"] or ''
        item["locations"] = userInfo["locations"] or ''

        # 查询数据库中是否已经存在该条数据
        client = MongoClient('mongodb://localhost:27017/')
        db = client['spider_db']
        collection = db['zh_spider']

        result = collection.find_one({"url_token": item["url_token"]})

        if result is None:
            return item

        # return {
        #     "info": info,
        #     "user_info": userInfo
        # }

    def parse_article(self, response):
        yield {"url": response.url}

    def parse_question(self, response):
        pass
