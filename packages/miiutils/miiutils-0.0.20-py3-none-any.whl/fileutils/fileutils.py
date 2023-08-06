import json
from os import path
from munch import Munch

def loadFile(file):
    if not file or not path.exists(file):
        return None

    with open(file, 'r') as f:
        return f.read() 

def jsonFileToDct(file):
    if not file or not path.exists(file):
        return None

    with open(file, 'r') as f:
        return json.load(f)  
    
def jsonFileToObj(file):
    dct = jsonFileToDct(file)  
    
    return Munch.fromDict(dct) if dct else None    

def dctToFile(dct, file):
    with open(file, 'w') as f:     
        f.write(json.dumps(dct, sort_keys=False, indent=4)) 

def fileSize(file):
    if not file or not path.exists(file):
        return -1
    return path.getsize(file)     
