# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mongoengine.queryset.visitor import Q
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.http import JsonResponse
from bson import ObjectId
import os
import json
from recommend_templates.Main.paserManager.newsContentPaser import *
from recommend_templates.Main.dbManager.mongoClass import MongoOperator
from recommend_templates.Main.recSys.knn import get_K_nearst_love
from recommend_templates.Main.recSys.arima import get_min_max_degree
from recommend_templates.pager import Pagination
from recommend_templates.Main.paserManager.newsContentPaser import paserWeather
from recommend_templates.models import *

ROOT_URL = os.getcwd()


# Create your views here.
# 主界面
def index(request, data={}):
    # data = {"user_name":"jeje","user_pwd":"jeje"}
    # return HttpResponse("Hello world！ This is my first trial. [Poll的笔记]")
    # return Http404
    try:
        current_page = request.GET.get('p')
        user_name = request.session.get('user_name')
        db_ans1 = page.objects.filter(Q(class_name__contains='要闻'))
        db_ans2 = page.objects.filter(Q(class_name__contains='论坛'))
        db_ans3 = page.objects.filter(Q(class_name__contains='种植技术'))
        db_ans4 = page.objects.filter(Q(class_name__contains = '科技与健康'))
        db_ans5 = page.objects.filter(Q(class_name__contains = '成果推介'))
        db_ans6 = page.objects.filter(Q(title__contains='水稻'))
        db_ans7 = page.objects.filter(Q(title__contains='玉米'))
        db_ans8 = page.objects.filter(Q(title__contains='蔬菜'))
        db_ans9 = page.objects.filter(Q(title__contains='小麦'))
        data = {}
        ans_list1 = []
        ans_list2 = []
        ans_list3 = []
        ans_list4 = []
        ans_list5 = []
        ans_list6 = []
        ans_list7 = []
        ans_list8 = []
        ans_list9 = []
        count = 0
        for i, news in enumerate(db_ans1, 0):
            try:
                content = str(news.content['content0'])
                if news.content['content0'] == "":
                    content = str(news.content['content1'])
                ans_list1.append({
                    'content': content,
                    "news": news,
                })
                count += 1
            except:
                continue

        count = 0
        for i, news in enumerate(db_ans2, 0):
            try:
                content = str(news.content['content0'])
                if news.content['content0'] == "":
                    content = str(news.content['content1'])
                ans_list2.append({
                    'content': content,
                    "news": news,
                })
                count += 1
            except:
                continue

        count = 0
        for i, news in enumerate(db_ans3, 0):
            try:
                content = str(news.content['content0'])
                if news.content['content0'] == "":
                    content = str(news.content['content1'])
                ans_list3.append({
                    'content': content,
                    "news": news,
                })
                count += 1
            except:
                continue


        count = 0
        for i, news in enumerate(db_ans4, 0):
            try:
                content = str(news.content['content0'])
                if news.content['content0'] == "":
                    content = str(news.content['content1'])
                ans_list4.append({
                    'content': content,
                    "news": news,
                })
                count += 1
            except:
                continue


        count = 0
        for i, news in enumerate(db_ans5, 0):
            try:
                content = str(news.content['content0'])
                if news.content['content0'] == "":
                    content = str(news.content['content1'])
                ans_list5.append({
                    'content': content,
                    "news": news,
                })
                count += 1
            except:
                continue



        count = 0
        for i, news in enumerate(db_ans6, 0):
            try:
                content = str(news.content['content0'])
                if news.content['content0'] == "":
                    content = str(news.content['content1'])
                ans_list6.append({
                    'content': content,
                    "news": news,
                })
                count += 1
            except:
                continue

        count = 0
        for i, news in enumerate(db_ans7, 0):
            try:
                content = str(news.content['content0'])
                if news.content['content0'] == "":
                    content = str(news.content['content1'])
                ans_list7.append({
                    'content': content,
                    "news": news,
                })
                count += 1
            except:
                continue

        count = 0
        for i, news in enumerate(db_ans8, 0):
            try:
                content = str(news.content['content0'])
                if news.content['content0'] == "":
                    content = str(news.content['content1'])
                ans_list8.append({
                    'content': content,
                    "news": news,
                })
                count += 1
            except:
                continue

        count = 0
        for i, news in enumerate(db_ans9, 0):
            try:
                content = str(news.content['content0'])
                if news.content['content0'] == "":
                    content = str(news.content['content1'])
                ans_list9.append({
                    'content': content,
                    "news": news,
                })
                count += 1
            except:
                continue




        page_obj = Pagination(count, current_page)
        data["news_list1"] = ans_list1[page_obj.start():page_obj.end()]
        data["news_list2"] = ans_list2[page_obj.start():page_obj.end()]
        data["news_list3"] = ans_list3[page_obj.start():page_obj.end()]
        data["news_list4"] = ans_list4[page_obj.start():page_obj.end()]
        data["news_list5"] = ans_list5[page_obj.start():page_obj.end()]
        data["news_list6"] = ans_list6[page_obj.start():page_obj.end()]
        data["news_list7"] = ans_list7[page_obj.start():page_obj.end()]
        data["news_list8"] = ans_list8[page_obj.start():page_obj.end()]
        data["news_list9"] = ans_list9[page_obj.start():page_obj.end()]

        data["user_name"] = user_name



        #主页天气模块
        pred_min_list, pred_max_list = get_min_max_degree()
        data_w = {};
        ans_list_w = []
        weather_list = paserWeather()  # [{},{},{},...]
        for i, weather in enumerate(weather_list, 0):
            if i >= 7: break;
            ans_list_w.append({
                "key": i,
                "content": weather,
            })
        data["weather_data"] = ans_list_w
        data["pred_max"] = ["%.2f" % (degree) for degree in pred_max_list[1:]]
        data["pred_min"] = ["%.2f" % (degree) for degree in pred_min_list[1:]]




    except:
        return index(request)
    return render(request, ROOT_URL + "/recommend_templates/templates/homepage.html",
                  {'data': data, 'page_obj': page_obj})


# 第一类新闻 农业新闻
def class_1(request, data={}):
    print("class_1 ......")
    try:
        current_page = request.GET.get('p')
        user_name = request.session.get('user_name')
        db_ans = page.objects.filter(Q(class_name__contains = '要闻') | Q(class_name__contains = '论坛')| Q(class_name__contains = '新闻'))
        data = {}
        ans_list = []
        count = 0
        for i, news in enumerate(db_ans, 0):
            try:
                content = str(news.content['content0'])
                if news.content['content0'] == "":
                    content = str(news.content['content1'])
                ans_list.append({
                    'content': content,
                    "news": news,
                })
                count += 1
            except:
                continue
        page_obj = Pagination(count, current_page)
        data["news_list"] = ans_list[page_obj.start():page_obj.end()]
        data["user_name"] = user_name
    except:
        return index(request)
    return render(request, ROOT_URL + "/recommend_templates/templates/class_1.html",
                  {'data': data, 'page_obj': page_obj})


# 第二类新闻 病虫害
def class_2(request):
    print("class_2 ......")
    try:
        current_page = request.GET.get('p')
        user_name = request.session.get('user_name')
        db_ans = page.objects.filter(Q(class_name__contains = '植物保护技术'))
        data = {}
        ans_list = []
        count = 0
        for i, news in enumerate(db_ans, 0):
            try:
                content = str(news.content['content0'])
                if news.content['content0'] == "":
                    content = str(news.content['content1'])
                ans_list.append({
                    'content': content,
                    "news": news,
                })
                count += 1
            except:
                continue
        page_obj = Pagination(count, current_page)
        data["news_list"] = ans_list[page_obj.start():page_obj.end()]
        data["user_name"] = user_name
    except:
        return index(request)
    return render(request, ROOT_URL + "/recommend_templates/templates/class_2.html",
                  {'data': data, 'page_obj': page_obj})


def news(request, data={}):
    data['user_name'] = request.session.get('user_name')
    return render(request, ROOT_URL + "/recommend_templates/templates/news.html", {'data': data})


# 第三类新闻  种植技术
def class_3(request):
    print("class_3 ......")
    try:
        current_page = request.GET.get('p')
        user_name = request.session.get('user_name')
        db_ans = page.objects.filter(Q(class_name__contains = '种植技术') | Q(class_name__contains = '种植业技术'))
        data = {}
        ans_list = []
        count = 0
        for i, news in enumerate(db_ans, 0):
            try:
                content = str(news.content['content0'])
                if news.content['content0'] == "":
                    content = str(news.content['content1'])
                ans_list.append({
                    'content': content,
                    "news": news,
                })
                count += 1
            except:
                continue
        page_obj = Pagination(count, current_page)
        data["news_list"] = ans_list[page_obj.start():page_obj.end()]
        data["user_name"] = user_name
    except:
        return index(request)

    return render(request, 'class_3.html', {'data': data, 'page_obj': page_obj})


# 第四类新闻  市场价格
def class_4(request, data={}):
    print("class_4 ......")
    try:
        current_page = request.GET.get('p')
        user_name = request.session.get('user_name')
        db_ans = page.objects.filter(class_name__contains='市场价格')
        data = {}
        ans_list = []
        count = 0
        for i, news in enumerate(db_ans, 0):
            try:
                content = str(news.content['content0'])
                if news.content['content0'] == "":
                    content = str(news.content['content1'])
                ans_list.append({
                    'content': content,
                    "news": news,
                })
                count += 1
            except:
                continue
        page_obj = Pagination(count, current_page)
        data["news_list"] = ans_list[page_obj.start():page_obj.end()]
        data["user_name"] = user_name
    except:
        return index(request)
    return render(request, ROOT_URL + "/recommend_templates/templates/class_4.html",
                  {'data': data, 'page_obj': page_obj})


# 第五类新闻  科技新闻
def class_5(request, data={}):
    print("class_5 ......")
    try:
        current_page = request.GET.get('p')
        user_name = request.session.get('user_name')
        db_ans = page.objects.filter(Q(class_name__contains = '科技与健康')| Q(class_name__contains = '成果推荐'))
        data = {}
        ans_list = []
        count = 0
        for i, news in enumerate(db_ans, 0):
            try:
                content = str(news.content['content0'])
                if news.content['content0'] == "":
                    content = str(news.content['content1'])
                ans_list.append({
                    'content': content,
                    "news": news,
                })
                count += 1
            except:
                continue
        page_obj = Pagination(count, current_page)
        data["news_list"] = ans_list[page_obj.start():page_obj.end()]
        data["user_name"] = user_name
    except:
        return index(request)

    return render(request, 'class_5.html', {'data': data, 'page_obj': page_obj})


def myRecommend(request, data={}):
    print("myRecommend ......")
    user_name = request.session.get('user_name')
    try:
        user = User.objects.filter(username=user_name)[0]
        new_id_list = user.looked_list
        if new_id_list == None:  # 面对冷启动问题
            pass  #
        else:
            # print "========*****#######*********"
            rec_new_id_list = get_K_nearst_love(8, new_id_list)  # 推荐5个最优新闻名称给用户
        ans_list = []
        for i, news_id in enumerate(rec_new_id_list, 0):
            rec_db = MongoOperator('localhost', 27017, 'AgriRecSys', 'page')
            db_ans = rec_db.find({"_id": ObjectId(news_id)})
            if db_ans.count() == 0:
                continue
            db_ans = db_ans[0]
            ans_list.append({
                "news": db_ans,
                "news_id": str(db_ans["_id"]),
            })
        data["user_name"] = user_name
        data["news_list"] = ans_list
    except:

        return index(request)

    return render(request, ROOT_URL + "/recommend_templates/templates/myRecommend.html", {'data': data})  # 注意路径一定要写对


def history(request):
    print("history ......")
    data = {}
    user_name = request.session.get('user_name')
    try:
        user = User.objects.filter(username=user_name).first()
        new_id_list = user.looked_list
        ans_list = []
        for i, news_id in enumerate(new_id_list, 0):
            rec_d = MongoOperator('localhost', 27017, 'AgriRecSys', 'page')
            db_ans = rec_d.find({'_id': ObjectId(news_id)})
            if db_ans.count() == 0:
                continue
            db_ans = db_ans[0]
            ans_list.append({
                "news": db_ans,
                "news_id": str(db_ans["_id"]),
            })
        data["user_name"] = user_name
        data["news_list"] = ans_list
    except:
        return index(request)
    return render(request, ROOT_URL + "/recommend_templates/templates/history.html", {'data': data})  # 注意路径一定要写对


# 获取用户对某一个新闻的点击 ajax技术
def count_click_times(request):
    print("count_click_times ...... ")
    if request.POST:
        news_id = request.POST.get('news_id')
        user_name = request.POST.get('user_name')
    else:
        news_id = request.GET.get('news_id')
        user_name = request.GET.get('user_name')
    try:
        user = User.objects.filter(username=user_name).first()
        if user.looked_list is None:
            looked_list = set([news_id])
        else:
            looked_list = set(list(user.looked_list))
            looked_list = looked_list | set([news_id])
        User.objects(username=user_name).update(looked_list=looked_list)
    except:
        return index(request)


def shift_title_bar(request):
    print("shift_title_bar ...... ")
    data = []
    if request.POST:
        bar_name = request.POST.get('bar_name')
        user_name = request.POST.get('user_name')
    else:
        bar_name = request.GET.get('bar_name')
        user_name = request.GET.get('user_name')
    data["bar_name"] = bar_name
    data["user_name"] = user_name
    return JsonResponse(data)


# 天气栏
def weather(request):
    # print "weather ......"
    try:
        pred_min_list, pred_max_list = get_min_max_degree()
        user_name = request.session.get('user_name')
        data = {};
        ans_list = []
        weather_list = paserWeather()  # [{},{},{},...]
        for i, weather in enumerate(weather_list, 0):
            if i >= 7: break;
            ans_list.append({
                "key": i,
                "content": weather,
            })
        data["weather_data"] = ans_list
        data["user_name"] = user_name
        data["pred_max"] = ["%.2f" % (degree) for degree in pred_max_list[1:]]
        data["pred_min"] = ["%.2f" % (degree) for degree in pred_min_list[1:]]
    except:
        return index(request)
    return render(request, ROOT_URL + "/recommend_templates/templates/weather.html", data)  # 注意路径一定要写对


# 显示文章
def article(request, pageId):
    article = page.objects.filter(pageId=pageId).first()
    return render(request, 'article.html', {'articles': article})


##############################################################################################################################################

def weatherTest(request):
    # from recommend_templates.Main.paserManager.weather import Weather
    # weather = Weather()
    # weather_list = weather.getWeather() #json.dumps(weather.getWeather(),ensure_ascii=False,encoding="utf-8") #unicode 转换为 utf-8
    # print(json.dumps(weather_list[0],ensure_ascii=False,encoding="utf-8"))
    # print(json.dumps(weather_list[1],ensure_ascii=False,encoding="utf-8"))
    data = {}
    data['user_name'] = request.session.get('user_name')
    today = {"temp_low": "14", "weather": "小雨", "weatid1": "", "humi_low": "0", "humi_high": "0", "temp_curr": "16",
             "temperature": "18℃/14℃", "cityid": "101270101", "windid": "20", "weaid": "265", "week": "星期五",
             "temperature_curr": "16℃", "weather_icon1": "", "winpid": "201", "weatid": "2", "weather_curr": "多云",
             "citynm": "成都", "cityno": "chengdu", "days": "2017-10-13", "humidity": "85%",
             "weather_icon": "http://api.k780.com/upload/weather/d/1.gif", "temp_high": "18", "winp": "1级",
             "wind": "北风"}
    seven_day = [
        {"week": "星期五", "weather_icon": "http://api.k780.com/upload/weather/d/7.gif", "humi_high": "0", "humi_low": "0",
         "temperature": "18℃/14℃", "weatid": "8", "temp_low": "14", "citynm": "成都", "cityno": "chengdu",
         "winpid": "125", "days": "2017-10-13", "humidity": "0%/0%", "cityid": "101270101",
         "weather_icon1": "http://api.k780.com/upload/weather/n/7.gif", "weather": "小雨", "temp_high": "18",
         "weatid1": "8", "windid": "124", "winp": "微风", "wind": "无持续风向", "weaid": "265"},
        {"week": "星期六", "weather_icon": "http://api.k780.com/upload/weather/d/7.gif", "humi_high": "0", "humi_low": "0",
         "temperature": "18℃/15℃", "weatid": "8", "temp_low": "15", "citynm": "成都", "cityno": "chengdu",
         "winpid": "125", "days": "2017-10-14", "humidity": "0%/0%", "cityid": "101270101",
         "weather_icon1": "http://api.k780.com/upload/weather/n/7.gif", "weather": "小雨", "temp_high": "18",
         "weatid1": "8", "windid": "124", "winp": "微风", "wind": "无持续风向", "weaid": "265"},
        {"week": "星期日", "weather_icon": "http://api.k780.com/upload/weather/d/7.gif", "humi_high": "0", "humi_low": "0",
         "temperature": "18℃/14℃", "weatid": "8", "temp_low": "14", "citynm": "成都", "cityno": "chengdu",
         "winpid": "125", "days": "2017-10-15", "humidity": "0%/0%", "cityid": "101270101",
         "weather_icon1": "http://api.k780.com/upload/weather/n/7.gif", "weather": "小雨", "temp_high": "18",
         "weatid1": "8", "windid": "124", "winp": "微风", "wind": "无持续风向", "weaid": "265"},
        {"week": "星期一", "weather_icon": "http://api.k780.com/upload/weather/d/7.gif", "humi_high": "0", "humi_low": "0",
         "temperature": "18℃/13℃", "weatid": "8", "temp_low": "13", "citynm": "成都", "cityno": "chengdu",
         "winpid": "125", "days": "2017-10-16", "humidity": "0%/0%", "cityid": "101270101",
         "weather_icon1": "http://api.k780.com/upload/weather/n/7.gif", "weather": "小雨", "temp_high": "18",
         "weatid1": "8", "windid": "124", "winp": "微风", "wind": "无持续风向", "weaid": "265"},
        {"week": "星期二", "weather_icon": "http://api.k780.com/upload/weather/d/7.gif", "humi_high": "0", "humi_low": "0",
         "temperature": "19℃/13℃", "weatid": "8", "temp_low": "13", "citynm": "成都", "cityno": "chengdu",
         "winpid": "125", "days": "2017-10-17", "humidity": "0%/0%", "cityid": "101270101",
         "weather_icon1": "http://api.k780.com/upload/weather/n/7.gif", "weather": "小雨", "temp_high": "19",
         "weatid1": "8", "windid": "124", "winp": "微风", "wind": "无持续风向", "weaid": "265"},
        {"week": "星期三", "weather_icon": "http://api.k780.com/upload/weather/d/7.gif", "humi_high": "0", "humi_low": "0",
         "temperature": "21℃/14℃", "weatid": "8", "temp_low": "14", "citynm": "成都", "cityno": "chengdu",
         "winpid": "125", "days": "2017-10-18", "humidity": "0%/0%", "cityid": "101270101",
         "weather_icon1": "http://api.k780.com/upload/weather/n/1.gif", "weather": "小雨转多云", "temp_high": "21",
         "weatid1": "2", "windid": "124", "winp": "微风", "wind": "无持续风向", "weaid": "265"},
        {"week": "星期四", "weather_icon": "http://api.k780.com/upload/weather/d/7.gif", "humi_high": "0", "humi_low": "0",
         "temperature": "27℃/19℃", "weatid": "8", "temp_low": "19", "citynm": "成都", "cityno": "chengdu",
         "winpid": "125", "days": "2017-10-19", "humidity": "0%/0%", "cityid": "101270101",
         "weather_icon1": "http://api.k780.com/upload/weather/n/7.gif", "weather": "小雨", "temp_high": "27",
         "weatid1": "8", "windid": "124", "winp": "微风", "wind": "无持续风向", "weaid": "265"}]
    if request.method == 'POST':
        # today = request.POST.get('today')
        # seven_day = request.POST.get('seven_day')
        weather = request.POST.get('weather')
        if weather == 'seven_day':
            return JsonResponse({'code': '7', 'weather_list': seven_day})  # weather_list[1]
    return render(request, 'weatherTest.html',
                  {'weather': today, 'user_name': request.session.get('user_name'), 'data': data})  # weather_list[0]


def login(request):
    data = {}
    if request.method == 'POST':
        userName = request.POST.get('user')
        pwd = request.POST.get('password')
        # if userName != '':
        #     if User.objects.filter(username=userName):
        #         data['code'] = '200'
        #         #return HttpResponse(json.dumps(data),content_type='application/json')
        #     else:
        #         data ['code'] = '404'
        #         #return HttpResponse(json.dumps(data), content_type='application/json')
        # else:
        #     data['isEmpty'] = '0'
        if userName != '' and pwd != '':
            if User.objects.filter(username=userName, password=str(pwd)):  # 如果用户名和密码不能对上号，就返回主页
                request.session['is_login'] = True
                request.session['user_name'] = userName
                # return index(request)
                data['correctCode'] = '1'
            else:
                data['errorCode'] = '0'
        else:
            data['emptyCode'] = '0'
        return JsonResponse(data)
    return render_to_response('loginTest.html')


def register(request):
    selectList = []
    if request.method == 'POST':
        user = request.POST.get('user')  # 标签里面的 name 属性
        pwd = request.POST.get('password')
        age = request.POST.get('age')
        email = request.POST.get('email')
        address = request.POST.get('address')

        select1 = request.POST.get('select1')
        select2 = request.POST.get('select2')
        select3 = request.POST.get('select3')
        select4 = request.POST.get('select4')
        selectList = [select1, select2, select3, select4]

        user1 = re.findall(r'^[A-Za-z]+[_A-Za-z0-9]*|^[1-9][0-9]{10,10}$', str(user))
        pwd1 = re.findall(r'^[_.#*@%&A-Za-z0-9]{6,20}$', str(pwd))
        email1 = re.findall(
            r'^[\w!#$%&\'*+/=?^_`{|}~-]+(?:\.[\w!#$%&\'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?$',
            str(email))
        age1 = re.findall(r'^[0-9]\d*$', str(age))

        isExist = User.objects.filter(username=user)
        code = {}
        if isExist:
            code['existCode'] = '200'
            # return HttpResponse('<script>alert("账号已存在")</script>')
        else:
            if user1 and pwd1:
                if email != '':
                    if not email1:
                        code['inputErrorCode'] = '404'
                        return JsonResponse(code)
                        # return HttpResponse('<script>alert("输入有误")</script>')
                if age != '':
                    if not age1:
                        code['inputErrorCode'] = '404'
                        return JsonResponse(code)
                        # return HttpResponse('<script>alert("输入有误")</script>')
                code['successCode'] = 'true'
                user = User(username=user, password=pwd, age=str(age), email=email, address=address,
                            user_love=selectList)
                user.save()
                # return render(request, 'loginTest.html')
            else:
                code['inputErrorCode'] = '404'
                # return HttpResponse('<script>alert("输入有误")</script>')
        return JsonResponse(code)
    return render_to_response('registerTest.html')
    #     if isExist:
    #         code['existCode'] = '200'
    #         return HttpResponse('<script>alert("账号已存在")</script>')
    #     else:
    #         if user1 and pwd1:
    #             if email != '':
    #                 if not email1:
    #                     code['inputErrorCode'] = '404'
    #                     return HttpResponse('<script>alert("输入有误")</script>')
    #             if age != '':
    #                 if not age1:
    #                     code['inputErrorCode'] = '404'
    #                     return HttpResponse('<script>alert("输入有误")</script>')
    #             user = User(username=user, password=pwd, age=str(age), email=email, address=address, user_love=selectList)
    #             user.save()
    #             return render(request, 'loginTest.html')
    #         else:
    #             code['inputErrorCode'] = '404'
    #             return HttpResponse('<script>alert("输入有误")</script>')
    # return render_to_response('registerTest.html')


def register_ajax(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('password')
        age = request.POST.get('age')
        email = request.POST.get('email')
        result = {}
        # print('账号：%s 密码：%s 年龄：%s 邮箱：%s' % (user, pwd, age, email))
        if pwd != '':
            if re.findall(r'^[_.#*@%&A-Za-z0-9]{6,20}$', str(pwd)):
                result['pCode'] = '200'
            else:
                result['p_msg'] = '密码包含特殊符号、或长度小于6'
                result['pCode'] = '404'
        else:
            result['pCodeEmpty'] = '0'

        if email != '':
            if re.findall(
                    r'^[\w!#$%&\'*+/=?^_`{|}~-]+(?:\.[\w!#$%&\'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?$',
                    str(email)):
                result['eCode'] = '200'
            else:
                result['e_msg'] = '邮箱格式不正确'
                result['eCode'] = '404'
        else:
            result['eCodeEmpty'] = '0'

        if age != '':
            if re.findall(r'^[0-9]\d*$', str(age)):
                result['aCode'] = '200'
            else:
                result['a_msg'] = '年龄必须是数字'
                result['aCode'] = '404'
        else:
            result['aCodeEmpty'] = '0'

        if user != '':
            if re.findall(r'^[A-Za-z]+[_A-Za-z0-9]*|^[1-9][0-9]{10,10}$', str(user)):
                result['uCode'] = '200'
                if User.objects.filter(username=user):
                    result['code'] = '200'
                    result['msg'] = '账号已经被使用了'
                else:
                    result['code'] = '404'
            else:
                result['u_msg'] = '账号必须是电话号码、或者字母开头的可包含数字和下划线的字符串'
                result['uCode'] = '404'
        else:
            result['uCodeEmpty'] = '0'

        return JsonResponse(result)


# 用户提交登出
def subLogout(request):
    # print "subLogout ......
    request.session['is_login'] = False
    request.session['user_name'] = None
    return index(request)
