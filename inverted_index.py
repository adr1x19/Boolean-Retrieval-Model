from collections import defaultdict
import os
from preprocessing import tokenization, stemmer, normalization

def create_inverted_index(folder_path):
    inverted_index=defaultdict(dict)

    files=[f for f in os.listdir(folder_path) if f.endswith('.txt')]
    #print(files)
    counter=1
    mapfile=defaultdict(str)
    #always sort your filename gives a speed up when querying 

    for file in files:
        doc_id=counter
        local_dict= defaultdict(list)
        mapfile[doc_id]=file

        words=tokenization(folder_path+file)
        #print(f"For doc{doc_id}")
        pos=1
        for word in words:
            local_dict[word].append([pos,-1])
            pos=pos+1

        
        #implement skip pointers 
        for key, value in local_dict.items(): 
            l = int(len(value) ** 0.5)
            if l > 1:
                c = 0
                for item in value:
                    if c % l == 0:
                        if c + l < len(value):
                            item[1] = c+l
                    c = c + 1
                
        #print(local_dict)
        
    
        
        for word,count in local_dict.items():
            inverted_index[word][doc_id]=[len(count),count]
        counter=counter+1
    return inverted_index

#serialize the the inverted index 
import json
import os

def save_index_to_disk(inverted_index, filename="inverted_index.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(inverted_index, file, ensure_ascii=False, indent=4)
    print(f"Index successfully saved to {filename}")

def load_index_from_disk(filename="inverted_index.json"):
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        return {}
        
    with open(filename, "r", encoding="utf-8") as file:
        inverted_index = json.load(file)
        
    print(f"Index successfully loaded from {filename}")
    return inverted_index


if __name__=="__main__":
    # print(dict(mapfile))
    #print("Inverted Index:\n")
    for key,value in create_inverted_index("data/").items():
        
        if key==(stemmer(normalization("सैका"))):
            print(value.keys())

