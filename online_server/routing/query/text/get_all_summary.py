from db.text import Text


def fetch(limit:int=2000):
    q = Text.query()
    q.order = ['-weight']
    
    return q.fetch(limit=limit)