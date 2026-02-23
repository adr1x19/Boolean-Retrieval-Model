import math
import os
import matplotlib.pyplot as plt
from collections import defaultdict
from inverted_index import create_inverted_index,save_index_to_disk,load_index_from_disk
from preprocessing import tokenization
from pathlib import Path

inverted_index_file=Path("inverted_index.json")
if(inverted_index_file.is_file()):
    print("Loading from index...\n")
    inverted_index=load_index_from_disk("inverted_index.json")
else:
    print("Creating the index...\n")
    inverted_index=create_inverted_index("data/hindi/")
    save_index_to_disk(inverted_index)

def data_extraction(inverted_index):
    freq_arr = defaultdict(int)
    for term, postings in inverted_index.items():
        total_freq = 0
        for doc_id, val in postings.items():
            total_freq += val[0]
        freq_arr[term] = total_freq
        
    sorted_items = sorted(freq_arr.items(), key=lambda item: item[1], reverse=True)
    return dict(sorted_items)

def plot_zipfs_law(freq_data):
    frequencies = list(freq_data.values())
    ranks = list(range(1, len(frequencies) + 1))
    
    log_ranks = [math.log10(r) for r in ranks]
    log_freqs = [math.log10(f) for f in frequencies]
    
    plt.figure(figsize=(8, 5))
    plt.plot(log_ranks, log_freqs, marker='o', linestyle='-')
    plt.title("Zipf's Law")
    plt.xlabel("Log10(Rank)")
    plt.ylabel("Log10(Frequency)")
    plt.grid(True)
    plt.savefig("zipfs_law_plot.png")
    plt.close()

def plot_heaps_law(folder_path):
    total_tokens = 0
    vocabulary = set()
    
    tokens_history = []
    vocab_history = []
    
    files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    for file in files:
        file_path = os.path.join(folder_path, file)
        words = tokenization(file_path)
        for word in words:
            total_tokens += 1
            vocabulary.add(word)
            
            if total_tokens % 50 == 0:
                tokens_history.append(total_tokens)
                vocab_history.append(len(vocabulary))
                
    if total_tokens > 0 and (not tokens_history or tokens_history[-1] != total_tokens):
        tokens_history.append(total_tokens)
        vocab_history.append(len(vocabulary))

    if not tokens_history:
        return

    log_tokens = [math.log10(t) for t in tokens_history]
    log_vocab = [math.log10(v) for v in vocab_history]
    
    plt.figure(figsize=(8, 5))
    plt.plot(log_tokens, log_vocab, marker='o', linestyle='-')
    plt.title("Heaps' Law")
    plt.xlabel("Log10(Total Tokens)")
    plt.ylabel("Log10(Vocabulary Size)")
    plt.grid(True)
    plt.savefig("heaps_law_plot.png")
    plt.close()

if __name__ == "__main__":
    freq_data = data_extraction(inverted_index)
    
    plot_zipfs_law(freq_data)
    plot_heaps_law("data2/")