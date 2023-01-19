from datetime import datetime
import json
from PttPost import PttPost
from PttPostComment import PttPostComment
import requests
import configparser
import pyodbc
from DcardPostMedia import DcardPostMedia
from DcardPostReaction import DcardPostReaction
from DcardPostComment import DcardPostComment

config = configparser.ConfigParser()
config.read('..\config_dcard.env')
db_UserName = config.get('DEFAULT', 'DB_USERNAME')
db_Password = config.get('DEFAULT', 'DB_PASSWORD')
db_Name = config.get('DEFAULT', 'DB_NAME')
db_Host = config.get('DEFAULT', 'DB_HOST')

# 閒聊
ptt_apiurl = "https://pttbrain-api.herokuapp.com/api/dcard/forum/255fd275-fec2-49d2-8e46-2e1557ffaeb0"
headers = {"Content-Type": "application/json"}
start_index = 99095
end_index = 99195
# start_index = 35995
# end_index = 93195
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


def insert_post_content(get_data_count):
    """
    貼文
    """
    ptt_apiurl = f"https://pttbrain-api.herokuapp.com/api/dcard/forum/255fd275-fec2-49d2-8e46-2e1557ffaeb0/posts?limit={get_data_count}&offset={i}"
    response = requests.get(ptt_apiurl,  headers=headers)
    data = response.json()
    articles = data['data']

    for article in articles:
        post = PttPost('', '', '', '', '', '', '', None, 0, 0, 0, None)
        post.Id = article["id"]
        print(post.Id)
        post.source = 'talk'
        post.title = article["title"]
        post.content = article["content"]
        post.num_like = article["num_comments"]

        if article["created_at"] is None:
            datetime_str = None
        else:
            datetime_str = article["created_at"]

        post.postdatetime = datetime_str

        sql = "select * from dbo.post where forum=? and Id=?"

        result = cursor.execute(sql, post.source, post.Id)
        if len(result.fetchall()) > 0:
            continue

        if datetime_str is not None and post.postdatetime.count('2021') > 0:
            # print_ClassValue(post)

            sql = "INSERT INTO dbo.post([Id],[forum],[title],[content],[num_comment],[crtdate]) VALUES(?,?,?,?,?,?)"

            cursor.execute(sql, post.Id, post.source, post.title,
                           post.content, post.num_like, post.postdatetime)

            # 回文的總筆數
            comments_count = post.num_like
            insert_comment_content(comments_count, post.Id)
            insert_reaction(article)
            insert_media(article)


def insert_reaction(article):
    """
    回應種類
    """

    reactions = article['reactions']
    reactionIndex = 0

    for reaction in reactions:
        reactionIndex += 1

        postReaction = DcardPostReaction('', '', '', '')
        postReaction.PostId = article["id"]
        postReaction.datacount = reaction['count']
        postReaction.link = reaction["link"]
        postReaction.descript = reaction["description"]

        sql = "INSERT INTO dbo.postreaction([Id],[postId],[count],[link],[descript]) VALUES(?,?,?,?,?)"

        cursor.execute(sql, reactionIndex, postReaction.PostId, postReaction.datacount,
                       postReaction.link, postReaction.descript)


def insert_media(article):
    """
    媒體連結
    """

    medias = article['media']

    mediaIndex = 0

    for media in medias:
        mediaIndex += 1
        postMedia = DcardPostMedia('', '')
        postMedia.PostId = article["id"]
        postMedia.media_url = media["url"]

        sql = "INSERT INTO dbo.postmedia([Id],[postId],[media_url]) VALUES(?,?,?)"

        cursor.execute(sql, mediaIndex, postMedia.PostId,
                       postMedia.media_url)


# 回文
def insert_comment_content(comments_count, postId):
    ptt_PostCommentUrl = f"https://pttbrain-api.herokuapp.com/api/dcard/post/{postId}/comments?limit={comments_count}&offset=0"
    response = requests.get(ptt_PostCommentUrl,  headers=headers)
    json_object = response.json()
    data = json_object['data']
    comments = data['content']

    for comment in comments:
        postComment = DcardPostComment('', '', '', 0, 0,  None)
        postComment.Id = comment['id']
        postComment.PostId = postId
        postComment.floor = comment['floor']
        postComment.content = comment['content']
        postComment.likecount = comment['like_count']
        if comment['created_at'] is None:
            postComment.postdate = None
        else:
            postComment.postdate = comment['created_at']

        # print_ClassValue(postComment)
        sql = "INSERT INTO dbo.postcomment([Id],[postId],[content],[floor],[likecount],[crtdate]) VALUES(?,?,?,?,?,?)"
        cursor.execute(
            sql, postComment.Id, postComment.PostId, postComment.content, postComment.floor, postComment.likecount, postComment.postdate)


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

# except Exception as e:
#     cnxn.rollback()
finally:
    # print('over')
    cnxn.commit()
    cnxn.close()
