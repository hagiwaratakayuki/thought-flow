import random, string
from logic.save import buildModel, _save
import numpy as np
from dto import DTO
from doc2vec.indexer.dto import build_mock_sentiment_result 



 
def main():
    keyword_map = [
            ''.join([random.choice(string.ascii_letters + string.digits) for i in range(random.randint(1, 10))])
            for n in range(random.randint(5, 20))
            
    ]
    keywords_len = len(keyword_map)
    keywords_indexs_count = keywords_len -1
    n_samples = 100
    keywords = [
            
            [ keyword_map[random.randint(0, keywords_indexs_count)] for n in range(random.randint(1, keywords_len))]
            
            for i in range(n_samples)
    ]
    datas = [DTO(body='', title='', data={}) for i in range(n_samples)]
    vectors = np.random.rand(n_samples, 10)
    sentiments = [build_mock_sentiment_result(n_samples=n_samples, d1=10) for i in range(n_samples)]
       
        
       
    db_model = buildModel()
    
        
    print(_save(datas=zip(vectors, sentiments, keywords, datas), model=db_model)) 

if __name__ == 'main':
    main()