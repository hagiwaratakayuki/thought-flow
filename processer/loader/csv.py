import csv
from dto import DTO
from typing import Callable


def load(columnmap:dict, path:str, skipfirst:bool=True):
    is_first = False
    with open(path) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            values = {}
            for k, i in columnmap.items():
                if skipfirst == True and is_first == True:
                    is_first = False
                    continue                    
                if isinstance(i, int):
                    values[k] = row[i]
                
                if isinstance(i, Callable):
                    values[k] = i(row)
            dto = DTO(**values)
            yield dto
