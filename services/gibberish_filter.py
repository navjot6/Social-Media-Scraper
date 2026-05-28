import re 
from langdetect import detect 
def is_gibberish(text): 
    try: 
        if len(text.split()) < 3: 
            return True 
        weird = re.findall(r'[^\\w\\s]', text) 
        if len(weird) > 20: 
            return True 
        detect(text) 
        return False 
    except: 
        return True