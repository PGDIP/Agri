#-*- coding:utf-8 -*-
# from __future__ import print_function
import pandas as pd
import numpy as np
from scipy import  stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot
from statsmodels.tsa.arima_model import ARIMA



dta = [10930,10318,10595,10972,7706,6756,9092,10551,9722,10913,11151,8186,6422, 
6337,11649,11652,10310,12043,7937,6476,9662,9570,9981,9331,9449,6773,6304,9355, 
10477,10148,10395,11261,8713,7299,10424,10795,11069,11602,11427,9095,7707,10767, 
12136,12812,12006,12528,10329,7818,11719,11683,12603,11495,13670,11337,10232, 
13261,13230,15535,16837,19598,14823,11622,19391,18177,19994,14723,15694,13248, 
9543,12872,13101,15053,12619,13749,10228,9725,14729,12518,14564,15085,14722, 
11999,9390,13481,14795,15845,15271,14686,11054,10395]


# 残差值还原
def get_pre_list(last_ele,predict_df):
	pre_list = [last_ele]
	for stragger in predict_df.values:
		tmp = pre_list[-1]
		pre_list.append( stragger + tmp)
	return pre_list


def data_init(dta):
	dta = pd.Series(dta)
	dta.index = pd.Index(sm.tsa.datetools.dates_from_range('2001','2090'))
	# dta.plot(figsize=(12,8))
	# ############################    时间序列差分  ################################
	# fig = plt.figure(figsize=(12,8))
	# ax1 = fig.add_subplot(111)
	# diff1 = dta.diff(1) # 原列 - 整列向下平移一个单位后的列 1即为差分的阶数
	# diff1.plot(ax=ax1)
	return dta


def build_model(dta):
	# fig = plt.figure(figsize=(12,8))
	# ax2= fig.add_subplot(111)
	# diff2 = dta.diff(2)
	# diff2.plot(ax=ax2)
	####################  检查平稳时间序列的自相关图和偏自相关图  ###############
	dta= dta.diff(1) #我们已经知道要使用一阶差分的时间序列，之前判断差分的程序可以注释掉
	# fig = plt.figure(figsize=(12,8))
	# ax1 = fig.add_subplot(211)
	# fig = sm.graphics.tsa.plot_acf(dta,lags=40,ax=ax1)
	# ax2 = fig.add_subplot(212)
	# fig = sm.graphics.tsa.plot_pacf(dta,lags=40,ax=ax2)

	dta = dta.replace(np.nan,0)
	arma_mod20 = sm.tsa.ARMA(dta,(7,0)).fit()
	# print(arma_mod20.aic,arma_mod20.bic,arma_mod20.hqic)
	# arma_mod30 = sm.tsa.ARMA(dta,(0,1)).fit()
	# print(arma_mod30.aic,arma_mod30.bic,arma_mod30.hqic)
	# arma_mod40 = sm.tsa.ARMA(dta,(7,1)).fit()
	# print(arma_mod40.aic,arma_mod40.bic,arma_mod40.hqic)
	# arma_mod50 = sm.tsa.ARMA(dta,(8,0)).fit()
	# print(arma_mod50.aic,arma_mod50.bic,arma_mod50.hqic)
	return arma_mod20

def predict(model):
	# print( len(dta) )
	pred = model.predict('2090', '2100', dynamic=True)
	# print( len(dta) )
	# print(pred)
	# fig, ax = plt.subplots(figsize=(12, 8))
	# ax = dta.ix['2001':].plot(ax=ax)
	# pred.plot(ax=ax)
	return pred
	
if __name__ == '__main__':
	last_ele = dta[-1]
	dta_series = data_init(dta)
	model = build_model(dta_series)
	pred = predict(model)
	print type(pred)
	pred = get_pre_list( last_ele, pred )
	dta = dta + pred
	pd.Series(dta).plot()
	plt.show();




