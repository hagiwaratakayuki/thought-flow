from datetime import datetime
from typing import Any
class BaseDataDTO:
    def __init__(self, 
                 title:Any='', 
                 body:Any='', 
                 author:Any='',
                 authorid:Any='',
                 published:Any = None, 
                 data:Any={}):
        self.title = title
        self.body = body
        self.data = data.copy()
        self.published = published
        self.author = author
        self.authorid = authorid
fuga:Any = None
hoge:datetime = fuga

