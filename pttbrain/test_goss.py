from datetime import datetime
import json
from PttPost import PttPost
from PttPostComment import PttPostComment
import requests
import configparser
import pyodbc

config = configparser.ConfigParser()
config.read('..\config.env')
db_UserName = config.get('DEFAULT', 'DB_USERNAME')
db_Password = config.get('DEFAULT', 'DB_PASSWORD')
db_Name = config.get('DEFAULT', 'DB_NAME')
db_Host = config.get('DEFAULT', 'DB_HOST')

# 政黑
ptt_apiurl = "https://www.pttbrain.com/ptt/board/8"
headers = {"Content-Type": "application/json"}
start_index = 1319600
end_index = 1380000
# start_index = 0
# end_index = 10
get_data_count = 100


def write_json(new_data, filename='data.json'):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data['data'].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)


def print_ClassValue(classObject):
    attrs = vars(classObject)
    print(', '.join("%s: %s" % item for item in attrs.items()))

# 貼文
def insert_post_content(get_data_count):
    ptt_apiurl = f"https://pttbrain-api.herokuapp.com/api/ptt/board/8/articles?limit={get_data_count}&offset={i}"
    response = requests.get(ptt_apiurl,  headers=headers)
    data = response.json()
    articles = data['data']

    for article in articles:
        post = PttPost('', '', '', '', '', '', '', None, 0, 0, 0, None)
        post.Id = article["id"]
        print(post.Id)
        post.source = 'Gossiping'
        post.title = article["title"]
        post.content = article["content"]
        post.author = article["author"]
        post.author_id = article["author_id"]
        post.url = article["url"]
        if article["datetime"] is None:
            datetime_str = None
        else:
            datetime_str = article["datetime"]

        post.postdatetime = datetime_str
        post.num_like = article["num_likes"]
        post.num_hate = article["num_hates"]
        post.num_replies = article["num_replies"]
        if article["updated_at"] is None:
            datetime_str = None
        else:
            datetime_str = article["updated_at"]

        sql = "select * from dbo.pttpostgossing where source=? and Id=?"
        result = cursor.execute(sql, post.source, post.Id)
        if len(result.fetchall()) > 0:
            continue

        if datetime_str is not None and post.postdatetime.count('2021') > 0:
            post.update_at = datetime_str

            sql = "INSERT INTO dbo.pttpostgossing([source],[Id],[title],[context],[author],[author_id],[url],[postdatetime],[num_like],[num_hate],[num_replies],[update_at]) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)"

            cursor.execute(sql, post.source, post.Id, post.title, post.content, post.author,
                           post.author_id, post.url, post.postdatetime, post.num_like,
                           post.num_hate, post.num_replies, post.update_at)

            # 回文的總筆數
            comments_count = post.num_like+post.num_hate+post.num_replies
            insert_comment_content(comments_count, post.Id)

# 回文


def insert_comment_content(comments_count, postId):
    ptt_PostCommentUrl = f"https://pttbrain-api.herokuapp.com/api/ptt/article/{postId}/pushes?limit={comments_count}&offset=0"
    response = requests.get(ptt_PostCommentUrl,  headers=headers)
    json_object = response.json()
    data = json_object['data']
    comments = data['content']

    for comment in comments:
        postComment = PttPostComment('', '', '', '', '', '', None)
        postComment.Id = comment['id']
        postComment.PostId = postId
        postComment.IP = comment['ip']
        postComment.content = comment['content']
        postComment.TagComment = comment['tag']
        if comment['timestp'] is None:
            postComment.Comment_Datetime = None
        else:
            postComment.Comment_Datetime = comment['timestp']

        postComment.UserId = comment['user_id']
        sql = "INSERT INTO dbo.pttpostcommentgossing([Id],[postId],[content],[ip],[userid],[tagcomment],[comment_datetime]) VALUES(?,?,?,?,?,?,?)"
        cursor.execute(
            sql, postComment.Id, postComment.PostId, postComment.content, postComment.IP, postComment.UserId, postComment.TagComment, postComment.Comment_Datetime)

try:
    cnxn_str = ("Driver={SQL Server Native Client 11.0};"
                f"Server={db_Host};"
                f"Database={db_Name};"
                f"UID={db_UserName};"
                f"PWD={db_Password};")

    cnxn = pyodbc.connect(cnxn_str)
    # Create a cursor from the connection
    cursor = cnxn.cursor()

    for i in range(start_index, end_index, get_data_count):
        # 貼文
        print("目前流水號:", i)
        insert_post_content(get_data_count)
        cnxn.commit()
finally:
    cnxn.commit()
    cnxn.close()
