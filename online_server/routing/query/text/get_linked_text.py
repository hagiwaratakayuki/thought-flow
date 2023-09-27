from db.text import Text

def fetch(text_id:str, start_cursor=str | None, limit:int = 10):
    query = Text.query()
    query.add_filter('link_to', '=', text_id)
    query.order = ["linked_count"]
    itr = query.fetch(start_cursor=start_cursor, limit=limit)
    return itr, itr.next_page_token