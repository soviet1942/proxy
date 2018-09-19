import os
import sys
from multiprocessing import Process

import checker
import catcher

dir_path = os.path.dirname(__file__)
sys.path.append(dir_path)

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/proxy/<path:num>')
def getProxy(num):
    return str(checker.get_proxy(num))

@app.route('/proxy/check')
def check_start():
    checker.start()
    return "测试开启"

@app.route('/proxy/current')
def check_current():
    return checker.getValidProxyNum()

@app.route('/proxy/loadIpsFile')
def check_load():
    checker.loadIpsFromFile()
    return "ip文件装载成功"

@app.route('/proxy/catch')
def check_catch():
    catcher.start()
    return "抓取开启"

@app.route('/proxy/start')
def start():
    checker.start()
    catcher.start()
    return "抓取检测全部开启"

if __name__ == '__main__':
    app.run()