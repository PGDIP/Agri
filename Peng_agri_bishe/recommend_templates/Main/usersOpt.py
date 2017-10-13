# -*- coding: utf-8 -*-
import os, sys
import jieba
import numpy
import pandas as pd
from imp import reload
from recommend_templates.Main.dbManager.mongoClass import MongoOperator

"""
处理网站用户相关操作
"""
def userRegist(user_name,user_passwd):
	value = {
		"user_name": user_name,
		"user_passwd": user_passwd,
		"user_read_id": ""
	}
	rec_db = MongoOperator('localhost',27017,'AgriRecSys','users')
	rec_db.insert(value,"users")

def userRead():
	pass


def userLogin(user_name,user_passwd):
	rec_db = MongoOperator('localhost',27017,'AgriRecSys','users')
	user_id = rec_db.find( {"user_name": user_name,"user_passwd": user_passwd,} )
	if user_id != None:
		return "success"
	else:
		return user_id["_id"]



