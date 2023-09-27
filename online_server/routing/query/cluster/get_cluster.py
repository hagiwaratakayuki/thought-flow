from db.cluster import Cluster

def fetch(limit:int=2000):
    q = Cluster.query()
    q.order = ['-linked_count']
    q.projection = ["published"]    
    return q.fetch(limit=limit)