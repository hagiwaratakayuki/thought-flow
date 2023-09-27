from db.cluster_keyword import ClusterKeyword


def fetch(cluster_id:str):
    query = ClusterKeyword.query()
    query.add_filter("text_id", "=", cluster_id)
    query.projection = ["keyword"]
    return [e["keyword"] for e in query.fetch()]
