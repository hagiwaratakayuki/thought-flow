from db.text_keyword import TextKeyword


def fetch(text_id:str):
    query = TextKeyword.query()
    query.add_filter("text_id", "=", text_id)
    query.projection = ["keyword"]
    return [e["keyword"] for e in query.fetch()]
