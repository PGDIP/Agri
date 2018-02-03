from urllib import request
from urllib import error
import re
import time
# import chardet #自动获取网页编码方式  pip install chardet
import multiprocessing
from selenium import webdriver
from recommend_templates.models import price
import os
from multiprocessing import Pool


class Price():
    def __init__(self,ROOT_PATH):
        self.ROOT_PATH = ROOT_PATH

    def setHeaders(self):
        head = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Proxy-Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235',
            'Referer': 'http://www.3w3n.com/user/price4Day/goIndex',
            'Cookie': self.getCookie()[1],
            'Host': 'www.3w3n.com',
        }
        return head

    def getHtml(self,typeId):
        url = 'http://www.3w3n.com/user/price4Day/showPriceListPage?&typeId=' + str(typeId) + '&province=%E5%9B%9B%E5%B7%9D%E7%9C%81&r=' + self.getCookie()[0]
        pattern = re.compile(r'<div style="width:100%;height:100px;line-height: 100px;text-align: center;">暂无数据</div>',re.S)
        req = request.Request(url, headers=self.setHeaders())
        try:
            response = request.urlopen(req)  #
            html = response.read().decode('utf-8', 'ignore')
            result = re.findall(pattern, html)
            if result:
                print('暂没数据')
                time.sleep(10)
            else:
                self.getData(html)
                time.sleep(10)
        except error.HTTPError as e:
            print(e.code)
        except error.URLError as e:
            print(e.reason)

    def getData(self,html):
        pattern = re.compile(r'<tr>.*?</tr>', re.S)
        pattern_item = re.compile(r'<div.*?>(.*?)</div>', re.S)
        pattern_add = re.compile(r'<a title="查看详情".*?>(.*?)</a>', re.S)
        tr = re.findall(pattern, html)
        for td in tr[1:]:
            isHave = re.findall(pattern_item, td)
            # print(isHave)
            if isHave != None:
                name = isHave[0].strip()
                average = isHave[1].strip().replace('&nbsp', '').replace(';', '')
                market = re.findall(pattern_add, isHave[2])[0]
                date_create = isHave[4].strip()
                # 和数据库中的数据对比
                all_data = price.objects.filter(name=name, market=market, average=average, date=date_create)
                # print(type(all_data))
                data = price.objects.filter(name=name, market=market)
                if all_data:
                    print('>>>>数据已经存在<<<<')
                    continue
                else:
                    if data:
                        one_item = price.objects.get(name=name, market=market)
                        pro_date = one_item.date
                        week_price = one_item.week_price
                        # print(date,average)

                        now_time = int(time.time())  # 当前时间的时间戳

                        # 上次更新数据库里面的时间
                        timeArray = time.strptime(pro_date, "%Y-%m-%d")
                        pro_time = int(time.mktime(timeArray))

                        # 当前数据的时间戳
                        timeArray1 = time.strptime(date_create, "%Y-%m-%d")
                        data_time = int(time.mktime(timeArray1))

                        if (now_time - pro_time) >= (now_time - data_time):
                            print('.....数据更新中')
                            if week_price:
                                price.objects.filter(name=name, market=market).update(average=average, date=date_create,week_price='')
                            else:
                                price.objects.filter(name=name, market=market).update(average=average, date=date_create)
                        else:
                            print('时间超前了......')
                            continue
                            # continue
                    else:
                        print('正在保存数据.......')
                        cate = price(name=name, market=market, average=average, date=date_create, week_price='')
                        cate.save()
            else:
                print('暂时没数据')

    def getCookie_value(self,url):
        driver = webdriver.Chrome()
        # driver.maximize_window()  #屏幕最大化
        driver.get(url)
        source = driver.page_source
        pattern = re.compile(r'<body value="(.*?)">', re.S)
        value = re.findall(pattern, source)[0].strip()

        # get the session cookie
        cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
        # print cookie
        cookiestr = ';'.join(item for item in cookie)
        li = [value + '/n', cookiestr + '/n']
        with open(self.ROOT_PATH+r'/io/cookie.txt', 'w', encoding='utf-8') as f:
            f.writelines(li)

        time.sleep(5)
        driver.quit()

    def getCookie(self):
        list = []
        with open(self.ROOT_PATH+r'/io/cookie.txt', 'r', encoding='utf-8') as f:
            for item in f.readlines():
                list.append(item.strip())
        return list

    def main_price(self):
        cookie_url = 'http://www.3w3n.com/user/price4Day/goIndex'
        self.getCookie_value(cookie_url)
        cpu = multiprocessing.cpu_count()
        pool = Pool(processes=cpu)  # 建立进程池
        pool.map(self.getHtml, (typeId for typeId in range(1,2001)))  # 映射到主函数中进行循环
        print('价格采集完毕...............')


if __name__ == '__main__':
    ROOT_PATH = os.getcwd()
    price = Price(ROOT_PATH[:-13])
    price.main_price()
