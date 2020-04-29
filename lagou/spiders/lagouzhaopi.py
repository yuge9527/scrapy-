# -*- coding: utf-8 -*-
#Time:2020/03/27
#author:渔戈
'''
在此，特别感谢拉钩，我们只是对拉钩网进行爬虫学习。若有侵犯拉钩权益，请马上联系删除
仅供学习使用，不得作商业用途
'''
import scrapy
import json
import time
from lagou.items import LagouItem
class LagouSpider(scrapy.Spider):
    name = 'lagouzhaopi'
    allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/']

    def start_requests(self):
        #获取这个链接的cookies:
        url = 'https://www.lagou.com/jobs/list_%E5%A4%A7%E6%95%B0%E6%8D%AE/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput='
        yield scrapy.Request(url=url,callback=self.detail_urls)


    #这个函数用于处理cookie格式，提取出符合要求的cookies信息
    def stringToDict(self,cookie):
        itemDict = {}
        items = cookie.replace(':','=').split(',')
        for item in items:
            key = item.split('=')[0].replace(' ', '').strip(" [ b ' "  )
            value = item.split('=')[1].strip(' Max-Age ; Path Version "')
            itemDict[key] = value
        return itemDict

    def detail_urls(self,response):
        try:
            urls = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
            for i in range(1,200):#控制爬取的页数
                print("正在请求第{}页的数据，请稍等。。。".format(i))
                time.sleep(10)
                if i == 1:
                    data={
                        'first':'true',
                        'pn':str(i),
                        'kd':'大数据'
                    }
                else:
                    data = {
                        'first': 'false',
                        'pn': str(i),
                        'kd': '大数据',
                        'sid':'ea05796f6f014966a8b505be78832c61'
                    }
                cookies = self.stringToDict(str(response.headers.getlist('Set-Cookie')))
                # print(cookies)#查看cookie的格式是否正确
                yield scrapy.FormRequest(url=urls, formdata=data,method='POST',cookies=cookies,callback=self.parse, dont_filter=True)
        except Exception as e:
            print('生成了一个{}错误'.format(e))
    def parse(self, response):
        try:
            results = json.loads(response.text)
            contents = results["content"]["positionResult"]["result"]  # 进入到result这个字典里面，这里包含着所有的招聘的详细信息
            # ["content"]["positionResult"]["result"]：表示着以级一级地进入到result这个字典中。
            for content in contents:
                positionName = content['positionName']  # 获取职位名称
                city = content['city']  # 获取城市
                district = content['district']#地区
                linestaion = content['linestaion']#路线
                if linestaion == None:
                    linestaion = '无具体路线！'
                companyFullName = content['companyFullName']  # 获取公司名称
                companyShortName = content['companyShortName']  # 公司简称
                industryField = content['industryField']  # 公司所属领域
                financeStage = content['financeStage']  # 融资阶段
                positionAdvantage = content['positionAdvantage']  # 职位福利
                if positionAdvantage == None:
                    positionAdvantage = '无福利！'
                companyLabelList = ' '.join(content['companyLabelList'])#公司福利
                if companyLabelList == None:
                    companyLabelList = '无福利！'
                education = content['education']  # 获取学历
                salary = content['salary']  # 获取薪资
                workYear = content['workYear']  # 获取工作经验
                lastLogin = content['lastLogin']  # 获取最后发布时间
                companySize = content['companySize']  # 获取公司规模
                skillLables = ' '.join(content['skillLables'])  # 获取学识要求
                if skillLables == None:
                    skillLables = "无具体要求！"
                item = LagouItem(positionName=positionName,city=city,district=district,linestaion=linestaion,companyFullName=companyFullName,
                                 companyShortName=companyShortName,industryField=industryField,
                                 financeStage=financeStage,positionAdvantage=positionAdvantage,companyLabelList=companyLabelList,
                                 education=education,salary=salary,workYear=workYear,
                                 lastLogin=lastLogin,companySize=companySize,skillLables=skillLables)

                print(positionName, city,district,linestaion,companyFullName, companyShortName, industryField,
                      financeStage, positionAdvantage,companyLabelList,
                      education, salary, workYear, lastLogin, companySize, skillLables)
                yield item


        except Exception as e:
            print(e)
