api = 'http://api.xicidaili.com/free2016.txt'

from mongoengine.queryset.visitor import Q
import requests

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

from recommend_templates.models import page
print('总条数：',page.objects().count())
cate = page.objects.filter(title__contains = '百科')
for item in cate:
    print(item.title)
print('成果推荐：',cate.count())
title = []
for item in page.objects():
    if item.title not in title:
        title.append(item.title)
print('总条数',len(title))




