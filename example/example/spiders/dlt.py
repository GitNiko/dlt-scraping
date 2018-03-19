#coding=utf-8
import scrapy
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest
from ..items import DLTItem, DLTType


def genJS(jsStr):
    """
    var lottery_nums='大乐透|18018|06,08,13,24,28,06,12|2018-02-10|4,824,492,674.96|1~七星彩|18018|3,2,5,9,9,5,8|2018-02-11|1,000,000|2~22选5|13172|08,09,14,15,19|2013-06-28||3~31选7|10118|03,06,10,19,20,24,30,28|2010-10-09||4~排列3|18042|5,3,7|2018-02-11||5~排列5|18042|5,3,7,6,9|2018-02-11|250,970,124.66|6~';show_new();
    :param jsStr:
    :return:
    """
    # [n.split("|")[:5] for n in jsStr.split("var lottery_nums='")[1:][0].split("~")[:-1]]
    return list(map(lambda x: x.split("|")[:5], jsStr.split("var lottery_nums='")[1:][0].split("~")[:-1]))

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

# 暂时用不到复杂的方式
# class DLTSpider(scrapy.Spider):
#     name = "dlt"
#
#     def start_requests(self):
#         urls = [
#             # 'http://www.sporttery.cn/digitallottery/',
#             'http://info.sporttery.cn/interface/lottery_num.php?action=new',
#         ]
#         for url in urls:
#             yield  SplashRequest(url, self.parse, args={'wait': 0.5})
#
#     def parse(self, response):
#         # page = response.xpath('/html/body/div[4]/div[1]/div[1]/table/tbody/tr[2]/td[1]/text()').extract()
#         # print('------', page)
#         # print('page', response.body)
#         yield {
#             'dlt': '1'
#         }
#
#     def getDlt(self, response):
#         pass
#         quotes = {
#             name: '/html/body/div[4]/div[1]/div[1]/table/tbody/tr[2]/td[1]/span/text()',
#             round: '/html/body/div[4]/div[1]/div[1]/table/tbody/tr[2]/td[1]/text()',
#             code: '',
#             total: '/html/body/div[4]/div[1]/div[1]/table/tbody/tr[2]/td[2]/div[4]/text()',
#             date: '/html/body/div[4]/div[1]/div[1]/table/tbody/tr[2]/td[2]/div[1]/text()',
#         }
#         item = DLTItem()
#
#         for key, value in quotes.items():
#             item.__setattr__(key, response.xpath(value).extract_first())

# 简单的获取
class TinyDLTSpider(scrapy.Spider):
    name = "tiny_dlt"
    start_urls = [
        'http://info.sporttery.cn/interface/lottery_num.php?action=new',
    ]

    def parse(self, response):
        js = response.body.decode(encoding='gb2312', errors='strict')
        print('js', js)
        datas = genJS(js)
        print('datas', datas)
        mapping = {
                '大乐透': DLTType.Dlt.value,
                '七星彩': DLTType.Qxc.value,
                '22选5': DLTType.X5.value,
                '31选7': DLTType.X7.value,
                '排列3': DLTType.P3.value,
                '排列5': DLTType.P5.value
        }
        for cate in datas:
            item = DLTItem()
            item['name'] = cate[0]
            item['type'] = mapping[cate[0]]
            item['round'] = cate[1]
            item['code'] = cate[2]
            item['date'] = cate[3]
            item['total'] = cate[4]
            yield  item
            # print('item', item)