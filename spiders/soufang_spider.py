# coding=utf-8
# !/usr/bin/python
import random
from scrapy.spiders import Spider
from scrapy import Request
from degreeroom.items import DegreeroomItem
from urllib.parse import quote_plus

class SoufangSpider(Spider):
    name = 'degreeroom'

    allowed_domains = ["esf.gz.fang.com"]

    #dest_schools=["市桥中心小学","市桥东城小学","市桥南阳里小学","市桥德兴小学","市桥北城小学"]
    dest_schools = ["市桥中心小学"]
    base_url = "http://esf.gz.fang.com/map/?mapmode=y&district=78&subwayline=&subwaystation=&price=0-170&room=&area=&towards=&floor=&hage=&equipment=&keyword=${keyword}&comarea=&orderby=16&isyouhui=&newCode=&houseNum=&schoolDist=&schoolid=&ecshop=&groupedmode=4&PageNo=${page}&zoom=16&a=ajaxSearch&city=gz&searchtype=&housetag=81";

    start_urls = []
    for i in dest_schools:
        keyword=quote_plus(str(i))
        for j in range(1, 10):
            start_urls.append(str(base_url).replace("${page}", str(j)).replace("${keyword}",keyword))

    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', self.user_agent_list[0])
        # 这句话用于随机选择user-agent
        ua = random.choice(self.user_agent_list)
        if ua:
            request.headers.setdefault('User-Agent', ua)

    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

    def parse(self, response):
        self.log('A response from %s just arrived!' % response.url)
        infos = response.xpath("//a/@href").extract()
        for i in infos:
            i_str = str(i)
            if "esf" in i_str:
                url = i_str.replace('\\', '').strip()
                yield Request(url=url.replace("\"", ""), callback=self.parse_details)

    def parse_details(self, response):
        item = DegreeroomItem()
        item['url'] = response.url
        item['title'] = response.xpath('//div[@class="title rel"]/text()').extract_first()
        item['total_price'] = response.xpath('//div[contains(@class,"price_esf")]//text()').extract_first()
        infos = response.xpath('//div[@class="tt"]/text()').extract()
        item['hu_xin'] = infos[0]
        item['mian_ji'] = infos[1].replace('平米','')
        item['unit_price'] = infos[2]
        item['chao_xiang'] = infos[3]
        item['lou_ceng'] = infos[4]
        item['zhuang_xiu'] = infos[5]
        item['hu_xin'] = infos[0]
        infos = response.xpath('//div[contains(@class ,"rcont")]//a/text()').extract()
        item['xiao_qu'] = infos[0]
        item['qu_yu'] = infos[2]+infos[3]
        if len(infos)>4:
            item['xue_xiao'] = infos[4]
        else :
            item['xue_xiao'] = ""
        infos = response.xpath('//div[@class="content-item fydes-item"]//div[@class="text-item clearfix"]/span[contains(@class ,"rcont")]/text()').extract()
        item['jianzu_year'] = infos[0]
        if len(infos)==6 :
            item['id'] = infos[4]
            item['publish_date'] = infos[5]
        else:
            item['id'] = infos[5]
            item['publish_date'] = infos[6]
        item['core_maidian']=response.xpath('//div[@class ="fyms_con floatl gray3"]/text()').extract_first()
        item['imgs']=response.xpath('//li[@class]/img[@class ="detailslideimg"]/@src').extract()
        yield item
