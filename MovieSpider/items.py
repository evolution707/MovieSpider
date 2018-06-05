# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviespiderItem(scrapy.Item):
    # (公共字段)
    # 片名
    title = scrapy.Field()
    # 导演
    director = scrapy.Field()
    # 编剧
    writer = scrapy.Field()
    # 主演
    actor = scrapy.Field()
    # 类型
    type = scrapy.Field()
    # 地区
    area = scrapy.Field()
    # 语言
    language = scrapy.Field()
    # 又名
    other_name = scrapy.Field()
    # 简介
    intro = scrapy.Field()
    # 图片
    pic = scrapy.Field()
    # 评分
    grade = scrapy.Field()

    # (电影字段)
    # 上映时间
    release_date = scrapy.Field()
    # 片长
    lenght = scrapy.Field()

    # (电视剧字段)
    # 首播时间
    debut = scrapy.Field()
    # 集数
    cd = scrapy.Field()
    # 单集片长
    min = scrapy.Field()


