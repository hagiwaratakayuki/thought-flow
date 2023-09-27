from db.text import Text
from db.cluster_member import ClusterMember

def fetch(cluster_id:str ,start_cursor:str | None=None, limit:int=100):
    q = ClusterMember.query()
    q.add_filter("cluster_id", "=", cluster_id)
    q.order = ['-linked_count']
    q.projection  = ["text_id"]
    itr = q.fetch(start_cursor=start_cursor, limit=limit)
    return Text.get_multi([e["text_id"] for e in itr]), itr.next_page_token