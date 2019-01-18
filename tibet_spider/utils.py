# __author__: Mai feng
# __file_name__: tibetItem.py
# __time__: 2018:09:22:00:01
from elasticsearch_dsl import Text, Date, Keyword, Integer, Document
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import analyzer
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
import random
connections.create_connection(hosts=["localhost"])
my_analyzer = analyzer('ik_smart')


class TibetIndex(Document):
    '''西藏大学索引'''
    # suggest = Completion(analyzer=my_analyzer)
    title = Text(analyzer=my_analyzer)
    content = Text(analyzer=my_analyzer)
    url = Keyword()
    classify = Keyword()
    read_count = Keyword()
    release_time = Keyword()

    class Index:
        name = 'tibet'


class SpiderIndex(Document):
    '''西藏大学索引'''
    # suggest = Completion(analyzer=my_analyzer)
    title = Text(analyzer=my_analyzer)
    content = Text(analyzer=my_analyzer)
    url = Keyword()
    classify = Keyword()
    read_count = Keyword()
    release_time = Keyword()

    class Index:
        name = 'spider'


class TibetItem():
    '''西藏新闻item'''
    def __init__(self, user_index):
        # print(user_index)
        client = Elasticsearch()
        self.s = Search(using=client, index=user_index)
        if user_index == 'tibet':
            self.tibet = TibetIndex()
        else:
            self.tibet = SpiderIndex()
        self.rand_words = 'zxcvbnmlkjhgfdsaqwertyuiopPOIUYTREWQASDFGHJKLMNBVCXZ1234567890'
        self.rand_num  = 5

    def save_to_es(self, item):
        '''将数据存入到es'''
        # self.tibet.meta.id = item['id']
        self.tibet.classify = item['raw_type']
        self.tibet.read_count = str(random.randint(20, 3000))
        self.tibet.release_time = item['publish_time']
        self.tibet.title = item['title']
        self.tibet.url = item['url']
        # try:
        #     self.tibet.url = item['url']
        # except Exception as e:
        #     print(e)
        self.tibet.content = item['content']
        self.tibet.save()

    def from_es_search(self, word):
        data_array = []
        q = Q('multi_match', query=word, fields=['title', 'content']) # 构造q语句
        self.s = self.s.query('bool', must=[q])
        response = self.s.execute() 
        for hit in response['hits']['hits']:
            data_dict = {}
            data_dict['id'] = hit['_id']
            data_dict['title'] = hit['_source']['title']
            data_dict['content'] = hit['_source']['content']
            data_dict['url'] = hit['_source']['url']
            data_dict['classify'] = hit['_source']['classify']
            data_dict['release_time'] = hit['_source']['release_time']
            data_dict['read_count'] = hit['_source']['read_count']
            data_array.append(data_dict)
        return data_array

    def get_url_search(self, url):
        q = Q('multi_match', query=url, fields=['url']) # 构造q语句
        self.s = self.s.query('bool', must=[q])
        response = self.s.execute() 
        if response['hits']['hits']:
            # print(response['hits']['hits'])
            print(url)
            print('repeat...')
            return True
        else:
            return None

    def delete_to_es(self, _id):
        '''从es删除特定的数据'''
        item = self.tibet.get(id=_id)
        item.delete()
        return item
    
    def update_to_es(self,data):
        '''更新数据'''
        item = self.tibet.get(data['id'])
        item.update(title=data['title'],
                    content=data['content'],
                    url=data['url'],
                    classify=data['classify'],
                    release_time=data['release_time'],
                    read_count=data['read_count'])
        return item

    def get_data_by_id(self,_id):
        item = self.tibet.get(id=_id, ignore=404)
        return item

    def get_random(self):
        random.seed()
        number = []
        for i in range(self.rand_num):
            number.append(random.choice(self.rand_words))
        _id = ''.join(number)
        if self.get_data_by_id(_id):    
            return self.get_random()
        else:
            return _id


if __name__ == '__main__':
    '''初始化索引，若es中没有索引，请运行该文件'''
    TibetIndex.init()
    SpiderIndex.init()
    # tibet = TibetItem('utibet')
    # res = tibet.get_url_search('http://www.utibet.edu.cn/news/article_3_5_14488.html')
    # print(res)
    # tibet.delete_to_es('ldHU4')
