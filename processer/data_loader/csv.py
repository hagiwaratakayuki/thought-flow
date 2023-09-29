import csv
from data_loader.dto import BaseDataDTO
from typing import Callable



def load(columnmap:BaseDataDTO, path:str, skipfirst:bool=True):
    is_first = False
    with open(path) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            values = {}
            for k in [k for k in dir(columnmap) if k.find('_') != 0]:
                i = getattr(columnmap, k)
                if skipfirst == True and is_first == True:
                    is_first = False
                    continue                    
                if isinstance(i, int):
                    values[k] = row[i]
                
                if isinstance(i, Callable):
                    values[k] = i(row)
            dto = BaseDataDTO(**values)
            yield dto
