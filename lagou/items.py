# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    positionName = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    linestaion = scrapy.Field()
    companyFullName = scrapy.Field()
    companyShortName = scrapy.Field()
    industryField = scrapy.Field()
    financeStage = scrapy.Field()
    positionAdvantage = scrapy.Field()
    companyLabelList = scrapy.Field()
    education = scrapy.Field()
    salary = scrapy.Field()
    workYear = scrapy.Field()
    lastLogin = scrapy.Field()
    companySize = scrapy.Field()
    skillLables = scrapy.Field()
