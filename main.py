import requests
import time
import random
from lxml import etree

# get ip address
def get_ip(url, n=10): # 默认获取前 10 页数据
    with open('ip.txt', 'w') as f:

        for i in range(1,10):
            print(url+str(i))
            html_text = requests.get(url+str(i)).text
            #print(html_text)
            html = etree.HTML(html_text)
            # 每一页的整块 ip
            all_ip = html.xpath('//td[@data-title="IP"]')
            for each_ip in all_ip:
                print(each_ip.text)
                f.write(each_ip.text+'\n')
            # 反反爬虫
            time.sleep(5)

# 检查ip的可用性
def useful_ip():
    ip = []
    with open('ip.txt', 'r') as f:
        all_ip = f.readlines()
        for each_ip in all_ip:
            each_ip = each_ip.rstrip()
            ip.append(each_ip)

    # 将可用 ip 写入 useful_ip.txt
    with open('useful_ip.txt', 'w') as f:
        for each_ip in ip:
            proxies = {'http': 'http://{proxy}'.format(proxy=each_ip)}
            try:
                # 超过 10s 就不用该 ip
                r = requests.get('http://www.baidu.com', proxies=proxies, timeout=10, verify=False)
                if r.status_code == 200:
                    f.write(str(each_ip)+'\n')
            except Exception as e:
                print('time out')

def access(address):
    header = {'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, sdch',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              }
    with open('useful_ip.txt', 'r') as f:
        all_ip = f.readlines()
        for each_ip in all_ip:
            each_ip = each_ip.rstrip()
            proxies = {'http': 'http://{proxy}'.format(proxy=each_ip)}
            print(each_ip)
            html = requests.get(address, headers = header, proxies=proxies, timeout=20).text
            #print(html)
            time.sleep(random.randint(1, 10))

if __name__=='__main__':
    url = 'http://www.kuaidaili.com/free/inha/'
    address = 'https://www.maimemo.com/share/page/?uid=1512656&pid=uid'
    get_ip(url, 10)
    useful_ip()
    access(address)