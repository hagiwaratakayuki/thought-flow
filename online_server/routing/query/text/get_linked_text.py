from db.text import Text

def fetch(text_id:str, cursor: str | None = None, limit:int = 10):
    start_cursor = None
    if cursor != None:
        start_cursor = cursor.encode('utf-8')
    query = Text.query()
    query.add_filter('link_to', '=', text_id)
    query.order = ["linked_count"]
    itr = query.fetch(start_cursor=start_cursor, limit=limit)
    next_page_token = None
    if itr.next_page_token != None:
        next_page_token = itr.next_page_token.decode('utf-8') 
    return Text.get_multi([{'id':e.id or e.key.name} for e in itr]), next_page_token