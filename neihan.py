# _*_ coding: utf-8 _*_
# @File : neihan.py
# @Author : Xa_ier
# @time : 18-9-10 下午8:39
import re
import requests

class NeihanSpider(object):

    def __init__(self):
        self.base_url = "https://www.neihan8.com/article/list_5_"
        self.headers =  {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        # 设置自增页数
        self.page = 1
        # 匹配页面指定的数据，将通过findall()方法提取
        self.patterns_page = re.compile(r'<div class="f18 mb20">(.*?)</div>',re.S)
        # 匹配页面特定的数据，将通过 sub() 方法替换
        # <.*?> 表示无用标签，如 <p> </p> <br> 等
        # &.*?; 表示无用的html实体字符， 如&nbsp; 等
        # \s 表示空白字符，如 空格、\n、\t 等q（但不包括中文全角空格）
        # 　 即 u"\u3000".encode("utf-8")， 表示 中文全角空格
        self.patterns_content = re.compile(r"<.*?>|&.*?;|\s|　")

    def send_request(self,url):
        print ("[INFO]:正在发送请求 [{}] <{}>".format("GET",url))
        html = requests.get(url,headers = self.headers).content
        utf8_html = html.decode("gbk").encode("utf-8")

        return utf8_html

    def parse_page(self,html):

        content_list = self.patterns_page.findall(html)
        return content_list

    def write_content(self,content_list):
        print ("[INFO]:正在写入数据 ")

        with open("neihan.txt","a") as f:
            f.write("第{}页:\n".format(self.page))

            for content in content_list:
                result = self.patterns_content.sub("",content)
                f.write(result)
                f.write("\n")
            f.write("\n\n")


    def main(self):
        while True:
            full_url = self.base_url + str(self.page) + ".html"
            html = self.send_request(full_url)
            content_list = self.parse_page(html)
            self.write_content(content_list)
            self.page  += 1

            if raw_input("按下回车继续抓取（按Ｑ退出）:").upper() == "Q":
                break
        print ("[INFO]:谢谢使用，再见！")



if __name__ == '__main__':
    spider = NeihanSpider()
    spider.main()