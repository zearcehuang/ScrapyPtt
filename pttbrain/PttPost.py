class PttPost:
    # 建構式
    def __init__(self, source, Id, title, content, author, author_id, url, postdatetime, num_like, num_hate, num_replies, update_at):
        self.source = source 
        self.Id = Id
        self.title = title
        self.content = content
        self.author = author
        self.author_id = author_id
        self.url = url
        self.postdatetime = postdatetime
        self.num_like = num_like
        self.num_hate = num_hate
        self.num_replies = num_replies
        self.update_at = update_at
