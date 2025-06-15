import json

def jsonDump(data) :
    return json.dumps(data, ensure_ascii=False) 
