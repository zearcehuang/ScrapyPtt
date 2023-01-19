# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pyodbc
import json


class PttPipeline:
    def __init__(self):
        cnxn_str = ("Driver={SQL Server Native Client 11.0};"
                    "Server=.,1400;"
                    "Database=PTTSpider;"
                    "UID=sa;"
                    "PWD=Passw0rd;")
        self.conn = pyodbc.connect(cnxn_str)
        self.cursor = self.conn.cursor()
        print('連線成功')

    def process_item(self, item, spider):
        try:
            sql = "INSERT INTO dbo.post(Id,title,author,date,content,ip,score,[Url]) VALUES(?,?,?,?,?,?,?,?)"

            self.cursor.execute(sql, item['Id'], item['title'], item['author'],
                                item['date'], item['content'], item['ip'], item['score'], item['url'])

            for comment in item['comments']:
                sql = "INSERT INTO dbo.postcomment(Id,postId,[user],[content],score,ipdatetime) VALUES(?,?,?,?,?,?)"
                self.cursor.execute(
                    sql, comment['Id'], comment['postId'], comment['user'], comment['content'], comment['score'], comment['ipdatetime'])

            print('資訊寫入成功')
        except Exception as ex:
            print('has error occur', str(ex))

        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
