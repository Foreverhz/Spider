
# coding:utf-8
# import StringIO,gzip
import base64
import urllib2

import re
from lxml import etree

class EnterDesk(object):
    def __init__(self):
        self.base_url = "https://mm.enterdesk.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "X - Requested - With": "XMLHttpRequest"
        }
        self.image_header={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        }

    def send_request(self, url, headers=None):
        try:
            request = urllib2.Request(url,headers=self.image_header)
            response = urllib2.urlopen(request)
            # print(response.headers)
            result = response.read()
            # if response.headers.get('Content-Encoding') == 'gzip':
            #     deal_result = self.deal_gzip(result)
            #     return deal_result
            # else:
            return result
        except Exception as e:
            print('[Log]:到尽头了，别撸了' + str(e))


    def parse_list(self,html):
        html = etree.HTML(html)
        image_list = html.xpath('//div[@class="chapterlist_box"]//a/@href')
        url_list = image_list[0:-5]
        return url_list

    def parse_image_list(self,url):
        real_url =[]
        chapter_count = 0
        for i in url:
            chapter_count += 1
            response = self.send_request(i)
            patterns = re.compile(r'"src":"(.*?)",')
            result = patterns.findall(response)
            chapter_url = self.get_real_image_url(result)
            self.save_image(chapter_url, chapter_count)
        return real_url

    def get_real_image_url(self,url):
        real_url = []
        for parse_url in url:
            real_url.append(base64.b64decode(parse_url))
        return real_url

    def save_image(self, image_list, count):
        i = 0
        for image in image_list:

            i+=1
            with open(u"./有妖气/{}-{}.jpg".format(count,i),"wb") as f:
                print(str(count) + '-' + str(i))
                result = self.send_request(image,self.image_header)
                f.write(result)

    # def deal_gzip(self,data):
    #     compresseddata = data
    #     compressedstream = StringIO.StringIO(compresseddata)
    #     gzipper = gzip.GzipFile(fileobj=compressedstream)
    #     result = gzipper.read()
    #     return result

    def main(self):
        url = "http://www.u17.com/comic/3166.html"
        html = self.send_request(url)
        # print html
        url_list = self.parse_list(html)
        self.parse_image_list(url_list)

if __name__ == '__main__':
    enterdesk = EnterDesk()
    enterdesk.main()
