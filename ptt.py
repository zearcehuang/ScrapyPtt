import logging
import sys
import time
import PyPtt
import pyodbc
import uuid
from datetime import datetime

ptt_bot = PyPtt.API()
try:
    ptt_bot.login('account', 'PW', False)
    # start_index = 19050
    start_index = 19486
    last_index = 111104
    newest_index = ptt_bot.get_newest_index(PyPtt.NewIndex.BOARD, 'Gossiping')

    # print(newest_index)

    for i in range(start_index, last_index):
        # post_info = ptt_bot.get_post('Gossiping', index=newest_index)
        post_info = ptt_bot.get_post('Gossiping', index=i)

        # print(post_info)
        if post_info[PyPtt.PostField.post_status] == PyPtt.PostStatus.EXISTS:
            total_score = 0
            score = 0
            for comment in post_info[PyPtt.PostField.comments]:
                if comment[PyPtt.CommentField.type] == PyPtt.CommentType.BOO:
                    score = -1
                elif comment[PyPtt.CommentField.type] == PyPtt.CommentType.PUSH:
                    score = 1
                else:
                    score = 0

                total_score += score

            # Specifying the ODBC driver, server name, database, etc. directly
            cnxn_str = ("Driver={SQL Server Native Client 11.0};"
                        "Server=server;"
                        "Database=dbname;"
                        "UID=account;"
                        "PWD=password;")
            cnxn = pyodbc.connect(cnxn_str)
            # Create a cursor from the connection
            cursor = cnxn.cursor()

            if post_info[PyPtt.PostField.date] is None:
                datetime_str = None
            else:
                datetime_str = datetime.strptime(
                    post_info[PyPtt.PostField.date], '%a %b %d %H:%M:%S %Y')

            sql = "INSERT INTO dbo.post(Id,title,author,date,content,ip,score,[Url]) VALUES(?,?,?,?,?,?,?,?)"
            
            cursor.execute(sql, post_info[PyPtt.PostField.index], post_info[PyPtt.PostField.title], post_info[PyPtt.PostField.author],
                           datetime_str, post_info[PyPtt.PostField.content], post_info[PyPtt.PostField.ip], total_score, post_info[PyPtt.PostField.url])

            # print(post_info)
            print('文章編號:', post_info[PyPtt.PostField.index])
            # print('作者:', post_info[PyPtt.PostField.author])
            print('標題:', post_info[PyPtt.PostField.title])
            # print('日期:', post_info[PyPtt.PostField.date])
            # print('文章網址:', post_info[PyPtt.PostField.url])
            # print('文章 IP:', post_info[PyPtt.PostField.ip])
            # print('文章推文數量:', post_info[PyPtt.PostField.push_number])
            # print('文章推文:', post_info[PyPtt.PostField.comments])
            # print('文章內容:', post_info[PyPtt.PostField.content])

            for comment in post_info[PyPtt.PostField.comments]:
                if comment[PyPtt.CommentField.type] == PyPtt.CommentType.BOO:
                    score = -1
                elif comment[PyPtt.CommentField.type] == PyPtt.CommentType.PUSH:
                    score = 1
                else:
                    score = 0

                sql = "INSERT INTO dbo.postcomment(Id,postId,[user],[content],score,ip,commenttime) VALUES(?,?,?,?,?,?,?)"
                cursor.execute(
                    sql, str(uuid.uuid1()), post_info[PyPtt.PostField.index], comment[PyPtt.CommentField.author], comment[PyPtt.CommentField.content], score, comment[PyPtt.CommentField.ip], comment[PyPtt.CommentField.time])

        cnxn.commit()
        print('文章資料可以使用')
finally:
    ptt_bot.logout()
    cnxn.commit()
    cnxn.close()
