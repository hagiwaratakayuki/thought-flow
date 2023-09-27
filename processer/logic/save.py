
import numpy as np
from db import text, cluster, cluster_member, model as db_model, edge, text_to_keyword
from multiprocessing import Pool
from collections import deque, defaultdict

from ridgedetect.taged import Taged
from doc2vec import Doc2Vec
from doc2vec.indexer.dto import SentimentResult
from logic.data import date_converter
import uuid

def process(loader):
    vectaizer = buildVectaizer()
    model = buildModel()

    datas = loader('')
 
    vectors = vectaizer.exec(datas)
    
    

    return _save(vectors, model=model)
            





class Model:

    def __init__(self) -> None:
        self._chunk = []
        self._vectotrs = []
        self._keywords = []

    def save(self, eid, data, vector, sentiment_result:SentimentResult, linked_to:list[str], linked_count:int):
        textEntity = text.Text(eid=eid)
        sentiment = {'neautral':sentiment_result.weights.neutral, 'negative':sentiment_result.weights.negative, 'positive':sentiment_result.weights.positive}
        textEntity.setProperty('',  
                               data.body, 
                               dict(vector=vector.tolist(), sentiment=sentiment),
                               linked_to=linked_to, 
                               linked_count=linked_count, 
                               published=date_converter.convert(data.published))
        self._chunk.append(textEntity)
        
        
        
        if len(self._chunk) < 30:
            return
        entities = db_model.put_multi(self._chunk)
        

        return entities
    def finish(self):
        entities = db_model.put_multi(self._chunk)
        return entities



def buildModel():
    return Model()
    

def buildVectaizer():
    return Doc2Vec()

#ファイルを読む
#パース
#クラスタリング　+ キーワード抽出
#保存

def _save(datas, model:Model):
   
    tags_map = {}
    index2id = {}
    
    vectors_map = {}
    
    index = 0
    
    shape = [0, 0]
    is_first = True
    for vector, sentimentResults, keywords, data in datas:
        
        
        if is_first == True:
            is_first = False
            shape[1] = vector.shape[0] 
        vectors_map[index] = vector
        index2id[index] = uuid.uuid4()
        tags_map[index] = keywords
        index +=1  
        

   
    
   

    shape[0] = index

    vectors = np.zeros(shape=shape)
  
    
   
    for i, v in vectors_map.items():
        vectors[i] = v
   
    taged = Taged()
    taged.fit(tags_map=tags_map, vectors=vectors, sample=4)
    count = 0
    chunk = []
    members_chunk = []
    connect_count_cache = {}
    member_model_chunk = []
    member_model_count = 0
    for cluster_members in taged.clusters.values():
        cluster_model = cluster.Cluster()
        cluster_model.member_count = len(cluster_members)
        chunk.append(cluster_model)
        members_chunk.append(cluster_members)
        count += 1
        
        if count >= 30:
            
            entities = db_model.put_multi(chunk)
            chunk = []
            count = 0
            
            for entity, members in zip(entities, members_chunk):
               
                for member in members:
                    member_model =  cluster_member.ClusterMember()
                    member_model.cluster = entity.id
                    member_model.vertex = index2id[member]
                    if not member in connect_count_cache:
                        connect_count_cache[member] = len(taged.graph.get(member, {}))
                    member_model.connect = connect_count_cache[member]
                    member_model_chunk.append(member_model)
                    member_model_count += 1
                    if member_model_count >= 30:
                        
                        db_model.put_multi(member_model_chunk)
                        member_model_count = 0
                        member_model_chunk = []
           
    if count > 0:
        entities = db_model.put_multi(chunk)
        chunk = []
        count = 0
        for entity, members in zip(entities, members_chunk):
            for member in members:
                member_model =  cluster_member.ClusterMember()
                member_model.cluster = entity.id
                member_model.vertex = index2id[member]
                if not member in connect_count_cache:
                    connect_count_cache[member] = len(taged.graph.get(member, {}))
                member_model.connect = connect_count_cache[member]
                member_model_chunk.append(member_model)
                member_model_count += 1
                if member_model_count >= 30:
                    db_model.put_multi(member_model_chunk)
                    member_model_count = 0
    if member_model_count > 0:
        db_model.put_multi(member_model_chunk)
    chunk = []
    count = 0
    linked_counts_map = defaultdict(int)
    for ind, vertexs in taged.graph.items():
        
        for vertex in vertexs:
            edge_model = edge.Edge()
            edge_model.linked_from = index2id[ind]
            link_to = index2id[vertex]
            linked_counts_map[link_to] += 1
            edge_model.link_to = link_to
            chunk.append(edge_model)
            count += 1
            if count >= 30:
                db_model.put_multi(chunk)
                count = 0
                chunk = []
    if count > 0:
        db_model.put_multi(chunk)
    index = 0
    model = Model()
    keyword_chunk = deque()
    keyword_count = 0 
    for vector, sentimentResults, keywords, data in datas:
        eid = index2id[index]
        link_to = [index2id[to_index] for to_index in taged.graph[index]]
        linked_count = linked_counts_map[index]
        model.save(eid=eid, data=data, vector=vector, sentiment_result=sentimentResults,linked_to=link_to, linked_count=linked_count)
        for keyword in keywords:
            keyword_model = text_to_keyword.TextToKeyword()
            keyword_model.published = data.published
            keyword_model.linked_count = linked_count
            keyword_model.keyword = keyword
            keyword_model.text_id = eid
            keyword_chunk.append(keyword_model)
            keyword_count += 1
            if keyword_count >= 30:
                db_model.put_multi(keyword_chunk)
                keyword_count = 0
                keyword_chunk = deque()
    if keyword_count > 0:
       db_model.put_multi(keyword_chunk)     



        

    model.finish()
