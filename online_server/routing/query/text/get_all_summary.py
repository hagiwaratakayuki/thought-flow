from db.text import Text
import itertools

def fetch(limit:int=200):
    q = Text.query()
    q.order = ['-weight']
    
    return q.fetch(limit=limit)