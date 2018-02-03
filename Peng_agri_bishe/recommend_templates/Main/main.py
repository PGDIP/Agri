# -*- coding: utf-8 -*-

'''
@describ: this part be modefied by jichang
@email: 2218982471@qq.com
start
'''
import sys
sys.path.append('/home/ubuntu/Peng_agri_bishe/')

'''
end
'''

import jieba
from bson.objectid import ObjectId
import numpy
import pandas as pd
from recommend_templates.Main.dbManager.mongoClass import MongoOperator
from recommend_templates.Main.paserManager.newsContentPaser import *
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors

from recommend_templates.Main.paserManager.newsContent import *
from recommend_templates.Main.paserManager.price import Price

"remove db news"

import time

ROOT_PATH = os.getcwd()


# 更新数据�?保证新闻信息最�?
def updateDB():
    # mongodb使用AgriRecSys数据�?默认数据库集合为: news集合
    rec_db = MongoOperator('localhost', 27017, 'AgriRecSys', 'news')
    news_dict_list = [
        paserClass1(),
        paserClass2(),
        paserClass3(),
        paserClass4(),
        paserClass5(),
    ]
    # print "end get passer list"
    for news_dict in news_dict_list:
        if len(news_dict) == 0:
            continue
        for key, value in news_dict.items():
            # print "success insert.",key
            rec_db.insert(value, "news")  # �?news集合中插�?
        # print "end updata ",news_dict[0]["class_name"]


def tfidf2Txt():
    rec_db = MongoOperator('localhost', 27017, 'AgriRecSys', 'page')
    content_dict = list(rec_db.find())
    key_bucket = []
    content = []
    for i, content_k in enumerate(content_dict, 0):
        key_bucket.append([content_k["_id"], content_k["title"], content_k["class_name"]])
        content.append(content_k["jieba_cut_content"])
    key_bucket_df = pd.DataFrame(key_bucket, columns=["_id", "title", "class_name"])

    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词�?
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权�?
    train_set_vector = vectorizer.fit_transform(content)  # 将文本转为词频矩�?返回[(文章idx,词语id),词频]......
    tfidf = transformer.fit_transform(train_set_vector)  # 计算tf-idf,返回[(文章idx,词语id),tf-idf值]......
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词�?汉字)
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素weight[i][j]表示j词在i类文本中的tf-idf权重
    # print "整个样本集合�?样本个数*词库大小) = ",weight.shape



    # for i in range(len(weight)):  # 遍历所有文�?
        # print(u"-------这里输出�?, i, u"类文本的词语tf-idf权重------")
        # for j in range(len(word)):  # 遍历某一类文本下的词语权�?
            # print(word[j], weight[i][j])



    nbrs = NearestNeighbors(n_neighbors=10, algorithm="ball_tree").fit(weight)
    # 返回距离每个点k个最近的点和距离指数，indices可以理解为表示点的下标，distances为距�?
    distances, indices = nbrs.kneighbors(weight)
    k_nrbs_list = []
    for i in range(len(indices)):
        k_nrbs_list.append(" ".join(["%d" % x for x in indices[i]]))
    key_bucket_df["k_nbrs"] = pd.Series(k_nrbs_list)
    key_bucket_df.to_csv("./recSys/data/key_bucket.csv", index=False, index_label=False,encoding='utf-8')

def main():
    # import os
    # from recommend_templates.Main.paserManager.util import CorrectIp
    # from recommend_templates.models import page

    # try:
        # print('正在尝试删除  page数据�? �? 代理ip')
        # page.drop_collection()  #删除数据�?
        #os.remove(ROOT_PATH+r'/io/correctIp.txt') #删除代理ip
    # except:
        # pass

    #ci = CorrectIp()
    #ci.getProxyIp() #代理ip

    # print('正在�?.........中国农业科技.........')
    # zgny = ZGNYKJ(ROOT_PATH)  # .........中国农业科技.........
    # zgny.main()

    # print('正在�?.........耕种�?........')
    # gzb = GZB(ROOT_PATH)  #  .........耕种�?........
    # gzb.main_process()

    tfidf2Txt()  # tf-idf和knn算法入口

    # price = Price(ROOT_PATH)  # ...........价格........
    # price.main_price()

    # weather = Weather()  #  .........天气.........
    # weather_list = weather.getWeather()




if __name__ == '__main__':
    main()



