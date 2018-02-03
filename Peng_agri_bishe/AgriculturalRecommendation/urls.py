#-*- coding:utf-8 -*-
"""AgriculturalRecommendation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from recommend_templates.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^admin/', admin.site.urls),
    url(r'^index/$', index, name='index'),
    url(r'^news/$',class_1),
    url(r'^class_1/$', class_1), # 转到新闻类1
    url(r'^class_2/$', class_2), # 转到新闻类2
    url(r'^class_3/$', class_3), # 转到新闻类3
    url(r'^class_4/$', class_4), # 转到新闻类4
    url(r'^class_5/$', class_5), # 转到新闻类5
    url(r'^count_click_times/$', count_click_times,name='click'), # 用户点击过哪条新闻
    url(r'^shift_title_bar/$', shift_title_bar), #
    url(r'^subLogout/$', subLogout), #
    url(r'^history/$', history), # 浏览历史
    url(r'^myRecommend/$', myRecommend), # 我的推荐
    url(r'^weather/$', weather), # 天气
    url(r'article/(?P<pageId>[0-9]+)$',article,name='article'),
    ##############################################################
    url(r'^login/$', login, name='login'),
    url(r'^register/', register, name='register'),
    url(r'^registerAjax/', register_ajax, name='registerAjax'),
    url(r'weatherTest/', weatherTest, name='weather')

]
