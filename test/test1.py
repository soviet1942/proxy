import json
import re
import requests
from lxml import etree

if __name__ == '__main__':
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }
    proxies = {
        'http': '127.0.0.1:1080'
    }
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
        print(ip)
        print(port)
