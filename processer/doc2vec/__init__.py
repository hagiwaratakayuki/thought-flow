from typing import Iterable
from indexer.cls import Indexer
from tokenaizer.nltk_tokenaizer import NLTKTokenazer
from multiprocessing import Pool
import multiprocessing as multi
from vectaizer.gensim_fasttext import Vectaizer
from sentiment.nltk_analizer import NLTKAnalizer

from dto import DTO


class Doc2Vec:
    def __init__(self, modelfile:str = 'example/fasttext_model/wiki-news-300d-1M.vec', workers:int = multi.cpu_count()) -> None:
        tokenaizer = NLTKTokenazer()
        vectaizer = Vectaizer(modelfile)
        analizer = NLTKAnalizer()
        self._workers = workers
        self._indexer = Indexer(tokenaizer=tokenaizer, vectaizer=vectaizer, sentimentAnalyzer=analizer)
    
    def exec(self, datas:Iterable[DTO]):
        
        p = Pool(self._workers)
        for response in p.imap_unordered(self._callIndexer, datas):
            yield response
        
        p.close()

    def _callIndexer(self, data:DTO):
        ret = list(self._indexer.exec(data.body))
        ret.append(data)
        return ret
        