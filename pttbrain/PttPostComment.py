class PttPostComment:
    # 建構式
    def __init__(self, Id, PostId, content, IP, UserId, TagComment, Comment_Datetime):
        self.Id = Id
        self.PostId = PostId
        self.content = content
        self.IP = IP
        self.UserId = UserId
        self.TagComment = TagComment
        self.Comment_Datetime = Comment_Datetime
