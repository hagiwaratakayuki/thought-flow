from db.vertex import Vertex

def query(limit:int=2000):
    q = Vertex.query()
    q.order()