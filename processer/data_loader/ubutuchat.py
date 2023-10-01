from data_loader.csv import load as csv_load
from data_loader.dto import BaseDataDTO

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
