from typing import Iterable
from doc2vec.indexer.cls import Indexer
from doc2vec.tokenaizer.nltk_tokenaizer import NLTKTokenazer
from multiprocessing import Pool
import multiprocessing as multi
from doc2vec.vectaizer.gensim_fasttext import Vectaizer, MODEL_PATH
from doc2vec.sentiment.nltk_analizer import NLTKAnalizer
from collections import deque

from dto import DTO


class Doc2Vec:
    def __init__(self, modelfile:str = MODEL_PATH, workers:int = multi.cpu_count()) -> None:
        tokenaizer = NLTKTokenazer()
        vectaizer = Vectaizer(modelfile)
        analizer = NLTKAnalizer()
        self._workers = workers
        self._indexer = Indexer(tokenaizer=tokenaizer, vectaizer=vectaizer, sentimentAnalyzer=analizer)
    
    def exec(self, datas:Iterable[DTO]):
        ret = deque()
        with Pool(self._workers) as p:
            for r in p.imap_unordered(self._callIndexer, datas):
                ret.append(r)
            return ret


        
      

    def _callIndexer(self, data:DTO):
        ret = list(self._indexer.exec(data.body))
        ret.append(data)
        return ret
        