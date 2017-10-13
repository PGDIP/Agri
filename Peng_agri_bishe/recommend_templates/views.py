# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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
from recommend_templates.pager import  Pagination
from recommend_templates.Main.paserManager.newsContentPaser import paserWeather
from recommend_templates.models import *

ROOT_URL = os.getcwd()

# Create your views here.
# 主界面
def index(request, data={}):
    # data = {"user_name":"jeje","user_pwd":"jeje"}
    # return HttpResponse("Hello world！ This is my first trial. [Poll的笔记]")
    # return Http404
    user_name = request.session.get('user_name')
    data["user_name"] = user_name
    print(data["user_name"],'//////////////////////////////////////')
    return render(request, ROOT_URL + "/recommend_templates/templates/homepage.html", data)  # 注意路径一定要写对
def test(request):
	print ("class_1 ......")
	try:
		current_page = request.GET.get('p')
		user_name = request.session.get('user_name')
		rec_db = MongoOperator('localhost',27017,'AgriRecSys','news')
		db_ans = rec_db.find({"class_name":"病虫害"} )
		data={}
		ans_list = []
		count=0
		for i,news in enumerate(list(db_ans),0):
			ans_list.append( {
				"news": news,
				 "news_id": str(news["_id"]),

				#"href": "#href_id%d" % (i),
				#"content_id": "href_id%d" % (i),

				#"click_id": "ajax_id_%d" % (i),
				#"ajax_id": "#ajax_id_%d" % (i),
			} )
			count+=1
		page_obj = Pagination(count, current_page)
		data_list = ans_list[page_obj.start():page_obj.end()]
		data["user_name"] = user_name
	except: return index(request)
	return render(request, ROOT_URL +"/recommend_templates/templates/test.html",{'data':data_list,'page_obj':page_obj})
# 第一类新闻 农业新闻
def class_1(request, data={}):
    # print "class_1 ......"
    try:
        user_name = request.session.get('user_name')
        # rec_db = MongoOperator('localhost', 27017, 'AgriRecSys', 'news')
        # db_ans = rec_db.find({"class_name": "农业新闻"})
        db_ans = page.objects.filter(class_name='农业新闻')
        data = {}
        ans_list = []
        for i, news in enumerate(list(db_ans), 0):
            ans_list.append({
                "news": news,
                "news_id": str(news["_id"]),

                "href": "#href_id%d" % (i),
                "content_id": "href_id%d" % (i),

                "click_id": "ajax_id_%d" % (i),
                "ajax_id": "#ajax_id_%d" % (i),
            })
        data["news_list"] = ans_list
        data["user_name"] = user_name
    except:
        return index(request)
    return render(request, ROOT_URL + "/recommend_templates/templates/class_1.html", data)  # 注意路径一定要写对


# 第二类新闻 病虫害
def class_2(request):
    # print "class_2 ......"
    try:
        current_page = request.GET.get('p')
        user_name = request.session.get('user_name')
        # rec_db = MongoOperator('localhost', 27017, 'AgriRecSys', 'news')
        # db_ans = rec_db.find({"class_name": "病虫害"})
        db_ans = page.objects.filter(class_name = '水果病虫害防治')
        data = {}
        ans_list = []
        count = 0
        for i, news in enumerate(db_ans, 0):
            content = str(news.content['content0'])
            ans_list.append({
                "news": news,
                "news_id": news.id,
                'content': content

                # "href": "#href_id%d" % (i),
                # "content_id": "href_id%d" % (i),

                # "click_id": "ajax_id_%d" % (i),
                # "ajax_id": "#ajax_id_%d" % (i),
            })
            count += 1
        page_obj = Pagination(count, current_page)
        data_list = ans_list[page_obj.start():page_obj.end()]
        data["user_name"] = user_name
    except:
        return index(request)
    return render(request, ROOT_URL + "/recommend_templates/templates/class_2.html", {'data': data_list, 'page_obj': page_obj})


def news(request,data={}):
	return render(request,ROOT_URL+"/recommend_templates/templates/news.html",data)


# 第三类新闻  种植技术
def class_3(request):
    # print "class_3 ......"
    try:

        current_page = request.GET.get('p')
        user_name = request.session.get('user_name')
        #rec_db = MongoOperator('localhost', 27017, 'AgriRecSys', 'news')
        #db_ans = rec_db.find({"class_name": "果蔬种植"})
        db_ans = page.objects.filter(class_name='蔬菜种植技术')
        data = {}
        ans_list = []
        count = 0
        for i, news in enumerate(db_ans, 0):
            content = str(news.content['content0'])
            ans_list.append({
                'content':content,
                "news": news,
                "news_id": news.id,

                # "href": "#href_id%d" % (i),
                # "content_id": "href_id%d" % (i),

                # "click_id": "ajax_id_%d" % (i),
                # "ajax_id": "#ajax_id_%d" % (i),
            })
            count += 1
        page_obj = Pagination(count, current_page)
        data_list = ans_list[page_obj.start():page_obj.end()]
        data["user_name"] = user_name
    except:
        return index(request)
    return render(request, ROOT_URL + "/recommend_templates/templates/class_3.html",{'data': data_list, 'page_obj': page_obj})


# 第四类新闻  市场价格
def class_4(request, data={}):
    # print "class_4 ......"
    try:
        user_name = request.session.get('user_name')
        rec_db = MongoOperator('localhost', 27017, 'AgriRecSys', 'news')
        db_ans = rec_db.find({"class_name": "市场价格"})
        data = {}
        ans_list = []
        for i, news in enumerate(list(db_ans), 0):
            ans_list.append({
                "news": news,
                "news_id": str(news["_id"]),

                "href": "#href_id%d" % (i),
                "content_id": "href_id%d" % (i),

                "click_id": "ajax_id_%d" % (i),
                "ajax_id": "#ajax_id_%d" % (i),
            })
        data["news_list"] = ans_list
        data["user_name"] = user_name
    except:
        return index(request)
    return render(request, ROOT_URL + "/recommend_templates/templates/class_4.html", data)  # 注意路径一定要写对


# 第五类新闻  科技新闻
def class_5(request, data={}):
    # print "class_5 ......"
    try:
        current_page = request.GET.get('p')
        user_name = request.session.get('user_name')
        #rec_db = MongoOperator('localhost', 27017, 'AgriRecSys', 'news')
        #db_ans = rec_db.find({"class_name": "政策法规"})
        db_ans=page.objects.filter(class_name='科技要闻')
        data = {}
        ans_list = []
        count = 0
        for i, news in enumerate(list(db_ans), 0):
            content=str(news.content['content0'])
            ans_list.append({
                "content":content,
                "news": news,
                "news_id": str(news["_id"]),

                # "href": "#href_id%d" % (i),
                # "content_id": "href_id%d" % (i),

                # "click_id": "ajax_id_%d" % (i),
                # "ajax_id": "#ajax_id_%d" % (i),
            })
            count += 1
        page_obj = Pagination(count, current_page)
        data_list = ans_list[page_obj.start():page_obj.end()]
        data["user_name"] = user_name
    except:
        return index(request)
    return render(request, ROOT_URL + "/recommend_templates/templates/class_2.html",{'data': data_list, 'page_obj': page_obj})


def myRecommend(request, data={}):
    # print "myRecommend ......"
    user_name = request.session.get('user_name')
    try:
        rec_db = MongoOperator('localhost', 27017, 'AgriRecSys', 'user')
        db_ans = rec_db.find({"user_name": user_name})[0]
        new_id_list = db_ans.get("looked_list")
        if new_id_list == None:  # 面对冷启动问题
            pass  #
        else:
            # print "========*****#######*********"
            rec_new_id_list = get_K_nearst_love(8, new_id_list)  # 推荐5个最优新闻名称给用户
        # print "========**************",new_id_list
        ans_list = []
        for i, news_id in enumerate(rec_new_id_list, 0):
            rec_db = MongoOperator('localhost', 27017, 'AgriRecSys', 'news')
            db_ans = rec_db.find({"_id": ObjectId(news_id)})
            if db_ans.count() == 0: continue;
            db_ans = db_ans[0]
            ans_list.append({
                "news": db_ans,
                "news_id": str(db_ans["_id"]),

                "href": "#href_id%d" % (i),
                "content_id": "href_id%d" % (i),

                "click_id": "ajax_id_%d" % (i),
                "ajax_id": "#ajax_id_%d" % (i),
            })
        data["user_name"] = user_name
        data["news_list"] = ans_list
    except:
        return index(request)
    return render(request, ROOT_URL + "/recommend_templates/templates/myRecommend.html", data)  # 注意路径一定要写对


def history(request):
    # print "history ......"
    data = {}
    user_name = request.session.get('user_name')
    try:
        rec_db = MongoOperator('localhost', 27017, 'AgriRecSys', 'user')
        db_ans = rec_db.find({"user_name": user_name})[0]
        new_id_list = db_ans.get("looked_list")
        ans_list = []
        for i, news_id in enumerate(new_id_list, 0):
            rec_d = MongoOperator('localhost', 27017, 'AgriRecSys', 'news')
            db_ans = rec_d.find({'_id': ObjectId(news_id)})
            if db_ans.count() == 0:
                continue
            db_ans = db_ans[0]
            ans_list.append({
                "news": db_ans,
                "news_id": str(db_ans["_id"]),

                "href": "#href_id%d" % (i),
                "content_id": "href_id%d" % (i),

                "click_id": "ajax_id_%d" % (i),
                "ajax_id": "#ajax_id_%d" % (i),
            })
        data["user_name"] = user_name
        data["news_list"] = ans_list
    except:
        return index(request)
    return render(request, ROOT_URL + "/recommend_templates/templates/history.html", data)  # 注意路径一定要写对


# 获取用户对某一个新闻的点击 ajax技术
def count_click_times(request):
    # print "count_click_times ...... "
    if request.POST:
        news_id = request.POST.get('news_id')
        user_name = request.POST.get('user_name')
    else:
        news_id = request.GET.get('news_id')
        user_name = request.GET.get('user_name')
    try:
        rec_db = MongoOperator('localhost', 27017, 'AgriRecSys', 'user')
        db_ans = rec_db.find({"user_name": user_name})[0]
        if db_ans.get("looked_list") is None:
            looked_list = set([news_id])
        else:
            looked_list = set(list(db_ans["looked_list"]))
            looked_list = looked_list | set([news_id])
        # print news_id, user_name
        rec_db.update(
            {'user_name': user_name},
            {'$set': {"looked_list": list(looked_list)}},
        )
    except:
        return index(request)


def shift_title_bar(request):
    # print "shift_title_bar ...... "
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


##############################################################################################################################################

def login(request):
    response_data = {}
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('password')
        try:
            if User.objects.filter(username=user,password=str(pwd)):  # 如果用户名和密码不能对上号，就返回主页
                request.session['is_login'] = True
                request.session['user_name'] = user
                response_data["user_name"] = user
                return index(request, response_data)
            else:
                return index(request)
        except:
            return index(request)
    return render_to_response('loginTest.html')

def login_ajax(request):
    if request.method == 'POST':
        userName = request.POST.get('user')
        if User.objects.filter(username=userName):
            data = {
                'code':'200'
            }
            return JsonResponse(data)
            #return HttpResponse(json.dumps(data),content_type='application/json')
        else:
            data = {
                'code': '404'
            }
            return JsonResponse(data)
            #return HttpResponse(json.dumps(data), content_type='application/json')

def register(request):
    selectList = []
    if request.method == 'POST':
        user = request.POST.get('user')  #标签里面的 name 属性
        pwd = request.POST.get('password')
        age = request.POST.get('age')
        email = request.POST.get('email')
        address = request.POST.get('address')

        select1 = request.POST.get('select1')
        select2 = request.POST.get('select2')
        select3 = request.POST.get('select3')
        select4 = request.POST.get('select4')
        selectList =[select1,select2,select3,select4]

        user1 = re.findall(r'^[A-Za-z]+[_A-Za-z0-9]*|^[1-9][0-9]{10,10}$', str(user))
        pwd1 = re.findall(r'^[_.#*@%&A-Za-z0-9]{6,20}$',str(pwd))
        email1 = re.findall(r'^[\w!#$%&\'*+/=?^_`{|}~-]+(?:\.[\w!#$%&\'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?$',str(email))
        age1 = re.findall(r'^[0-9]\d*$',str(age))
        isExist = User.objects.filter(username=user)

        if (not user1 or not pwd1 or not email1 or not age1) and (email1 != '' or age1 != ''):
            return HttpResponse('alert(输入有误)')
        else:
            if isExist:
                return HttpResponse('账号已存在')
            else:
                user = User(username=user,password = pwd,age=str(age),email=email,address=address,user_love=selectList)
                user.save()
                return render(request, 'loginTest.html')
    return render_to_response('registerTest.html')

def register_ajax(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('password')
        age = request.POST.get('age')
        email = request.POST.get('email')
        result = {}
        #print('账号：%s 密码：%s 年龄：%s 邮箱：%s' % (user, pwd, age, email))
        if pwd != '':
            if re.findall(r'^[_.#*@%&A-Za-z0-9]{6,20}$',str(pwd)):
                result['pCode'] = '200'
            else:
                result['p_msg'] = '密码包含特殊符号、或长度小于6'
                result['pCode'] = '404'
        else:
            result['pCodeEmpty'] = '0'

        if email != '':
            if re.findall(r'^[\w!#$%&\'*+/=?^_`{|}~-]+(?:\.[\w!#$%&\'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?$',str(email)):
                result['eCode'] = '200'
            else:
                result['e_msg'] = '邮箱格式不正确'
                result['eCode'] = '404'
        else:
            result['eCodeEmpty'] = '0'

        if age != '':
            if re.findall(r'^[0-9]\d*$',str(age)):
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

def articles(request,pageId):
    article = page.objects.get(pageId = pageId)
    article = page.objects.all()

