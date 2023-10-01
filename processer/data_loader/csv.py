import csv
from data_loader.dto import BaseDataDTO
from typing import Callable
from datetime import datetime




def load(columnmap:BaseDataDTO, path:str, published_pattern: str | Callable,  skipfirst:bool=True):
    is_first = False

    if isinstance(published_pattern, str):
        str2datetime = lambda x: datetime.strptime(x, published_pattern)
    else:
        str2datetime = published_pattern
    with open(path) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            values = {}
            if skipfirst == True and is_first == True:
                is_first = False
                continue    
            for k in [k for k in dir(columnmap) if k.find('_') != 0]:
                i = getattr(columnmap, k)
                               
                if isinstance(i, int):
                    value = row[i]
                
                if isinstance(i, Callable):
                    value = i(row)
                if k == 'published':

                    value = str2datetime(value) #type: ignore
            dto = BaseDataDTO(**values)
            yield dto
