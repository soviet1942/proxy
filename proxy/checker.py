'''
Created on 2017年10月20日

@author: Administrator
'''
import asyncio
import json
import random
import re
import time
from multiprocessing import Process

import redis
import aiohttp
from config import base, user_agents

BATCH_TEST_SIZE = 50
input = base.PROXY['producer']
output = base.PROXY['consumer']
redisDB = redis.Redis(host=base.REDIS['host'], port=base.REDIS['port'], password=base.REDIS['password'], db=base.REDIS['database'])
agents = user_agents.agents
websites_entrys = base.WEBSITES
websites_keys = list(base.WEBSITES.keys())

async def test_single_proxy(proxy):
    conn = aiohttp.TCPConnector(verify_ssl=False)
    async with aiohttp.ClientSession(connector=conn) as session:
        try:
            if isinstance(proxy, bytes):
                proxy = proxy.decode('utf-8')
            real_proxy = 'http://' + proxy
            headers = {
                'User-Agent': random.choice(agents),
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Referer': proxy
            }
            url = random.choice(websites_keys)
            async with session.get(url=url, proxy=real_proxy, timeout=5, headers=headers) as response:
                html = await response.text()
                if str(html).find(websites_entrys.get(url)) > 0:
                    print(proxy + " says: yeap! feels good man ^_^  ^_^  ^_^  ^_^  ^_^")
                    score = redisDB.zscore(output, proxy)
                    if score == None or redisDB.zscore(output, proxy) < 100:
                        redisDB.zincrby(output, proxy, 1)
                    return
                else:
                    print(proxy + "'s holder suck!!! website:" + url)
                    redisDB.zincrby(output, proxy, -1)
                    return
        except:
            print(proxy + " says: timeout! feels sad man T_T")
            score = redisDB.zscore(output, proxy)
            if(score == None):
                print(proxy + ": first blood, feels really really sad man")
                redisDB.srem(input, proxy)
            elif score > 30:
                redisDB.zincrby(output, proxy, -10)
            elif score > 10 and score <= 30:
                redisDB.zincrby(output, proxy, -6)
            elif score > 3 and score <= 10:
                redisDB.zincrby(output, proxy, -2)
            else:
                redisDB.zincrby(output, proxy, -1)


def runTask():
    while True:
        proxies = list(redisDB.smembers(input))
        loop = asyncio.new_event_loop()
        for i in range(0, len(proxies), BATCH_TEST_SIZE):
            test_proxies = proxies[i:i + BATCH_TEST_SIZE]
            tasks = [test_single_proxy(proxy) for proxy in test_proxies]
            loop.run_until_complete(asyncio.wait(tasks))
            time.sleep(5)
        cleanTrash()
        left = redisDB.zcard(output)
        time.sleep(int(10000/left))
        gen_proxy_ready()


def loadIpsFromFile():
    with open("config/proxies.txt") as f:
        ips = f.readlines()
        for temp in ips:
            ip = temp[:-1]
            redisDB.sadd(input, ip)


def cleanTrash():
    list = redisDB.zrangebyscore(output, "-inf", -1)
    for each in list:
        redisDB.zrem(output, each.decode('utf-8'))
        redisDB.srem(input, each.decode('utf-8'))

def getValidProxyNum():
    all = str(redisDB.zcard(output))
    available = str(len(redisDB.zrangebyscore(output, "1", "+inf")))
    return "总共："+all+"条ip， 当前可用："+available+"条ip"

def gen_proxy_ready():
    redisDB.delete("proxy_ready")
    list = redisDB.zrangebyscore(output, "8", "+inf")
    redisDB.zrange
    for ip in list:
        redisDB.sadd("proxy_ready", ip)

def get_proxy(num):
    proxy_set = redisDB.smembers("proxy_ready")
    proxy_list = []
    for ip in proxy_set:
        proxy_list.append(ip.decode('utf-8'))
    return proxy_list[0:int(num)]

def start():
    gen_proxy_ready()
    p = Process(target=runTask)
    p.start()

