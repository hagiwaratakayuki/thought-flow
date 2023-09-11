import os, logging
logging.basicConfig(level=logging.INFO)
from gensim.models import KeyedVectors
import datetime



class Vectaizer:
    _model:KeyedVectors
    def __init__(self, filepath, basepath=os.getcwd()) -> None:
        targetpath = os.path.join(basepath , filepath)
        self._model:KeyedVectors = KeyedVectors.load_word2vec_format(targetpath)
        logging.info('model load ' + targetpath)
       

        
    def exec(self, word):
        if word in self._model:
            return self._model[word]
        return False
    def exec_dict(self, words):
        return {k:self._model[k] for k in words}
    
class