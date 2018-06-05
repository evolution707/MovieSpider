# -*- coding: utf-8 -*-
import json
import scrapy
from MovieSpider.items import MoviespiderItem
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class BdseeSpider(scrapy.Spider):
    name = 'bdsee'
    allowed_domains = ['www.bdsee.cn']
    offset = 1
    base_url = 'http://www.bdsee.cn/page/'
    start_urls = [base_url + str(offset)]

    def parse(self, response):
        url_list = response.xpath("//div[@class='content']/header/a/@href").extract()
        last_page_url = response.xpath("//div[@class='wp-pagenavi']/a[@class='last']/@href").extract()[0]
        # last_page_url = "http://www.bdsee.cn/page/360/"
        last_page = last_page_url.split('/')[-2]

        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse_1)

        self.offset += 1
        if self.offset < int(last_page):
            url = self.base_url + str(self.offset)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_1(self, response):
        item = MoviespiderItem()
        # 目标网站所有影片信息放在一个p标签中，相邻p标签中存放'简介'字段
        tag_p_1 = response.xpath("//div[@class='article-container post clearfix']/article/p[1]/text()").extract()
        # 此处不可以为None
        if tag_p_1 == []:
            tag_p = response.xpath("//div[@class='article-container post clearfix']/article/p[2]/text()").extract()
            intro_list = response.xpath("//div[@class='article-container post clearfix']/article/p[2]/following-sibling::p/text()").extract()
        else:
            tag_p = response.xpath("//div[@class='article-container post clearfix']/article/p[1]/text()").extract()
            intro_list = response.xpath("//div[@class='article-container post clearfix']/article/p[1]/following-sibling::p/text()").extract()
        # 分解p标签中的内容
        info_dict = {}
        for i in tag_p:
            s = i.split(':')
            info_dict[s[0].strip()] = s[1].strip()
        for key in info_dict:
            if key == '导演':
                item['director'] = info_dict[key]
            elif key == '编剧':
                item['writer'] = info_dict[key]
            elif key == '主演':
                item['actor'] = info_dict[key]
            elif key == '制片国家/地区':
                item['area'] = info_dict[key]
            elif key == '语言':
                item['language'] = info_dict[key]
            elif key == '又名':
                item['other_name'] = info_dict[key]
            elif key == '上映日期':
                item['release_date'] = info_dict[key]
            elif key == '片长':
                item['lenght'] = info_dict[key]
            elif key == '首播':
                item['debut'] = info_dict[key]
            elif key == '集数':
                item['cd'] = info_dict[key]
            elif key == '单集片长':
                item['min'] = info_dict[key]
            elif key == '类型':
                item['type'] = info_dict[key]
            else:
                pass

        # 片名
        title = response.xpath("//div[@class='article-details']/h1/text()").extract()[0]
        # 评分
        grade = response.xpath("//div[@class='post-ratings']/text()").extract()[1].split('(')[1].strip()[0:3]
        # 图片为两张
        pic_list = response.xpath("//div[@class='article-container post clearfix']/article/p/a[1]/@href").extract()
        pic = ','.join(pic_list)
        intro = ','.join(intro_list)

        item['title'] = title
        item['intro'] = intro
        item['pic'] = pic
        item['grade'] = grade

        # with open('F:/223344.json','a') as f:
        #     f.write(json.dumps(dict(item),ensure_ascii=False)+'\n')
        yield item







