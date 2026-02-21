import os
from collections import defaultdict
from inverted_index import create_inverted_index
from query_processor import process_query

inverted_index=create_inverted_index("data2/")
def k_gramIndex(inverted_index,k):
    k_gram_index=defaultdict(list)
    for key in inverted_index.keys():
        s="$"+key+"$"
        slice=[]
        for i in range(len(s)-k+1):
            st=s[i:i+k]
            
            k_gram_index[st].append(key)
        
    return (k_gram_index)


def k_gramQueries(word, k, k_gram_index):
    ans = None 
    
    t_slice=("$"+word+"$").strip().split("*")
    
    print(t_slice)

    for spl in t_slice:
        if spl=="$":
            continue
    
        for i in range(len(spl) - k + 1):
            st = spl[i:i+k]
            current_matches = set(k_gram_index[st])
            
            if ans is None:
                ans = current_matches
            else:
                ans = ans & current_matches

        
    return list(ans) if ans is not None else []




if __name__=="__main__":
    user_input="सन्द*"
    k=3
    k_gram_index=k_gramIndex(inverted_index,k)
    val=k_gramQueries(user_input,k,k_gram_index)
    tokens=[]
    for w in val:
        tokens.append(w)
        tokens.append(" OR ")
    
    tokens.pop()
    s=""
    for t in tokens:
        s=s+t
    print(process_query(s,inverted_index))
        
    