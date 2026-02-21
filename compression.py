import os
from inverted_index import create_inverted_index

def vb_encode_number(n):
    bytes_list = []
    while True:
        bytes_list.insert(0, n & 127) 
        if n < 128:
            break
        n >>= 7 
    bytes_list[-1] += 128 
    return bytes_list

def compress_postings(doc_ids):
    if not doc_ids:
        return []
    
    gaps = [doc_ids[0]]
    for i in range(1, len(doc_ids)):
        gaps.append(doc_ids[i] - doc_ids[i - 1])
        
    compressed_bytestream = bytearray()
    for gap in gaps:
        compressed_bytestream.extend(vb_encode_number(gap))
        
    return compressed_bytestream

def measure_index_compression(inverted_index):
    total_uncompressed_bytes = 0
    total_compressed_bytes = 0
    
    compressed_index = {}

    for term, postings_dict in inverted_index.items():
        doc_ids = sorted(list(postings_dict.keys()))
        
        uncompressed_size = len(doc_ids) * 4
        total_uncompressed_bytes += uncompressed_size
        
        compressed_bytes = compress_postings(doc_ids)
        total_compressed_bytes += len(compressed_bytes)
        
        compressed_index[term] = bytes(compressed_bytes)

    compression_ratio = total_uncompressed_bytes / total_compressed_bytes if total_compressed_bytes > 0 else 0

    print("-" * 40)
    print("INDEX COMPRESSION REPORT (Variable-Byte)")
    print("-" * 40)
    print(f"Original Size (32-bit ints): {total_uncompressed_bytes} bytes")
    print(f"Compressed Size (VB Encoded):  {total_compressed_bytes} bytes")
    print(f"Space Saved:                   {total_uncompressed_bytes - total_compressed_bytes} bytes")
    print(f"Compression Ratio:             {compression_ratio:.2f}:1")
    print("-" * 40)
    
    return compressed_index

if __name__ == "__main__":
    inverted_index = create_inverted_index("data/")
    compressed_index = measure_index_compression(inverted_index)