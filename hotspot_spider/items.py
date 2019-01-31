# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HotspotSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    mainclass=scrapy.Field()
    subclass=scrapy.Field()
    title=scrapy.Field()
    news=scrapy.Field()
    newsdate=scrapy.Field()
    author=scrapy.Field()
    # 消息来源
    newsource=scrapy.Field()
