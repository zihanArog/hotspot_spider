# -*- coding: utf-8 -*-
import scrapy
from hotspot_spider.items import HotspotSpiderItem


class SinaNewsSpider(scrapy.Spider):
    name = 'sina_news'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):

        parent_div = response.css('div#tab01>div:not([data-sudaclick=citynav])')

        for div in parent_div:

            # 这个也就是大类：mainclass
            parent_title = div.css('h3>a::text').extract()[0]

            sub_div = div.css('ul>li>a')
            for each in sub_div:
                # 小类：subclass
                item = HotspotSpiderItem()
                sub_url = each.css('::attr(href)').extract()[0]
                sub_title = each.css('::text').extract()[0]

                item['mainclass'] = parent_title
                item['subclass'] = sub_title

                # 处理小类页面
                yield scrapy.Request(url=sub_url,meta={'meta_1':item,'sub_url':sub_url},callback=self.parse_subpage)


    def parse_subpage(self,response):

        item=response.meta['meta_1']
        valid_links=[]
        sub_url=response.meta['sub_url']

        all_link=response.css('a::attr(href)').extract()

        for link in all_link:

            if link.startswith(sub_url) and link.endswith('.shtml'):

                valid_links.append(link)
        for link in valid_links:
            print('正在爬取新闻{}'.format(link))
            yield scrapy.Request(url=link,meta={'meta_2':item},callback=self.parse_news)


    def parse_news(self,response):

        item=response.meta['meta_2']
        item['title']=str(response.css('h1.main-title::text,h1#artibodyTitle::text').extract_first())
        if item['title'] != 'None':
            spans=response.css('div.date-source>span::text,span#pub_date::text').extract()
            item['newsource']=str(response.css('div.date-source>a::text,span#media_name>a::text').extract_first())
            if len(spans)>0:
                item['newsdate']=spans[0]
                if len(spans)>1:
                    item['author']=spans[1]
                else:
                    item['author']='None'
            else:
                item['newsdate']='None'
            item['news']=''.join(str(response.css('div#artibody>p::text').extract_first()))
            yield item