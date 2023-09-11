

from loader.loader import load
import numpy as np
from db import text, vertex, cluster, cluster_member, model as db_model
from multiprocessing import Pool
import multiprocessing as multi




def process():
    vectaizer = buildVectaizer()
    model = buildModel()
    return _process(loader=load, model=model, vectaizer=vectaizer)
            





class Model:

    def __init__(self) -> None:
        self._chunk = []
        self._vectotrs = []
        self._keywords = []

    def save(self, data, vector, sentimentresult, keyword):
        textEntity = text.Text()
        textEntity.setProperty('',  data.article, dict(vector=vector, sentiment=sentimentresult))
        self._vectotrs.append(vector)
        self._keywords.append(keyword)

        self._chunk.append(textEntity)
        self._vectotrs.append(vector)
        if len(self._chunk) < 30:
            return
        entities = db_model.put_multi(self._chunk)
        ret  = zip(self._vectotrs, self._keywords, entities)
        
        self._chunk = []
        self._vectotrs = []
        self._keywords = []

        return ret
    def finish(self):
        entities = db_model.put_multi(self._chunk)
        self._chunk = []
        return entities



def buildModel():
    return Model()
    

def buildVectaizer():
    pass

#ファイルを読む
#パース
#クラスタリング　+ キーワード抽出
#保存

def _process(loader, model:Model, vectaizer, workers=multi.cpu_count()):
    datas = loader()
    tags_map = {}
    index2id = {}
    
    vectors_map = {}
    index = 0
    
    shape = [0, 0]
    is_first = True
    for vector, sentimentResults, keywords, data in vectaizer.exec(datas):
        result = model.save(data, vector, sentimentResults, keywords)
        if result == None:
            continue
        
        for vec, keywords,entity  in result:
            if is_first == True:
                is_first = False
                shape[1] = vec.shape[1] 
            vectors_map[index] = vec
            index2id[index] = entity.id
            vectors_map[index] = vec
            tags_map[index] = keywords
            index +=1    


            

    result = model.finish()
   
    for vec, keywords,entity  in result:
        if is_first == True:
            is_first = False
            shape[1] = vec.shape[1]  
        vectors_map[index] = vec
        index2id[index] = entity.id
        vectors_map[index] = vec
        tags_map[index] = keywords
        index +=1
    shape[0] = index

    vectors = np.zeros(shape=shape)
    for i, v in vectors_map.items():
        vectors[i] = v

    