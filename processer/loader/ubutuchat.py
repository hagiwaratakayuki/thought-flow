from loader.csv import load as csv_load

def ubuntu_load(path):
    columnmap = {
        'body':5, 
        'data':_get_data,
        
    }
    return csv_load(columnmap=columnmap, path=path)

def _get_data(row:list):
    return {
        'from':row[3],
        'to':row[4] or '',
        'date':row[2]
    }
