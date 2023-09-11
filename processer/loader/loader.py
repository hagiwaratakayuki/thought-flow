import os, re

voidline = re.compile('\n{2}')
article_pt = re.compile("writes:$", re.MULTILINE)
quote_pt = re.compile(r'^\s*>+\s*')


def load(target_dir:str):
    files = list_files(target_dir=target_dir).keys()
    for file in files:
        with open(file, mode='r', encoding='utf-8') as f:
            text = f.read()
            splited = voidline.split(text)
           
            header_text = splited[0]
           
           
            header = {k.strip():v.strip() for k, v  in [line.split(':', 1) for line in header_text.splitlines()]}
            article = None
            body = None

            if len(splited) > 2:
                canditate = splited[1]
               
                if not quote_pt.search(canditate) and article_pt.search(canditate):
                    article = canditate

            if not article:
                body = '\n\n'.join(splited[1:])
            else:
                body = '\n\n'.join(splited[2:])
            cleanuped = '\n'.join(filter(lambda l: not quote_pt.search(l), body.splitlines()))
            splited_path = file.split(os.sep)
            category = splited_path[1]
            number = splited_path.pop().split('.')[0]
            yield dict(
                    article=article, 
                    body=body, 
                    header=header, 
                    header_text=header_text, 
                    cleanuped=cleanuped,
                    category=category,
                    number=number

                )





def list_files(target_dir):
    index = 0
    cursor = 0
    paths = {}
    paths[index] = target_dir
    index += 1
    
    
    
    res = {}
    while cursor < index:
        
        _target = paths[cursor]
        cursor += 1
        scaned = os.scandir(_target)
        for entry in scaned:
            
            if entry.is_file():
                
                res[entry.path] = (_target, entry.name,)
            elif entry.is_dir():
                paths[index] = os.path.relpath(entry.path)
                index += 1
        scaned.close()
        
    return res
