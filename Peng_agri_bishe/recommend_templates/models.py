# -*- coding: utf-8 -*-
# Create your models here. 一个model对应数据库一张数据表
from django.db import models
from mongoengine import *
from datetime import datetime

# 连接数据库
connect('AgriRecSys')  # 连接本地blog数据库


# connect('Data',host='127.0.0.1',port='27017')

# 如需验证和指定主机名
# connect('blog', host='192.168.3.1', username='root', password='1234')

class User(Document):
    # userId = IntField(required=True)
    # id = ObjectIdField(primary_key=True,required=True)
    username = StringField(max_length=1000, required=True)
    password = StringField(max_length=1000, required=True)
    email = StringField(default=None,required=False)
    age = StringField(default=None)
    looked_list = ListField(default=None)
    user_love = ListField(default=None)
    address = StringField(default=None)


class price(Document):
    name = StringField(required=True)
    market = StringField(required=True)
    date = StringField(required=True)
    average = StringField(required=True)
    week_price = StringField(default=None)

class page(Document):
    jieba_cut_content=StringField(default=None)
    title = StringField(required=True)
    content = DictField(required=True)
    class_name = StringField(required=True)
    pageId = IntField(required=True)
