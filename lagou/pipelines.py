# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from lagou.items import LagouItem
import csv
import pymysql
class LagouPipeline(object):
    def __init__(self):
        self.lagou_fp = open('拉钩大数据招聘.csv',mode='a',encoding='utf-8',newline='')
        self.lagou_writer = csv.writer(self.lagou_fp)
        self.headers = ['positionName','city','district','linestaion','companyFullName','companyShortName','industryField',
                      'financeStage','positionAdvantage','companyLabelList',
                      'education','salary','workYear','lastLogin','companySize','skillLables']
        self.lagou_writer.writerow(self.headers)
    def process_item(self, item, spider):
        #判断字段为空则不再写入
        if isinstance(item,LagouItem):
            self.lagou_writer.writerow(dict(item).values())
        return item


class MysqlPipeline(object):
    def __init__(self):
        #连接mysql数据库
        #user：用户名；password：密码；db：写你要插入数据的数据库；
        self.connect = pymysql.connect(host='localhost', user='root', password='写自己的密码', db='spider', port=3306,charset='utf8')
        self.cursor = self.connect.cursor()
    def process_item(self,item,spider):
        #往数据库写入数据
        try:
            if isinstance(item,LagouItem):
                self.cursor.execute('insert into lagou_dashuju values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                                    [item['positionName'],item['city'],item['district'],item['linestaion'],item['companyFullName'],item['companyShortName'],
                                     item['industryField'],item['financeStage'],item['positionAdvantage'],item['companyLabelList'],item['education'],
                                     item['salary'],item['workYear'],item['lastLogin'],item['companySize'],item['skillLables']])

            self.connect.commit()  # mysql增删改查后需要 提交事务
            return item
        except:
            print('数据库保存数据出错！！！')

    def close_spider(self,spider):
        self.cursor.close()
        self.connect.close()
        print('数据已成功写入Mysql！')


