import json, os
from dateutil import parser
from .dto import BaseDataDTO



def load(*args):
    
    with open('example/nasa_sti/parsed.json', encoding="utf-8") as fp:
        ret = [];
        for row in json.load(fp=fp):
            row['published'] = parser.parse(row['published'])
            ret.append(BaseDataDTO(**row))
        return ret
    
        

