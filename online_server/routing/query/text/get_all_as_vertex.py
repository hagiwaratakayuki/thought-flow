from db.text import Text


def fetch(limit:int=2000):
    q = Text.query()
    q.order = ['-linked_count']
    q.projection = ["published", "link_to"]    
    return q.fetch(limit=limit)