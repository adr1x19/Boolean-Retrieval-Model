import re
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

def transliterate_to_hindi(query, scheme=sanscript.ITRANS):
    if re.search(r'[A-Za-z]', query):
       
        tokens = query.split()
        converted_tokens = []
        
        for token in tokens:
            if token in ["AND", "OR", "NOT"]:
                converted_tokens.append(token)
            else:
               
                hindi_word = transliterate(token, scheme, sanscript.DEVANAGARI)
                converted_tokens.append(hindi_word)
                
        return " ".join(converted_tokens)
    

    return query


if __name__ == "__main__":
    
   
    chat_query = "internet"
    print("Original:", chat_query)
    print("ITRANS:  ", transliterate_to_hindi(chat_query, sanscript.ITRANS))
    
    print("-" * 40)
    hk_query = "internet"
    print("Original:", hk_query)
    print("HK:      ", transliterate_to_hindi(hk_query, sanscript.HK))
