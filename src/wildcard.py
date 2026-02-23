import os
from collections import defaultdict
from inverted_index import create_inverted_index
from query_processor import process_query
from pathlib import Path
from query_processor import save_index_to_disk, load_index_from_disk, measure_query_time
import re

def k_gramIndex(inverted_index, k):
    k_gram_index = defaultdict(list)
    for key in inverted_index.keys():
        s = "$" + key + "$"
        for i in range(len(s) - k + 1):
            st = s[i:i+k]
            k_gram_index[st].append(key)
    return k_gram_index


def k_gramQueries(word, k, k_gram_index):
    ans = None 
    t_slice = ("$" + word + "$").strip().split("*")
    
    for spl in t_slice:
        if spl == "$" or len(spl) < k:
            continue
    
        for i in range(len(spl) - k + 1):
            st = spl[i:i+k]
            current_matches = set(k_gram_index.get(st, []))
            
            if ans is None:
                ans = current_matches
            else:
                ans = ans & current_matches

    if ans is None or len(ans) == 0:
        return []
    
    final_ans = []
    regex_pattern = '^' + word.replace('*', '.*') + '$'
    
    for t in ans:
        if re.match(regex_pattern, t):
            final_ans.append(t)
            
    return final_ans


if __name__ == "__main__":
    user_input = "सन्द*"
    
    inverted_index_file = Path("inverted_index.json")
    if inverted_index_file.is_file():
        print("Loading from index...\n")
        inverted_index = load_index_from_disk("inverted_index.json")
    else:
        print("Creating the index...\n")
        inverted_index = create_inverted_index("data/hindi/")
        save_index_to_disk(inverted_index)
        
    k = 3
    k_gram_index = k_gramIndex(inverted_index, k)
    val = k_gramQueries(user_input, k, k_gram_index)
    
    if not val:
        print(f"No matches found for wildcard query: {user_input}")
    else:
        tokens = []
        for w in val:
            tokens.append(w)
            tokens.append(" OR ")
        
        if tokens:
            tokens.pop() 
        
        s = "".join(tokens)
        
        print(f"Original Query: {user_input}")
        print(f"Expanded Query: {s}")
        print("-" * 30)
        measure_query_time(s, inverted_index)
