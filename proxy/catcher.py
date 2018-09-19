import base64
import binascii
import json
import random
import re
import time
from concurrent.futures import ThreadPoolExecutor

import redis
import requests
from lxml import etree
import schedule

from config import base, user_agents

redisDB = redis.Redis(host=base.REDIS['host'], port=base.REDIS['port'], password=base.REDIS['password'], db=base.REDIS['database'])
executor = ThreadPoolExecutor(max_workers=10)
proxy_ready = base.PROXY['ready']

#http://www.gatherproxy.com/
def gatherproxy():
    print("catch_gatherproxy")
    header = {'User-Agent': random.choice(user_agents.agents)}
    proxies = {'http': '127.0.0.1:1080'}
    url = 'http://www.gatherproxy.com/'
    response = requests.get(url, headers=header, proxies=proxies).content
    html = etree.HTML(response)
    result = html.xpath("//script[@type='text/javascript']/text()")
    iter = re.finditer('gp.insertPrx\((.*?)\);\\\\r', str(result))
    for i in iter:
        jsonStr = i.group(1).strip()
        jsonObject = json.loads(jsonStr)
        ip = jsonObject["PROXY_IP"]
        port = int(jsonObject["PROXY_PORT"], 16)
        redisDB.sadd("proxy_input", ip+":"+str(port))
    time.sleep(random.randint(46, 78))

#https://free-proxy-list.net/
#https://www.us-proxy.org/
#https://free-proxy-list.net/uk-proxy.html
#https://free-proxy-list.net/anonymous-proxy.html
#https://www.sslproxies.org/
def freeproxy():
    print("catch_freeproxy")
    header = {'User-Agent': random.choice(user_agents.agents)}
    proxies = {'https': '127.0.0.1:1080'}
    urls = ["https://free-proxy-list.net/", "https://www.us-proxy.org/", "https://free-proxy-list.net/uk-proxy.html",
            "https://free-proxy-list.net/anonymous-proxy.html", "https://www.sslproxies.org/"]
    for url in urls:
        response = requests.get(url, headers=header, proxies=proxies).content
        html = etree.HTML(response)
        result = html.xpath("//table[@id='proxylisttable']/tbody/tr")
        for tr in result:
            ip = tr.xpath('.//td[1]/text()')[0] + ":" + tr.xpath('.//td[2]/text()')[0]
            redisDB.sadd("proxy_input", ip)

#https://www.my-proxy.com/
def myproxy():
    print("catch_myproxy")
    header = {'User-Agent': random.choice(user_agents.agents)}
    proxies = {'https': '127.0.0.1:1080'}
    for i in range(1,11):
        time.sleep(2)
        url = "https://www.my-proxy.com/free-proxy-list-" + str(i) + ".html"
        response = requests.get(url, headers=header, proxies=proxies).content
        html = etree.HTML(response)
        result = html.xpath('//div[@class="list"]/text()')
        for each in result:
            ip = str(each).split('#')[0]
            redisDB.sadd("proxy_input", ip)

#https://www.rmccurdy.com/scripts/proxy/good.txt
def rmccurdy():
    print("catch rmccurdy")
    header = {'User-Agent': random.choice(user_agents.agents)}
    time.sleep(2)
    url = "https://www.rmccurdy.com/scripts/proxy/good.txt"
    response = requests.get(url, headers=header).content.decode('utf-8')
    ips = response.split('\n')
    ips = ips[0:-2]
    for ip in ips:
        redisDB.sadd("proxy_input", ip)

#https://www.cool-proxy.net/
def cool_proxy():
    print("catch cool_proxy")
    header = {'User-Agent': random.choice(user_agents.agents)}
    proxies = {'https': '127.0.0.1:1080'}
    response = requests.get("https://www.cool-proxy.net/proxies/http_proxy_list", headers=header, proxies=proxies).content
    html = etree.HTML(response)
    pages = html.xpath('//table/tr[last()]/th/span/a/text()').pop(-2)
    pattern = re.compile(r'document\.write\(Base64\.decode\(str_rot13\(\"(.*)\"\)\)\)')
    for i in range(1, int(pages)+1):
        time.sleep(2)
        url = "https://www.cool-proxy.net/proxies/http_proxy_list/page:" + str(i)
        response = requests.get(url, headers=header, proxies=proxies).content
        html = etree.HTML(response)
        trs = html.xpath('//table/tr')
        trs = trs[1:6] + trs[7:-1]
        for tr in trs:
            match = pattern.match(tr.xpath('./td[1]/script/text()')[0])
            port = tr.xpath('./td[2]/text()')[0]
            if match:
                code_list = list(match.group(1))
                for index in range(len(code_list)):
                    i = code_list[index]
                    if i.isalpha():
                        if i.lower() < 'n':
                            i = chr(ord(i) + 13)
                            code_list[index] = i
                        else:
                            i = chr(ord(i) - 13)
                            code_list[index] = i

                ip_base64_str = "".join(code_list)
                ip = base64.b64decode(ip_base64_str).decode()
                redisDB.sadd("proxy_input", ip+":"+port)

#http://cn-proxy.com/
#http://cn-proxy.com/archives/218
def cn_proxy():
    print("catch cn_proxy")
    header = {'User-Agent': random.choice(user_agents.agents)}
    proxies = {'http': '127.0.0.1:1080'}
    urls = ["http://cn-proxy.com/", "http://cn-proxy.com/archives/218"]
    for url in urls:
        time.sleep(2)
        response = requests.get(url, headers=header,proxies=proxies).content
        html = etree.HTML(response)
        result = html.xpath('//table[@class="sortable"]/tbody/tr')
        for each in result:
            ip = each.xpath('./td[1]/text()')[0]
            port = each.xpath('./td[2]/text()')[0]
            redisDB.sadd("proxy_input", ip + ":" + port)

#http://www.xroxy.com/proxylist.php?port=&type=All_http&ssl=&country=&latency=&reliability=#table
def xroxy():
    print("catch xroxy")
    header = {'User-Agent': random.choice(user_agents.agents)}
    proxies = {'http': '127.0.0.1:1080'}
    response = requests.get("http://www.xroxy.com/proxylist.php?port=&type=All_http&ssl=&country=&latency=&reliability=#table", headers=header, proxies=proxies).content
    html = etree.HTML(response)
    page = int(int(html.xpath('//tr/td/small/b/text()')[0])/10)
    for i in range(0,page):
        time.sleep(2)
        url = "http://www.xroxy.com/proxylist.php?port=&type=All_http&ssl=&country=&latency=&reliability=&sort=reliability&desc=true&pnum=" + str(i) + "#table"
        response = requests.get(url, headers=header, proxies=proxies).content
        html = etree.HTML(response)
        trs = html.xpath('//table[@cellpadding="3"]/tr[starts-with(@class, "row")]')
        for each in trs:
            ip = each.xpath('./td[2]/a/text()')[0].replace('"', "").strip()
            port = each.xpath('./td[3]/a/text()')[0]
            redisDB.sadd("proxy_input", ip + ":" + port)

#https://proxy-list.org/english/index.php?p=1
def proxy_list():
    print("proxy_list")
    header = {'User-Agent': random.choice(user_agents.agents)}
    proxies = {'https': '127.0.0.1:1080'}
    keyList = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=")
    pattern = re.compile(r'Proxy\(\'(.*)\'\)')
    for i in range(1, 11):
        time.sleep(2)
        url = "https://proxy-list.org/english/index.php?p=" + str(i)
        response = requests.get(url, headers=header, proxies=proxies).content
        html = etree.HTML(response)
        decodes = html.xpath('//li[@class="proxy"]/script/text()')
        for decode in decodes:
            match = pattern.match(decode)
            if match:
                decode = match.group(1)
                target = list(decode)
                t = ""
                f = 0
                while (f < len(target)):
                    s = keyList.index(target[f])
                    f += 1
                    o = keyList.index(target[f])
                    f += 1
                    u = keyList.index(target[f])
                    f += 1
                    a = keyList.index(target[f])
                    f += 1
                    n = s << 2 | o >> 4
                    r = (o & 15) << 4 | u >> 2
                    i = (u & 3) << 6 | a
                    t = t + chr(n)
                    if (u != 64):
                        t = t + chr(r)
                    if (a != 64):
                        t = t + chr(i)
                redisDB.sadd("proxy_input", t)

#http://proxydb.net/?protocol=http&min_uptime=75&max_response_time=5&country=CN&offset=15
def proxydb():
    print("catch xroxy")
    header = {'User-Agent': random.choice(user_agents.agents)}
    pattern1 = re.compile(r".*\'(.*)\'\.split.*")
    pattern2 = re.compile(r".*\((\d+) \- \(\[\]\+\[\]\).*")
    pattern3 = re.compile(r".*atob\(\'(.*)\'\.replace.*")
    pattern4 = re.compile(r".*div style=\"display:none\" data-[a-z]+=\"(\d+)\".*")
    for i in range(0, 10):
        time.sleep(1)
        url = "http://proxydb.net/?protocol=http&min_uptime=75&max_response_time=15&country=CN&offset=" + str(i * 15)
        random_proxy = redisDB.srandmember(proxy_ready, 1)[0].decode('utf8')
        proxies = {'http': random_proxy}
        response = requests.get(url, headers=header, proxies=proxies).content
        html = etree.HTML(response)
        scripts = html.xpath('//td/script/text()')
        match4 = pattern4.match(str(response))
        for script in scripts:
            script = script.replace('\n', '')
            match1 = pattern1.match(script)
            match2 = pattern2.match(script)
            match3 = pattern3.match(script)
            if match1 and match2 and match3 and match4:
                list1 = list(match1.group(1))
                list1.reverse()
                code = base64.b64decode(binascii.a2b_hex(match3.group(1).replace("\\x", "")))
                ip = "".join(list1) + code.decode('utf8')
                port = int(match2.group(1)) + int(match4.group(1))
                redisDB.sadd("proxy_input", ip + ":" + str(port))

def xici():
    print("catch xroxy")
    header = {'User-Agent': random.choice(user_agents.agents)}
    response = requests.get("http://www.xicidaili.com/", headers=header).content
    html = etree.HTML(response)
    trs = html.xpath('//tr')
    for tr in trs:
        if(len(tr.xpath('./td[@class="country"]')) != 0):
            if(tr.xpath('./td[6]/text()')[0] == "socks4/5"):
                continue
            ip = tr.xpath('./td[2]/text()')[0]
            port = tr.xpath('./td[3]/text()')[0]
            redisDB.sadd("proxy_input", ip + ":" + port)

def handle(funcName):
    try:
        executor.submit(eval(funcName))
    except Exception as e:
        print(e)

def start():
    schedule.every(2).minutes.do(handle, "gatherproxy")
    schedule.every(10).minutes.do(handle, "freeproxy")
    schedule.every(3).hours.do(handle, "myproxy")
    schedule.every(1).days.do(handle, "rmccurdy")
    schedule.every(15).minutes.do(handle, "cool_proxy")
    schedule.every(12).hours.do(handle, "cn_proxy")
    schedule.every(1).hours.do(handle, "xroxy")
    schedule.every(45).minutes.do(handle, "proxy_list")
    schedule.every(2).hours.do(handle, "proxydb")
    schedule.every(11).minutes.do(handle, "xici")

    while True:
        schedule.run_pending()
        time.sleep(2)

if __name__ == '__main__':
    xici()