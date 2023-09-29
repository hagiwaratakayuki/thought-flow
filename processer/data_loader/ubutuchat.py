from data_loader.csv import load as csv_load
from data_loader.dto import BaseDataDTO

def ubuntu_load(path):
    columnmap = BaseDataDTO()
    columnmap.body = 5
    columnmap.data = _get_data
    columnmap.author = 3
    columnmap.authorid =

        
        
    
    return csv_load(columnmap=columnmap, path=path)

def _get_data(row:list):
    return {
        'from':row[3],
        'to':row[4] or '',
        
    }
