# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy import log
from .items import DLTItem
from .settings import MYSQL_DBNAME, MYSQL_HOST, MYSQL_PASSWD, MYSQL_USER

class ExamplePipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=MYSQL_HOST,
            db=MYSQL_DBNAME,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if DLTItem == item.__class__:
            try:
                self.cursor.execute(
                    """
                    SELECT * from t_lottery_info WHERE lotteryRound = %s AND lotteryType = %s
                    """,
                    (item['round'], item['type'])
                )
                ret = self.cursor.fetchone()
                if ret:
                    log.msg('开奖信息已经存在了,跳过')
                else:
                    log.msg('开奖信息插入')
                    self.cursor.execute(
                        """
                        INSERT INTO t_lottery_info(lotteryName, lotteryType, lotteryRound, lotteryCode, lotteryTotal, lotteryOpenDate)
                        VALUE (%s, %s, %s, %s, %s, %s)
                        """,
                        (
                            item['name'],
                            item['type'],
                            item['round'],
                            item['code'],
                            item['total'],
                            item['date']
                        )
                    )
                self.connect.commit()
            except Exception as error:
                log.msg(error)
        return item
