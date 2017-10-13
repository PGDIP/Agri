# coding:utf-8
import numpy
import pandas
import jieba  
import jieba.posseg as pseg 
import os  
import sys  
import pandas as pd
from sklearn import feature_extraction  
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer  
root_path = os.getcwd() + "/recommend_templates/Main/recSys"

def testTF_IDF():
    corpus=[
        "我 来到 北京 清华大学",#第一类文本切词后的结果，词之间以空格隔开  
        "他 来到 了 网易 杭研 大厦",#第二类文本的切词结果  
        "小明 硕士 毕业 与 中国 科学院",#第三类文本的切词结果  
        "我 爱 北京 天安门",
    ]#第四类文本的切词结果  
    vectorizer = CountVectorizer() # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频  
    transformer = TfidfTransformer() # 该类会统计每个词语的tf-idf权值 
    train_set_vector  = vectorizer.fit_transform(corpus) # 将文本转为词频矩阵,返回[(文章idx,词语id),词频]......
    tfidf = transformer.fit_transform(train_set_vector) # 计算tf-idf,返回[(文章idx,词语id),tf-idf值]......
    word = vectorizer.get_feature_names() # 获取词袋模型中的所有词语(汉子)
    weight = tfidf.toarray()# 将tf-idf矩阵抽取出来，元素weight[i][j]表示j词在i类文本中的tf-idf权重  
    for i in range(len(weight)):#遍历所有文本
        print (u"-------这里输出第",i,u"类文本的词语tf-idf权重------")
        for j in range(len(word)):  #遍历某一类文本下的词语权重 
            print (word[j],weight[i][j])


def get_K_nearst_love(K,news_id_list):
    print( "get_K_nearst_love")
    knn_log = pd.read_csv(root_path + "/data/key_bucket.csv");
    data = dict() # 保存近邻数据{key=近邻下标,value=被推荐次数}
    own_id = set() #保存用户已经浏览过的数据
    for news_id in news_id_list:
        knbrs = knn_log["k_nbrs"][knn_log["_id"]==news_id].values
        if len(knbrs) == 0: continue;
        knbrs = knbrs[0].split(" ")
        for i in range(len(knbrs)):
            key = int(knbrs[i])
            if i == 0: own_id = own_id | set([key]) #取并集
            if data.get(key)==None:
                data[ key ] = 1
            else: data[ key ] += 1
    # 去除用户已经看过的新闻，但又出现在推荐列表中的数据
    for key,value in data.items():
        if key in own_id:
            data.pop(key)
    data = sorted( data.items(), key=lambda x:x[1], reverse=True ) # 此时的data是一个list
    ans = [] # [(10, 6), (29, 5), (20, 5), (12, 4), (24, 4)]
    for i in range(min(K,len(data))):
        ans.append( knn_log.ix[data[i][0],"_id"] )
    return ans

if __name__ == "__main__":
    #testTF_IDF()
    news_id_list = [   
        "59954610c1f4a507809402f4",
        "59954610c1f4a507809402f6",
        "59954610c1f4a507809402f1",
        "59954610c1f4a507809403d9",
        "59954610c1f4a50780940306",
        "59954610c1f4a5078094037d",
        "59954610c1f4a50780940324",
        "59954610c1f4a5078094030b",
        "59954610c1f4a507809402ef",
    ]
    print (get_K_nearst_love(3,news_id_list))

