import re
from collections import defaultdict
import os 
from preprocessing import tokenization,normalization,stemmer,is_stopword
from inverted_index import create_inverted_index
#implement the query 
inverted_index=create_inverted_index("data/")


def optimized_sort(phrase):
    pass
    
def shunting_yard(phrase,inverted_index,docs):

    precedence_table={
        "NOT":3,
        "AND":2,
        "OR":1
    }
    pattern=r"[\u0900-\u0963\u0966-\u097F]+|AND|OR|NOT"
    raw_tokens=re.findall(pattern,phrase)
    tokens=[]
    for token in raw_tokens:
        if is_stopword(token):
            tokens.append(stemmer(normalization(token)))

    print(tokens)
    output=[]
    opstack=[]
    for t in tokens:
        if t in precedence_table:
            
            while len(opstack)>0:
                op=opstack[-1]
                if(precedence_table[t]>precedence_table[op]):
                    break
                opstack.pop()
                output.append(op)
            opstack.append(t)
                    
        else:
            output.append(t)
    

    while len(opstack)>0:
        output.append(opstack.pop())
    
    # solve the boolean query 
    res=[]
    print(output)
    for t in output:
        if t in precedence_table:
            ans=[]
            if(t=="NOT"):
                
                first=res.pop()
                for i in range(1,docs+1):
                    if i not in first:
                        ans.append(i)
                
                res.append(ans)
            
            if(t=="AND"):
                first=res.pop()
                second=res.pop()
                for i in first:
                    if i in second:
                        
                        ans.append(i)
                res.append(ans)
            
            if(t=="OR"):
                first=res.pop()
                second=res.pop()
                
                for i in first:
                    ans.append(i)
                for i in second:
                    if i not  in first:
                        ans.append(i)
                
                res.append(ans)

            
        else:
           # print(list(inverted_index[t].keys()))
            res.append(list(inverted_index[t].keys()))
    
    return res
            




    
    
    


def process_query(user_input,inverted_index):
    
    all_docs = set()
    for doc_dict in inverted_index.values():
        all_docs.update(doc_dict.keys())

    docs=len(all_docs)
    
    pattern="AND|OR|NOT"

    if re.search(pattern,user_input):
        #print("Boolean Query")
        return list(shunting_yard(user_input,inverted_index,docs)[0])
      
        

    else:
       # print("Phrase Query")
        word_pattern = r"[\u0900-\u0963\u0966-\u097F]+"
        raw_tokens=re.findall(word_pattern,user_input)
        tokens=[]
        for token in raw_tokens:
            if is_stopword(token):
                tokens.append(stemmer(normalization(token)))
        
        if not tokens:
            return []
        ans=set()
        first_word = tokens[0]
        if first_word not in inverted_index:
            return []

        local_list = inverted_index[first_word]
        for doc_id, posting in local_list.items():
            positions=posting[1]
            for pos in positions:
                base_pos=pos[0]
                is_phrase_match=True
                for i in range(1,len(tokens)):

                    next_word = tokens[i]
                    expected_pos = base_pos + i 
                    
                   
                    if doc_id not in inverted_index.get(next_word, {}):
                        is_phrase_match = False
                        break
                        
                   
                    next_word_posting = inverted_index[next_word][doc_id]
                    next_word_positions = next_word_posting[1]
                    
                    
                    found_exact_pos = False
                    for next_pos_data in next_word_positions:
                        if next_pos_data[0] == expected_pos:
                            found_exact_pos = True
                            break 

                    if not found_exact_pos:
                        is_phrase_match = False
                        break 
                if is_phrase_match:
                    ans.add(doc_id)
                    break

                
        return list(ans)
        
      







if __name__=="__main__":
    user_input="इंटरनेट "
    #print(process_query(user_input,inverted_index))
    print(process_query(user_input,inverted_index))