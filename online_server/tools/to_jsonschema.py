from routing.return_models.cluster import overview as cluster_overview
from routing.return_models.cluster import overviews as  cluster_overviews
from routing.return_models.text import overview as text_overview
from routing.return_models.text import overviews as text_overviews
from routing import text, cluster
from pydantic import TypeAdapter, BaseModel
import os, json


def check_class(target):
    try:
        return issubclass(target, BaseModel)
    except Exception as e:
        return False
modules = [
    cluster,
    text,
    cluster_overview,
    cluster_overviews,
    text_overview,
    text_overviews
]


for module in modules:
    
    module_name = str(module.__name__) 
    for name in dir(module):
        if name.find('_') == 0 :
            continue
        target = getattr(module, name)

        if not hasattr(target, '__module__'):
            continue

        target_module_name = str(target.__module__)           
        if target_module_name != module_name or target_module_name.find('pydantic') != -1 or check_class(target) == False:
            continue
     
        adapter = TypeAdapter(target)
        file_name = os.path.abspath('../schema/' + name + '.json')        
        
    
        with open(file_name, "w") as f:
            json.dump(adapter.json_schema(), f, ensure_ascii=False)
  
            
        



