# -*- coding: utf-8 -*-

# '''
# @describ: this part be modefied by jichang
# @email: 2218982471@qq.com
# start
# '''
# import sys
# sys.path.append('/home/ubuntu/Peng_agri_bishe/')

# '''
# end
# '''

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


# 更新数据库,保证新闻信息最新
def updateDB():
    # mongodb使用AgriRecSys数据库,默认数据库集合为: news集合
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
            rec_db.insert(value, "news")  # 向 news集合中插入
            # print "end updata ",news_dict[0]["class_name"]


def main_process():
    cpu = multiprocessing.cpu_count()
    rec_db = MongoOperator('localhost', 27017, 'AgriRecSys', 'page')
    content_dict = list(rec_db.find())
    item_list = []
    item_list_1 = []
    list_ = []
    list_1 = []
    j = 0
    m = 0
    for i, item in enumerate(content_dict, 1):
        list_.append(item)
        if (i - j) == int(len(content_dict) / cpu):
            for k ,item_1 in enumerate(list_,1):
                list_1.append(item_1)
                if (k - m) == int(len(list_) / 20):
                    item_list_1.append(list_1)
                    list_1 = []
                    m = k
            item_list.append(item_list_1)
            item_list_1 = []
            list_ = []
            j = i
            m = 0
    pool = Pool(processes=cpu)  # 建立进程池
    pool.map(add_thread, item_list)  # 映射到主函数中进行循环


def add_thread(item_list=[]):
    print('>>>>>>>>>主进程： ', os.getpid())
    threads = []
    for i in range(len(item_list)):
        thread = threading.Thread(target=tfidf2Txt, name='...线程:....' + str(i), args=(item_list[i],))
        threads.append(thread)
        thread.start()
    # 阻塞主进程，等待所有子线程结束
    for thread in threads:
        thread.join()


def tfidf2Txt(content_dict = []):
    # rec_db = MongoOperator('localhost', 27017, 'AgriRecSys', 'page')
    # content_dict = list(rec_db.find())
    print('每个线程完成：',len(content_dict),'个')
    key_bucket = []
    content = []
    for i, content_k in enumerate(content_dict, 0):
        key_bucket.append([content_k["_id"], content_k["title"], content_k["class_name"]])
        content.append(content_k["jieba_cut_content"])
    key_bucket_df = pd.DataFrame(key_bucket, columns=["_id", "title", "class_name"])

    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    train_set_vector = vectorizer.fit_transform(content)  # 将文本转为词频矩阵,返回[(文章idx,词语id),词频]......
    tfidf = transformer.fit_transform(train_set_vector)  # 计算tf-idf,返回[(文章idx,词语id),tf-idf值]......
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语(汉字)
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素weight[i][j]表示j词在i类文本中的tf-idf权重
    # print "整个样本集合中(样本个数*词库大小) = ",weight.shape



    # for i in range(len(weight)):  # 遍历所有文本
    #     print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
    #     for j in range(len(word)):  # 遍历某一类文本下的词语权重
    #         print(word[j], weight[i][j])

    nbrs = NearestNeighbors(n_neighbors=10, algorithm="ball_tree").fit(weight)
    # 返回距离每个点k个最近的点和距离指数，indices可以理解为表示点的下标，distances为距离
    distances, indices = nbrs.kneighbors(weight)
    k_nrbs_list = []
    for i in range(len(indices)):
        k_nrbs_list.append(" ".join(["%d" % x for x in indices[i]]))
    key_bucket_df["k_nbrs"] = pd.Series(k_nrbs_list)
    key_bucket_df.to_csv("./recSys/data/key_bucket.csv", mode ='a',index=False, index_label=False, encoding='utf-8')


# def tfidf2Txt():
#     rec_db = MongoOperator('localhost', 27017, 'AgriRecSys', 'page')
#     content_dict = list(rec_db.find())
#     key_bucket = []
#     content = []
#     for i, content_k in enumerate(content_dict, 0):
#         key_bucket.append([content_k["_id"], content_k["title"], content_k["class_name"]])
#         content.append(content_k["jieba_cut_content"])
#     key_bucket_df = pd.DataFrame(key_bucket, columns=["_id", "title", "class_name"])
#
#     vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
#     transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
#     train_set_vector = vectorizer.fit_transform(content)  # 将文本转为词频矩阵,返回[(文章idx,词语id),词频]......
#     tfidf = transformer.fit_transform(train_set_vector)  # 计算tf-idf,返回[(文章idx,词语id),tf-idf值]......
#     word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语(汉字)
#     weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素weight[i][j]表示j词在i类文本中的tf-idf权重
#     # print "整个样本集合中(样本个数*词库大小) = ",weight.shape
#
#     nbrs = NearestNeighbors(n_neighbors=10, algorithm="ball_tree").fit(weight)
#     # 返回距离每个点k个最近的点和距离指数，indices可以理解为表示点的下标，distances为距离
#     distances, indices = nbrs.kneighbors(weight)
#     k_nrbs_list = []
#     for i in range(len(indices)):
#         k_nrbs_list.append(" ".join(["%d" % x for x in indices[i]]))
#     key_bucket_df["k_nbrs"] = pd.Series(k_nrbs_list)
#     key_bucket_df.to_csv("./recSys/data/key_bucket.csv", index=False, index_label=False,encoding='utf-8')

def main():
    # import os
    # from recommend_templates.Main.paserManager.util import CorrectIp
    # from recommend_templates.models import page
    #
    # try:
    #     print('正在尝试删除  page数据库  和  代理ip')
    #     page.drop_collection()  #删除数据库
    #     os.remove(ROOT_PATH+r'/io/correctIp.txt') #删除代理ip
    # except:
    #     pass
    #
    # ci = CorrectIp()
    # ci.getProxyIp() #代理ip

    # print('正在爬 .........中国农业科技.........')
    # zgny = ZGNYKJ(ROOT_PATH)  # .........中国农业科技.........
    # zgny.main()

    # print('正在爬 .........耕种帮.........')
    # gzb = GZB(ROOT_PATH)  #  .........耕种帮.........
    # gzb.main_process()
    #
    #tfidf2Txt()  # tf-idf和knn算法入口
    main_process()

    # price = Price(ROOT_PATH)  # ...........价格........
    # price.main_price()

    # weather = Weather()  #  .........天气.........
    # weather_list = weather.getWeather()


if __name__ == '__main__':
    main()
