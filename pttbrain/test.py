import json
from PttPost import PttPost
from PttPostComment import PttPostComment
import requests

# post = PttPost()
# postComment = PttPostComment()
# 政黑
ptt_apiurl = "https://www.pttbrain.com/ptt/board/22"
headers = {"Content-Type": "application/json"}
start_index = 0
end_index = 500

# function to add to JSON
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

    # python object to be appended


for i in range(start_index, end_index, 100):
    ptt_apiurl = f"https://pttbrain-api.herokuapp.com/api/ptt/board/22/articles?limit=5&offset={i}"
    response = requests.get(ptt_apiurl,  headers=headers)
    data = response.json()
    articles = data['data']
    write_json(articles)
    print('目前序號:', i)
