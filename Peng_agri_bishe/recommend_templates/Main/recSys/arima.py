#-*- coding:utf-8 -*-
# from __future__ import print_function
import os
import pandas as pd
import numpy as np
from scipy import  stats
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot
from statsmodels.tsa.arima_model import ARIMA
root_path = os.getcwd() + "/recommend_templates/Main/recSys"

# 残差值还原
def get_pre_list(last_ele,predict_df):
	#print "get_pre_list ......."
	pre_list = [last_ele]
	for stragger in predict_df.values:
		tmp = pre_list[-1]
		pre_list.append( stragger + tmp)
	return pre_list

# 数据值初始化
def data_init(data_list): # 传入序列值
	#print "data_init ......."
	date_st, date_end = "2001","%d"%(2000 + len(data_list))
	data = pd.Series(data_list)
	data.index = pd.Index(sm.tsa.datetools.dates_from_range(date_st,date_end))
	return data,date_end

#构建ARIMA模型
def build_model(data):
	#print "build_model ......."
	data= data.diff(1) # 使用一阶差分的时间序列
	data = data.replace(np.nan,0) # 去掉第一个重合的值
	model = ARIMA(data, order=(7,0,0))
	model = model.fit(trend='nc', disp=0)
	return model

def arima_predict( model, date_end, pre_num ):
	#print "arima_predict ......."
	# pre_num 需要预测的序列长度
	pred = model.predict(date_end,"%d"%(int(date_end)+pre_num), dynamic=True)
	return pred

def arima_get_pre(data_list=None,pre_num=7):
	#print "arima_get_pre ......."
	last_ele = data_list[-1]
	data_series,date_end = data_init(data_list)
	model = build_model(data_series)
	pred = arima_predict(model,date_end,pre_num)
	pred = get_pre_list( last_ele, pred )
	return pred

def get_min_max_degree():
	#print "get_min_max_degree ......."
	data_df = pd.read_csv(root_path + "/data/weather.csv",sep="\t")
	#data_df = pd.read_csv( "./data/weather.csv",sep="\t")
	data_df = data_df.sort_values(by=['date'])
	min_list = list( data_df["min_degree"].values)
	max_list = list( data_df["max_degree"].values)
	return arima_get_pre(min_list), arima_get_pre(max_list)
