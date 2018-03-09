# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DegreeroomItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url =  scrapy.Field()
    title = scrapy.Field()
    total_price = scrapy.Field()
    hu_xin = scrapy.Field()
    mian_ji = scrapy.Field()
    unit_price = scrapy.Field()
    chao_xiang = scrapy.Field()
    lou_ceng = scrapy.Field()
    zhuang_xiu = scrapy.Field()
    hu_xin = scrapy.Field()
    xiao_qu = scrapy.Field()
    qu_yu = scrapy.Field()
    xue_xiao = scrapy.Field()
    jianzu_year = scrapy.Field()
    id = scrapy.Field()
    publish_date = scrapy.Field()
    core_maidian = scrapy.Field()
    imgs = scrapy.Field()
