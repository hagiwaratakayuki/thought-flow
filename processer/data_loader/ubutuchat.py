from data_loader.csv import load as csv_load
from data_loader.dto import BaseDataDTO
import hashlib
def ubuntu_load(path):
    columnmap = BaseDataDTO()
    columnmap.body = 5
    columnmap.data = _get_data
    columnmap.author = 3
    columnmap.authorid = 3


        
        
    
    return csv_load(columnmap=columnmap, published_pattern="%Y-%m-%dT%H:%M:%S.%fZ", path=path)

def _get_data(row:list):
    return {
        'to':row[4] or '',
        'dialogueid':row[1]

    }
def get_id(row:list):
    id_binary = '/'.join([row[5] , row[3]]).encode('utf-8')
    return hashlib.md5(id_binary).hexdigest
