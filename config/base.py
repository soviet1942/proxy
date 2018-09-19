'''
基础配置文件
'''

REDIS = {
    'host' : 'localhost',
    'port' : 6379,
    'user' : 'root',
    'password' : '123456',
    'database' : 2,
}

MONGO = {
    'host' : 'localhost',
    'port' : 27017,
    'user' : "root",
    'password' : '123456',
    'database' : 'proxyIps',
}

POOL = {
    'pool_size' : 100,
}

PROXY = {
    'producer' : 'proxy_input',
    'consumer' : 'proxy_output',
    'ready' : 'proxy_ready'
}

WEBSITES = {
    'http://www.baidu.com/' : 'baidu',
    'http://www.sohu.com/' : 'sohu',
    'http://www.163.com/' : '163.com',
    'http://www.ly.com/' : 'ly.com',
    'http://www.douban.com/' : 'douban',
    'http://www.eastmoney.com/' : 'eastmoney',
    'http://www.qidian.com' : 'qidian',
    'http://www.hupu.com' : 'hupu',
    'http://kankan.eastday.com/' : 'eastday',
    'http://www.autohome.com.cn/beijing/cheshi/' : 'autohome',
    'http://beijing.bitauto.com/' : 'bitauto',
    'http://www.qunar.com/' : 'qunar',
    'http://cn.chinadaily.com.cn/' : 'chinadaily',
    'http://www.zol.com.cn/' : 'zol',
    'http://www.lagou.com/' : 'lagou',
    'http://focus.tianya.cn/' : 'tianya',
    'http://www.51job.com/' : '51job',
    'http://www.zhaopin.com/' : 'zhaopin',
    'http://www.onlinedown.net/' : 'onlinedown'
}
