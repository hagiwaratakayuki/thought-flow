
import numpy as np
from db import text, cluster, cluster_member, model as db_model, edge, cluster_keyword
from multiprocessing import Pool
from collections import deque, defaultdict
from db import text_keyword
from typing import Iterable
from ridgedetect.taged import Taged
from doc2vec import Doc2Vec
from doc2vec.indexer.dto import SentimentResult
from logic.data import date_converter
from db.util.chunked import Chunker
from doc2vec.indexer.dto import SentimentResult
import hashlib
from data_loader.dto import BaseDataDTO
from cluster.get_position import get_position

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

    def save(self, id, data, vector, sentiment_result:SentimentResult, linked_to:list[str], linked_count:int):
        textEntity = text.Text(id=id)
        sentiment = {'position':sentiment_result.vectors.neutral.tolist(), 'direction':(sentiment_result.vectors.positive - sentiment_result.vectors.negative).tolist()}
        textEntity.setProperty('',  
                               data.body, 
                               dict(vector=vector.tolist(), sentiment=sentiment),
                               linked_to=linked_to, 
                               linked_count=linked_count, 
                               published=data.published)
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

def _save(datas:Iterable[tuple[np.ndarray, SentimentResult, Iterable[str], BaseDataDTO]], model:Model):
   
    index2tag = {}
    index2id = {}
    index2published = {}
    index2sentiments:dict[int, SentimentResult] = {}

    index2vector = {}
    
    index = 0
    
    shape = [0, 0]
    is_first = True
    for vector, sentimentResult, keywords, data in datas:
        
        
        if is_first == True:
            is_first = False
            shape[1] = vector.shape[0] 
        index2vector[index] = vector
        index2sentiments[index] = sentimentResult
        id_binary = '/'.join([data.title , data.body,  data.author, data.authorid]).encode('utf-8')
        index2id[index] = hashlib.md5(id_binary).hexdigest()
        index2tag[index] = keywords
        index2published[index] = data.published
        index +=1  
        

   
    
   

    shape[0] = index

    vectors = np.zeros(shape=shape)
  
    
   
    for i, v in index2vector.items():
       
        vectors[i] = v
   
    taged = Taged()
    taged.fit(tags_map=index2tag, vectors=vectors, sample=32)

   
    #edge_chunk = Chunker()
    linked_counts_map = defaultdict(int)
    for ind, vertexs in taged.graph.items():
        for vertex in vertexs:
            link_to = index2id[vertex]
            linked_counts_map[link_to] += 1
    """
    for ind, vertexs in taged.graph.items():
        linked_from =  index2id[ind]
        published = index2published[ind]
        for vertex in vertexs:
            edge_model = edge.Edge()
            edge_model.linked_from = linked_from
            edge_model.published = published             
            edge_model.link_to = index2id[vertex]
            edge_model.linked_count = linked_counts_map[vertex]
            edge_chunk.put(edge_model)          
           
    
    edge_chunk.close()
    edge_chunk = None
    """


    cluster_chunker = Chunker()
    members_chunk = deque()
    
    member_model_chunk = Chunker()

    cluster_keyword_chunk = deque()
    member_positions_chunk = deque()
    keyword_model_chunk = Chunker()

    for cluster_id, cluster_members in taged.clusters.items():
        positions = get_position(index2sentiments=index2sentiments, cluster_members=cluster_members)
        member_positions_chunk.append(positions)
        cluster_model = cluster.Cluster()
        cluster_model.member_count = len(cluster_members)
        cluster_model.short_keywords = list(taged.tag_index[cluster_id])[:10]
    
        entities = cluster_chunker.put(cluster_model)
        cluster_keyword_chunk.append(taged.tag_index[cluster_id])
        members_chunk.append(cluster_members)
        
        
        if entities != None:
            _put_cluster_data(
                entities=entities,
                members_chunk=members_chunk,
                cluster_keyword_chunk=cluster_keyword_chunk,
                index2id=index2id,
                linked_counts_map=linked_counts_map,
                member_model_chunk=member_model_chunk,
                index2published=index2published,
                taged=taged,
                keyword_model_chunk=keyword_model_chunk,
                member_positions_chunk=member_positions_chunk

            )
            members_chunk = deque()
            cluster_keyword_chunk = deque()
            member_positions_chunk = deque()
                      
            
           
    entities = cluster_chunker.close()
    if entities != None:
        _put_cluster_data(
            entities=entities,
            members_chunk=members_chunk,
            cluster_keyword_chunk=cluster_keyword_chunk,
            index2id=index2id,
            linked_counts_map=linked_counts_map,
            member_model_chunk=member_model_chunk,
            index2published=index2published,
            taged=taged,
            keyword_model_chunk=keyword_model_chunk,
            member_positions_chunk=member_positions_chunk
        )
        members_chunk = deque()
        keyword_chunk = deque()
        member_positions_chunk = deque()
    member_model_chunk.close()
    keyword_model_chunk.close()

    index = 0
    model = Model()
    keyword_chunk = Chunker()
    
    for vector, sentimentResult, keywords, data in datas:
        
        id = index2id[index]
        link_to = [index2id[to_index] for to_index in taged.graph[index]]
        linked_count = linked_counts_map[id]
        model.save(id=id, data=data, vector=vector, sentiment_result=sentimentResult,linked_to=link_to, linked_count=linked_count)
        for keyword in keywords:
            keyword_model = text_keyword.TextKeyword()
            keyword_model.published = data.published
            keyword_model.linked_count = linked_count
            keyword_model.keyword = keyword
            keyword_model.text_id = id
            keyword_chunk.put(keyword_model)
        index += 1
            
           
    
    entities = model.finish()
    keyword_chunk.close()
    
   

    

def _put_cluster_data(
        entities, 
        members_chunk, 
        cluster_keyword_chunk, 
        index2id, 
        linked_counts_map, 
        member_model_chunk:Chunker, 
        index2published,
        taged,
        keyword_model_chunk:Chunker,
        member_positions_chunk:deque
        
    ):
    
    for entity, members, keywords, positions in zip(entities, members_chunk, cluster_keyword_chunk, member_positions_chunk):
            
        for member, position in zip(members, positions):
            member_model =  cluster_member.ClusterMember()
            member_model.cluster_id = entity.id
            member_model.text_id = index2id[member]
            linked_count = linked_counts_map[member]
            published = index2published[member]
            member_model.linked_count = linked_count
            member_model.published = published
            member_model.position = position
           
            member_model_chunk.put(member_model)
        for keyword in keywords:
            keyword_model =  cluster_keyword.ClusterKeyword()
            keyword_model.keyword = keyword
            keyword_model.cluster_id = entity.id
            keyword_model_chunk.put(keyword_model)
        