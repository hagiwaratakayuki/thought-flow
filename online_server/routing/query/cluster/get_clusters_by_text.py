from db.cluster import Cluster
from db.cluster_member import ClusterMember

def fetch(text_id:str ,start_cursor:str | None=None, limit:int=10):
    q = ClusterMember.query()
    q.add_filter("text_id", "=", text_id)
    q.order = ['-linked_count']
    q.projection  = ["cluster_id"]
    return Cluster.get_multi([e["cluster_id"] for e in q.fetch(limit=limit, start_cursor=start_cursor)])
     