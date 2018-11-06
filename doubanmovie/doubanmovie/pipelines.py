# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import setting
import pymongo

class DoubanmoviePipeline(object):
    def __init__(self):
        # 获取setting中的主机号，端口号和数据库名
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']
        # 创建mongodb链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指向指定数据库
        mdb = client[dbname]
        # 获取数据库里存放数据的表名
        self.post = mdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        data = dict(item)
        # 向指定表里插入数据
        self.post.insert(data)
        return item


