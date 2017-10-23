import random
import requests
import re



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
        print(ipList)
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
        pool.map(self.Ip, List)  # 映射到主函数中进行循环
        print('..........代理ip提取完成...........')


if __name__ == '__main__':
    # ci = CorrectIp()
    # ci.getCorrectIp()
    from recommend_templates.Main.main import ROOT_PATH
    with open(ROOT_PATH[:-12] + r'io\correctIp.txt', 'r') as f:
        ipList = f.read()
        print(ipList.split(','))
    print(len(ipList.split(',')))

