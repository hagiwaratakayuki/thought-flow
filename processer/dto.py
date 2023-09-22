#interface data trsnsfer object

class DTO:
    def __init__(self, title:str='', body:str='', date:str='', data:dict={}):
        self.title = title
        self.body = body
        self.data = data.copy()
        self.date = date


