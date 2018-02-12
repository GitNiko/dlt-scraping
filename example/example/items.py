# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from enum import Enum, unique


class ExampleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DLTItem(scrapy.Item):
    name = scrapy.Field()
    type = scrapy.Field()
    round = scrapy.Field() # 期数
    code = scrapy.Field() # 开奖号码
    total = scrapy.Field() # 奖金池
    date = scrapy.Field() # 开奖时间

@unique
class DLTType(Enum):
    Dlt = 1 # 超级大乐透
    Qxc = 2 # 七星彩
    P3 = 3 # 排列三
    P5 = 4 # 排列五
    X5 = 5 # 22选5
    X7 = 6 # 31选7
