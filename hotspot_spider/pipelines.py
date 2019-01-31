# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class HotspotSpiderPipeline(object):
    def process_item(self, item, spider):
        # 数据库链接
        db=pymysql.connect(user='zihan',password='zihan979',port=3306,db='sina',host='localhost')
        # 这是一个游标
        cursor=db.cursor()

        # 数据库的表
        table='news'
        keys=','.join(item.keys())
        values=','.join(['%s']*len(item))

        # 创建表的命令
        create_table='''
            create table if not exists news(
                mainclass varchar(255),
                subclass varchar(255),
                title varchar(255) not null,
                newsdate varchar(255),
                author varchar(255),
                newsource varchar(255),
                news text,
                primary key (title)
            )
        '''
        insert_item='insert into {table}({keys}) values({values}) on duplicate key update '.format(table=table,keys=keys,values=values)
        insert_item+=','.join("{key}=%s".format(key=key) for key in item.keys())
        # 数据库如果不存在则创建
        create_database='create database if not exists sina'

        #创建表
        cursor.execute(create_table)

        try:
            cursor.execute(insert_item,tuple(item.values())*2)
            print('成功插入数据')
            db.commit()
        except:
            db.rollback()
        return item
