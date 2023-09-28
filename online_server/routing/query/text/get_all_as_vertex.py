from db.text import Text


def fetch(limit:int=2000):
    q = Text.query()
    q.order = ['-linked_count']
    
    return q.fetch(limit=limit)