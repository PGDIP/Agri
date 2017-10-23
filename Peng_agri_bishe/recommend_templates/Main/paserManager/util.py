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

    def getUserAgent(self):
        user_agent_list = [
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
        return random.choice(user_agent_list)

    def getHtml(self, url, timeout, num_retries, proxy=None):  ##给函数一个默认参数proxy为空
        if proxy == None:  ##当代理为空时，不使用代理获取response（别忘了response啥哦！之前说过了！！）
            try:
                headers = self.headers
                headers['User-Agent'] = self.getUserAgent()
                response = requests.get(url, headers= {'User-Agent':0}, timeout=timeout)  ##这样服务器就会以为我们是真的浏览器了
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
                    correctIp = CorrectIp()
                    time.sleep(5)
                    if len(correctIp.proxyIp()) <= 1:
                        print('可用代理 ip 为空，正在重新获取')
                        correctIp.getCorrectIp()
                    ip = ''.join(str(random.choice(correctIp.proxyIp())).strip())  ##下面有解释哦
                    proxy = {'http': ip}
                    return self.getHtml(url, 3, 6, proxy)  ##代理不为空的时候

        else:  ##当代理不为空
            try:
                headers = self.headers
                headers['User-Agent'] = self.getUserAgent()
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
                    print(u'代理也不好使了！取消代理')
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

class CorrectIp(): #代理ip获取及验证
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

    def getProxyIp(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://www.baidu.com/link?url=8EVV_CMht2u93RVzpkoQyVXTOmyvIZuS77hh7boZfrNMnE0nuaJyK4RVEYYA0JCI&wd=&eqid=8e36fcf6000165470000000359ec54d5',
            'User-Agent': random.choice(self.user_agent_list)
        }
        ipList = []
        response = requests.get('http://www.xicidaili.com/nt/', headers=headers).text
        pattern = re.compile(r'<td class="country"><img src=.*?/></td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?', re.S)
        List = re.findall(pattern, response)
        for item in List:
            ipList.append('http://' + item[0] + ':' + item[1])
        return ipList

    def Ip(self,proxy):
        headers = {
            'Host':'ip.chinaz.com',
            'User-Agent': random.choice(self.user_agent_list)
            }
        url = "http://ip.chinaz.com/getip.aspx"
        import os
        print('......主进程：.....',os.getpid())
        try:
            res = requests.get(url, headers = headers , proxies={'http': proxy} , timeout = 3)
            if res.status_code == '200':
                print(proxy)
                from recommend_templates.Main.main import ROOT_PATH
                with open(ROOT_PATH[:-12] + r'io\correctIp.txt', 'a+') as f:
                    f.writelines(proxy + ' , ')
        except Exception as e:
            print(e)

    def getCorrectIp(self):
        print('..........正在提取可用的 ip.........')
        List = ['http://113.93.225.94:9797', 'http://222.174.168.102:53281', 'http://49.73.236.172:3128', 'http://121.35.243.157:8080', 'http://218.56.132.154:8080', 'http://122.72.18.34:80', 'http://61.160.208.222:8080', 'http://122.72.18.35:80', 'http://124.232.148.7:3128', 'http://106.4.64.5:3128', 'http://122.224.227.202:3128', 'http://122.72.18.61:80', 'http://121.43.178.58:3128', 'http://118.113.146.4:8888', 'http://180.168.179.193:8080', 'http://211.103.208.244:80', 'http://218.56.132.156:8080', 'http://115.196.190.17:8118', 'http://119.90.63.3:3128', 'http://218.56.132.157:8080', 'http://59.32.155.235:9000', 'http://61.152.230.26:8080', 'http://183.54.246.179:9000', 'http://218.56.132.155:8080', 'http://139.129.166.68:3128', 'http://222.212.185.3:8888', 'http://124.119.27.98:53281', 'http://27.46.20.81:888', 'http://119.163.133.93:8118', 'http://121.13.159.164:9999', 'http://115.233.210.218:808', 'http://119.90.248.245:9999', 'http://180.140.160.224:9797', 'http://223.199.191.59:808', 'http://60.191.134.165:9999', 'http://180.173.52.202:53281', 'http://112.250.65.222:53281', 'http://61.134.25.106:3128', 'http://221.206.5.183:53281', 'http://113.66.158.221:9797', 'http://113.87.161.176:808', 'http://58.17.125.215:53281', 'http://222.86.191.44:8080', 'http://121.63.209.247:9999', 'http://114.98.7.180:9000', 'http://27.44.174.66:9999', 'http://182.88.199.87:9797', 'http://220.248.207.105:53281', 'http://110.16.80.106:8080', 'http://113.89.54.241:9999', 'http://218.62.90.30:53281', 'http://175.9.247.1:53281', 'http://111.192.237.220:9797', 'http://101.81.106.155:9797', 'http://123.138.89.133:9999', 'http://61.163.39.70:9999', 'http://110.189.153.33:53281', 'http://218.28.58.150:53281', 'http://218.6.145.11:9797', 'http://219.131.180.4:9797', 'http://113.77.241.17:9000', 'http://113.78.255.32:9000', 'http://125.125.212.145:80', 'http://58.60.33.242:9797', 'http://202.105.111.193:9000', 'http://219.156.151.20:53281', 'http://202.38.92.100:3128', 'http://59.78.47.184:8123', 'http://113.110.247.199:3128', 'http://113.66.236.193:9797', 'http://113.66.158.251:9797', 'http://1.81.102.173:8118', 'http://119.121.110.93:9797', 'http://119.123.176.43:9000', 'http://27.46.42.145:9797', 'http://115.193.100.252:9797', 'http://119.122.215.179:9000', 'http://175.171.179.160:53281', 'http://183.54.30.87:9000', 'http://180.173.67.83:9797', 'http://175.147.123.164:80', 'http://1.196.118.122:9000', 'http://58.59.172.224:9797', 'http://58.59.172.134:9797', 'http://124.89.33.75:9999', 'http://113.89.15.93:9999', 'http://27.42.158.68:9797', 'http://27.42.159.147:9797', 'http://110.52.8.213:53281', 'http://112.95.190.125:9999', 'http://125.40.25.102:9999', 'http://163.125.238.226:9797', 'http://163.125.198.140:9797', 'http://222.186.45.60:62222']
        import multiprocessing
        from multiprocessing import Pool
        cpu = multiprocessing.cpu_count()
        pool = Pool(processes=cpu)  # 建立进程池
        pool.map(self.Ip, List)  # 映射到主函数中进行循环  self.getProxyIp()
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

