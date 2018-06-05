# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#
# class MoviespiderPipeline(object):
#     def process_item(self, item, spider):
#         return item
import pymysql
import datetime


class MySQLPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            db='bdsee',
            user='root',
            passwd='root123',
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):

        type_dict = {1: '剧情', 2: '喜剧', 3: '动作', 4: '爱情', 5: '科幻', 6: '悬疑', 7: '惊悚',
                     8: '恐怖', 9: '犯罪', 10: '同性', 11: '音乐', 12: '歌舞', 13: '传记', 14: '历史',
                     15: '战争', 16: '西部', 17: '奇幻', 18: '冒险', 19: '灾难', 20: '武侠', 21: '情色',22: '纪录片'}
        area_dict = {1: '中国大陆', 2: '美国', 3: '香港', 4: '台湾', 5: '日本', 6: '韩国', 7: '英国',
                     8: '法国', 9: '德国', 10: '意大利', 11: '西班牙', 12: '印度', 13: '泰国', 14: '俄罗斯',
                     15: '伊朗', 16: '加拿大', 17: '澳大利亚', 18: '爱尔兰', 19: '瑞典', 20: '巴西', 21: '丹麦'}

        # 将字符串  "剧情 / 动作 / 科幻 / 悬疑" 根据对应关系转换成类似[1,3,5,6],方便添加到多对多关系表中
        def str_to_num(data_dict, field_dict, field):
            field_num_list = []
            try:
                field_list = data_dict[field].replace(' ', '').split('/')
                for field in field_list:
                    for value in field_dict.values():
                        if field == value:
                            field_id = list(field_dict.keys())[list(field_dict.values()).index(value)]
                            field_num_list.append(field_id)
            except:
                pass
            return field_num_list

        type_num_list = str_to_num(item, type_dict, 'type')
        area_num_list = str_to_num(item, area_dict, 'area')

        # 根据所要insert的数据，动态的获取其需要添加的字段
        keys = ', '.join(item.keys())
        values = ', '.join(['%s'] * (len(item) + 1))
        sql_1 = 'SELECT * FROM movie_movieandtv WHERE title = %s'
        # sql_2 ---->  "insert into movie_movieandtv (pic, language, area, grade, release_date, ...)values(%s,%s,%s,%s,%s,%s...)"
        sql_2 = 'INSERT INTO movie_movieandtv ({keys}, ctime) VALUES ({values})'.format(keys=keys, values=values)
        sql_3 = "INSERT INTO movie_movieandtv_m_to_type (movieandtv_id,movieandtvtype_id) VALUES (%s,%s)"
        sql_4 = "INSERT INTO movie_movieandtv_m_to_area (movieandtv_id,movieandtvarea_id) VALUES (%s,%s)"

        # 不知何种原因造成的数据库断连，错误信息 _mysql_exceptions.InterfaceError: (0, '')
        # 解决方法每次连接之前判断链接是否有效,触发异常则重连
        try:
            self.connect.ping()
        except:
            self.connect = pymysql.connect(host='localhost', port=3306, user='root', passwd='root123', db='bdsee', charset='utf8')
            self.cursor = self.connect.cursor()

        try:
            # 查重处理
            self.cursor.execute(sql_1,item['title'])
            repetition = self.cursor.fetchone()
            if repetition:
                pass
            else:
                # insert的数据没有‘创建时间’字段，另行添加ctime字段，值为当前系统时间
                ctime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.cursor.execute(sql_2, tuple(item.values() + [ctime]))
                # 查询 last_insert_id()
                r = int(self.connect.insert_id())
                # 构造插入的数据,表示当主表插入完数据，记录其id为保存在r变量，
                # 关系表中添加的值类似(1,3),(1,5),(1,9)==>1为主表id，(3,5,9)为已知类型表id
                # 7个r是因为一部影片最多有7个类型
                last_insert_id = [r, r, r, r, r, r, r]
                self.cursor.executemany(sql_3, zip(last_insert_id, type_num_list))
                self.cursor.executemany(sql_4, zip(last_insert_id, area_num_list))

                print 'INSETR INTO---->', item['title']
                self.connect.commit()
        except Exception as error:
            print 'An ERROR---->',error
            self.connect.rollback()
        self.connect.close()
        print 'done!!!!'
        return item