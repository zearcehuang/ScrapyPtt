import logging
import sys
import time
import PyPtt

ptt_bot = PyPtt.API()
try:
    ptt_bot.login('ecloud01', '13579', False)
    newest_index = ptt_bot.get_newest_index(PyPtt.NewIndex.BOARD, 'Gossiping')

    print(newest_index)

    # .. login ..
    # post_info = ptt_bot.get_post('Gossiping', index=newest_index)
    post_info = ptt_bot.get_post('Gossiping', index=221893)    

    print(post_info)
    print('文章編號:', post_info[PyPtt.PostField.index])
    print('作者:', post_info[PyPtt.PostField.author])
    print('標題:', post_info[PyPtt.PostField.title])
    print('日期:', post_info[PyPtt.PostField.date])
    print('文章網址:', post_info[PyPtt.PostField.url])
    print('文章 IP:', post_info[PyPtt.PostField.ip])
    print('文章推文數量:', post_info[PyPtt.PostField.push_number])
    print('文章推文:', post_info[PyPtt.PostField.comments])
    print('文章內容:', post_info[PyPtt.PostField.content])

    for comment in post_info[PyPtt.PostField.comments]:
        print('推文作者:', comment[PyPtt.CommentField.author])
        print('推文類型:', comment[PyPtt.CommentField.type])

    if post_info[PyPtt.PostField.post_status] == PyPtt.PostStatus.EXISTS:
        print('文章存在！')
    elif post_info[PyPtt.PostField.post_status] == PyPtt.PostStatus.DELETED_BY_AUTHOR:
        print('文章被作者刪除')
        sys.exit()
    elif post_info[PyPtt.PostField.post_status] == PyPtt.PostStatus.DELETED_BY_MODERATOR:
        print('文章被版主刪除')
        sys.exit()

    if not post_info[PyPtt.PostField.pass_format_check]:
        print('未通過格式檢查')
        sys.exit()

    print('文章資料可以使用')
finally:
    ptt_bot.logout()
