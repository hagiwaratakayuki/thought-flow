from .model import Model
import json, numpy
from google.cloud.datastore import query


class WordToVec(Model):
    vector:str
    word:str
    def __init__(self, word:str, vector:numpy.ndarray) -> None:

        self._entity_options = { "exclude_from_indexes":("vecter",)}
        self.vector = json.dumps(vector.tolist()) 
        super(WordToVec, self).__init__(eid=word)

def get_vectors(words):
    
    chunked = [words[i:i + 100] for i in range(0, len(words), 100)]
    results = {}
    for chunk in chunked:
        wordtovec_query = WordToVec.query()

        or_filters = query.Or(
            [
                query.PropertyFilter("word", "=", word)
                for word in chunk
            
            ]
        )
        wordtovec_query.add_filter(filter=or_filters)
        results_chunk = wordtovec_query.fetch()
        for result in results_chunk:
            results[result['word']] = numpy.array(json.loads(result["vector"]))
     
    return results

         

    