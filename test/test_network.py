import json
import re

import requests
from bs4 import BeautifulSoup
from pip._vendor.html5lib.treebuilders import etree

from config import base

if __name__ == '__main__':
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }
    proxies = {
        'http': '46.101.7.242:80'
    }
    url = 'http://www.eastmoney.com/'
    response = requests.get(url, headers=header, proxies=proxies).content
    print(response)
    if(str(response).find(base.WEBSITES.get(url)) > 0):
        print(base.WEBSITES.get(url))
        print("yes")
    else:
        print("damn")

