from db.text import Text


def query(limit:int=2000):
    q = Text.query()
    q.order = ['-linked_count']
    q.projection = ["published"]    
    return q.fetch(limit=limit)