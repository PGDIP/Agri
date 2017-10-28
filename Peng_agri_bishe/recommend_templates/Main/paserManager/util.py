from urllib import error, request
from  lxml import etree  # 整理html
from selenium import webdriver
import time
import re
from bs4 import BeautifulSoup
from PIL import Image, ImageFile
from io import BytesIO
import random
import requests
import os


# 数据获取（不整理html）
class HttpUtil():
    def __init__(self, url, headers, code):
        self.url = url
        self.headers = headers
        self.code = code
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

    def getHtml(self, url, timeout, num_retries, proxy=None):  ##给函数一个默认参数proxy为空
        if proxy == None:  ##当代理为空时，不使用代理获取response（别忘了response啥哦！之前说过了！！）
            try:
                headers = self.headers
                headers['User-Agent'] = random.choice(self.user_agent_list)
                response = requests.get(url, headers={'User-Agent': 0}, timeout=timeout)  ##这样服务器就会以为我们是真的浏览器了
                response.encoding = self.code
                html = response.text
                return html
            except:  ##如过上面的代码执行报错则执行下面的代码
                if num_retries > 0:  ##num_retries是我们限定的重试次数
                    time.sleep(5)  ##延迟十秒
                    print(u'获取网页出错，5s后将获取倒数第：', num_retries, u'次')
                    return self.getHtml(url, timeout, num_retries - 1)  ##调用自身 并将次数减1
                else:
                    print(u'开始使用代理')
                    ci = CorrectIp()
                    time.sleep(5)
                    if len(ci.proxyIp()) <= 1:
                        print('可用代理 ip 为空，正在重新获取')
                        ci.getProxyIp()
                    ip = ''.join(str(random.choice(ci.proxyIp())).strip())  ##下面有解释哦
                    proxy = {'http': ip}
                    return self.getHtml(url, 3, 6, proxy)  ##代理不为空的时候

        else:  ##当代理不为空
            try:
                headers = self.headers
                headers['User-Agent'] = random.choice(self.user_agent_list)
                response = requests.get(url, headers=headers, proxies=proxy, timeout=timeout)  ##使用代理获取response
                response.encoding = self.code
                html = response.text
                return html
            except:
                if num_retries > 0:
                    time.sleep(5)
                    ipList = CorrectIp().proxyIp()
                    ip = ''.join(str(random.choice(ipList)).strip())  ##下面有解释哦
                    proxy = {'http': ip}
                    print(u'正在更换代理，5s后将重新获取倒数第', num_retries, u'次')
                    print(u'当前代理是：', proxy)
                    return self.getHtml(url, timeout, num_retries - 1, proxy)
                else:
                    print(u'代理也不好使了！取消代理,  100s 后开始')
                    time.sleep(100)
                    return self.getHtml(url, 3, 6)

    def webDriver(self):
        #  不整理..........
        driver = webdriver.Chrome()
        driver.get(self.url)
        source = driver.page_source
        # get the session cookie
        cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
        # print cookie
        cookiestr = ';'.join(item for item in cookie)
        time.sleep(5)
        driver.quit()  # 关闭浏览器
        return cookiestr + '\n' + source

    def getData(self, html, key, flag):
        if flag == 1:
            result = re.findall(key, html)
        if flag == 2:
            soup = BeautifulSoup(html, 'lxml')
            result = soup.find_all(key)
        return result

    def saveImg(self, imageURL, fileName):
        # array = np.asarray(image)  # 将image 转换成numpy数组
        # print(image.format, image.size, image.mode)
        # image.show()
        # ImageFile.LOAD_TRUNCATED_IMAGES = True  # OSError: image file is truncated
        # response = requests.get(imageURL, headers=self.headers)
        # image = Image.open(BytesIO(response.content))
        # image.save(imagePath)
        try:
            img = requests.get(imageURL)
            rootPath = r'D:\image_Article\\'
            self.mkDir(rootPath)  # 创建目录
            imagePath = rootPath + fileName
            try:
                with open(imagePath, 'ab') as f:
                    f.write(img.content)
                    # f = open(imagePath, 'ab')  # 解决不能识别图像文件 ？？
                    # f.write(img.content)
                    # f.close()
            except:
                return None
            path = 'image_Article\\' + fileName
            return path
        except:
            return None

    def mkDir(self, rootPath):
        path = rootPath.strip()
        path = path.strip('\\')
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            print('{} 目录创建成功'.format(path))


class CorrectIp():
    def __init__(self):
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        self.baseUrlList = ['http://www.xicidaili.com/nt/', 'http://www.xicidaili.com/nn/',
                            'http://www.xicidaili.com/wn/', 'http://www.xicidaili.com/wt/']
        self.ipList = []

    # def getProxyIp(self):
    #     headers = {
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #         'Accept-Encoding': 'gzip, deflate',
    #         'Accept-Language': 'zh-CN,zh;q=0.9',
    #         'Upgrade-Insecure-Requests': '1',
    #         'Connection': 'keep-alive',
    #         'Host': 'www.goubanjia.com',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
    #         'Referer': 'http://www.goubanjia.com/',
    #         'Cookie': 'UM_distinctid=15f49ec60ab27-0d067d232c68e-5b4a2c1d-100200-15f49ec60ac1f8; JSESSIONID=AB5E98C8BEA481A6089B79D7C2752D44; CNZZDATA1253707717=435162388-1508773334-null%7C1508827880; Hm_lvt_2e4ebee39b2c69a3920a396b87bbb8cc=1508773749,1508815637,1508827881,1508832505; Hm_lpvt_2e4ebee39b2c69a3920a396b87bbb8cc=1508832905'
    #     }
    #     ipList = []
    #     urlList = []
    #     from recommend_templates.Main.paserManager.util import HttpUtil
    #     util = HttpUtil('http://www.goubanjia.com',headers=headers , code='utf-8')
    #     for url in self.baseUrlList:
    #         for index in range(1,5):
    #             urlList.append(url+str(index)+'.shtml')
    #
    #     def getOnePageIp(url):
    #         import time
    #         from bs4 import BeautifulSoup
    #         from recommend_templates.Main.paserManager.tools.replaceTool import Tool
    #         response = util.getHtml(url,3,3)
    #         tdIpList = BeautifulSoup(response,'lxml').find('div',id='list').find_all('td',class_ = 'ip')
    #         tool = Tool()
    #         for ip in tdIpList:
    #             print(ip)
    #             pattern = re.compile(r':|<span.*?>(.*?)</span>|<div.*?>(.*?)</div>',re.S)
    #             ip_ = []
    #             for ip in re.findall(pattern , str(ip)):
    #                 print(ip)
    #                 if ip[0] != '':
    #                     ip_.append(ip[0])
    #                 elif ip[1] != '':
    #                     ip_.append(ip[1])
    #                 else:
    #                     continue
    #             ipList.append(ip_[0])
    #         time.sleep(3)
    #         print(ipList)
    #     getOnePageIp('http://www.goubanjia.com/free/index1.shtml')
    #
    #     # threads = []
    #     # for i in range(len(urlList)):
    #     #     import threading
    #     #     thread = threading.Thread(target=getOnePageIp, name='...线程:....' + str(i), args=(urlList[i],))
    #     #     threads.append(thread)
    #     #     thread.start()
    #     # # 阻塞主进程，等待所有子线程结束
    #     # for thread in threads:
    #     #     thread.join()
    #     return ipList

    def getOnePageIp(self, url):
        import time
        from bs4 import BeautifulSoup
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWZhNTM3NTY0MGY4MGJhODgxMGVmMGRkM2MxYjJkOTU0BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMVl2LzNETGVKdGxYSDFDRmxmRlhSQmNRUXArd284eVFnZ3RWQkxuNnRubHc9BjsARg%3D%3D--18824704847b9c417b2707ad0ef92effbcad8f20; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1508748051,1508772712,1508815900,1508946118; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1508946275',
            'Host': 'www.xicidaili.com',
            'If-None-Match': 'W/"38cc9bff2b346d4a3b5fc348587d90a9"',
            'Referer': 'http://www.xicidaili.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': random.choice(self.user_agent_list)
        }
        util = HttpUtil(url,headers,'utf-8')
        response = util.getHtml(url,3,6)
        tbody = BeautifulSoup(response, 'lxml').find('table', id='ip_list')
        pattern = re.compile(r'<img.*?/>.*?</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>', re.S)
        ip_pro = re.findall(pattern, str(tbody))
        for ip in ip_pro:
            self.ipList.append(ip[0] + ':' + ip[1])
        self.getCorrectIp(self.ipList)
        time.sleep(3)

    def add_Threading(self, url):
        import os
        import threading
        print('......正在获取代理ip......')
        print('......主进程：.....', os.getpid())
        urlList = []
        for index in range(1, 5):
            urlList.append(url + str(index))
        threads = []
        for i in range(len(urlList)):
            thread = threading.Thread(target=self.getOnePageIp, name='...线程:....' + str(i), args=(urlList[i],))
            threads.append(thread)
            thread.start()
        # 阻塞主进程，等待所有子线程结束
        for thread in threads:
            thread.join()

    def getProxyIp(self):
        import multiprocessing
        from multiprocessing import Pool
        cpu = multiprocessing.cpu_count()
        pool = Pool(processes=cpu)  # 建立进程池
        pool.map(self.add_Threading, self.baseUrlList)  # 映射到主函数中进行循环

    def Ip(self, proxy):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.gengzhongbang.com',
            'Referer': 'https://www.baidu.com/link?url=TdtRy_RwYTTH1xVm1JWrX6N0YtG4DLBBEVVx69kmFNcEB9No-kySt6EPcNKdqUzF&wd=&eqid=e7f0f2410000192a0000000359f17f6d',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': random.choice(self.user_agent_list)
        }
        url = 'http://www.gengzhongbang.com/'  # "http://www.ip138.com"
        try:
            res = requests.get(url, headers=headers, proxies={'http': proxy}, timeout=3)
            if res.status_code == 200:
                print('.......可用ip.......', proxy)
                from recommend_templates.Main.main import ROOT_PATH
                with open(ROOT_PATH[:-12] + r'io\correctIp.txt', 'a+') as f:
                    f.writelines(proxy + ' , ')
        except Exception as e:
            print(e)
        time.sleep(3)

    def getCorrectIp(self, urlList):
        print('..........正在提取可用的 ip.........')
        threads = []
        for i in range(len(urlList)):
            import threading
            thread = threading.Thread(target=self.Ip, name='...线程:....' + str(i), args=(urlList[i],))
            threads.append(thread)
            thread.start()
        # 阻塞主进程，等待所有子线程结束
        for thread in threads:
            thread.join()
        print('..........代理ip提取完成...........')

    def proxyIp(self):
        from recommend_templates.Main.main import ROOT_PATH
        with open(ROOT_PATH[:-12] + r'io\correctIp.txt', 'r') as f:
            ipList = f.read()
        return ipList.split(',')

# class download:
#     def __init__(self):
#         pass
#
#     def get(self, url, timeout, proxy=None, num_retries=6):  ##给函数一个默认参数proxy为空
#         print(u'开始获取：', url)
#         UA = random.choice(user_agent_list)  ##从self.user_agent_list中随机取出一个字符串
#         headers = {'User-Agent': UA}  ##构造成一个完整的User-Agent （UA代表的是上面随机取出来的字符串哦）
#         if proxy == None:  ##当代理为空时，不使用代理获取response（别忘了response啥哦！之前说过了！！）
#             try:
#                 return requests.get(url, headers=headers, timeout=timeout)  ##这样服务器就会以为我们是真的浏览器了
#             except:  ##如过上面的代码执行报错则执行下面的代码
#                 if num_retries > 0:  ##num_retries是我们限定的重试次数
#                     time.sleep(5)  ##延迟十秒
#                     print(u'获取网页出错，5S后将获取倒数第：', num_retries, u'次')
#                     return self.get(url, timeout, num_retries - 1)  ##调用自身 并将次数减1
#                 else:
#                     print(u'开始使用代理')
#                     time.sleep(5)
#                     IP = ''.join(str(random.choice(getProxyIp)).strip())  ##下面有解释哦
#                     proxy = {'http': IP}
#                     return self.get(url, timeout, proxy, )  ##代理不为空的时候
#
#         else:  ##当代理不为空
#             try:
#                 IP = ''.join(str(random.choice(getProxyIp)).strip())  ##将从self.iplist中获取的字符串处理成我们需要的格式（处理了些什么自己看哦，这是基础呢）
#                 proxy = {'http': IP}  ##构造成一个代理
#                 return requests.get(url, headers=headers, proxies=proxy, timeout=timeout)  ##使用代理获取response
#             except:
#
#                 if num_retries > 0:
#                     time.sleep(5)
#                     IP = ''.join(str(random.choice(getProxyIp)).strip())
#                     proxy = {'http': IP}
#                     print(u'正在更换代理，10S后将重新获取倒数第', num_retries, u'次')
#                     print(u'当前代理是：', proxy)
#                     return self.get(url, timeout, proxy, num_retries - 1)
#                 else:
#                     print(u'代理也不好使了！取消代理')
#                     return self.get(url, 3)
#
#
#                     # Xz = download()  ##实例化w
#                     # response = Xz.get("http://www.mzitu.com/", 3).text ##打印headers
#                     # print(response)
