#coding:utf-8


import requests
import urllib
import time
import random
from hashlib import md5

from jsonpath import jsonpath


def get_sign():

    s1 = "fanyideskweb"
    s4 = "6x(ZHw]mwzX#u0V7@yfwK"

    i = raw_input("请输入需要翻译的文本:")
    t = str(int((time.time() * 1000 + random.randint(0, 10))))

    sign = md5(s1 + i + t + s4).hexdigest()

    return (i, t, sign)


def send_request():
    post_url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
    headers = {
        "Accept" : "application/json, text/javascript, */*; q=0.01",
        # requests模块和scrapy框架，都支持gzip解压缩
        "Accept-Encoding" : "gzip, deflate",
        "Accept-Language" : "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection" : "keep-alive",
        "Content-Length" : "218",
        "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie" : "_ntes_nnid=f77d53cb936304b5333b304b767a4958,1506087321856; OUTFOX_SEARCH_USER_ID_NCOO=971893961.4325761; OUTFOX_SEARCH_USER_ID=-1480774266@10.169.0.83; JSESSIONID=aaaVQyExswcsSf-RWwMxw; ___rl__test__cookies=1537170672377",
        "Host" : "fanyi.youdao.com",
        "Origin" : "http://fanyi.youdao.com",
        "Referer" : "http://fanyi.youdao.com/",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "X-Requested-With" : "XMLHttpRequest"
    }

    i, salt, sign = get_sign()

    formdata = {"i" : i,
    "from" : "AUTO",
    "to" : "AUTO",
    "smartresult" : "dict",
    "client" : "fanyideskweb",
    "salt" : salt,
    "sign" : sign,
    "doctype" : "json",
    "version" : "2.1",
    "keyfrom" : "fanyi.web",
    "action" : "FY_BY_CLICKBUTTION",
    "typoResult" : "false"}


    headers['Content-Length'] = str(len(urllib.urlencode(formdata)))

    python_obj = requests.post(post_url, headers =headers, data=formdata).json()
    result = jsonpath(python_obj, "$..tgt")[0]
    print(result)

if __name__ == "__main__":
    send_request()
