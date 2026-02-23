import re
import unicodedata

def stemmer(word):
    word = word.strip()
    suffixes = [
        (r'(ियां|ियों|ाएं)$', ''),  
        (r'(ों|एँ)$', ''),          
        (r'(ा|े|ी)$', '')          
    ]
    
    for pattern, replacement in suffixes:
        if re.search(pattern, word):
            return re.sub(pattern, replacement, word)
            
    return word

def normalization(word):
    word=word.strip()
    nukta_classes={
        'क़':'क',
        'ख़':'ख',
        'ग़':'ग',
        'ज़':'ज',
        'ड़': 'ड',
        'ढ़': 'ढ',
        'फ़':'फ',
        'य़': 'य'
    }
    word=unicodedata.normalize("NFC",word)
    word = word.replace('\u200d', '').replace('\u200c', '')    
    for key, value in nukta_classes.items(): 
        clean_key = unicodedata.normalize("NFC", key)
        word = re.sub(clean_key, value, word)
    word = re.sub(r"\u0901", "\u0902", word)
    return word
  
    
def is_valid_word(word):
    stopwords = [
    "के", "का", "की", "को", "में", "से", "ने", "पर",  
    "है", "हैं", "था", "थी", "थे", "हुआ", "हुए",    
    "और", "कि", "या", "तो", "भी", "ही",               
    "यह", "वह", "जो", "इस", "उस", "ये", "वे",         
    "नहीं", "कर", "लिए", "एक"                         
    ]
    if word not in stopwords:
        return True
    else:
        return False
    

def tokenization(filename):

    words=[]
    word_pattern = r"[\u0900-\u0963\u0966-\u097F]+"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip() 
                tokens = re.findall(word_pattern, line)
                
                for t in tokens:
                    t = normalization(t)
                    if is_valid_word(t):
                        t = stemmer(t)
                        if t:
                            words.append(t)
                            
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        
    return words



if __name__=="__main__":
   words= tokenization("data/0000.txt")
   print(words)

