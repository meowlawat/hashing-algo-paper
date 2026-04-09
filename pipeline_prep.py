import random
import re
from collections import Counter
import os

# --- Configuration ---
RAW_FILE = 'rockyou_1.txt' # Using your exact downloaded file name
TOTAL_PULL = 2000000       # The initial random slice
VAL_SIZE = 100000          # The sequestered validation set

def build_datasets():
    print("[*] Initiating Phase 1: Data Ingestion & Sanitization...")
    
    try:
        with open(RAW_FILE, 'r', encoding='latin-1') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[!] Error: {RAW_FILE} not found.")
        return None

    print(f"[*] Raw dataset loaded: {len(lines):,} total lines.")
    random.seed(42) 
    random.shuffle(lines)
    
    sampled_lines = lines[:TOTAL_PULL]
    print(f"[*] Sliced {TOTAL_PULL:,} random lines for processing.")

    clean_passwords = []
    ascii_regex = re.compile(r'^[\x20-\x7E]+$') 
    
    for line in sampled_lines:
        pwd = line.strip()
        if 8 <= len(pwd) <= 24 and ascii_regex.match(pwd):
            clean_passwords.append(pwd)

    print(f"[*] Sanitization complete. Usable credentials: {len(clean_passwords):,}")

    validation_set = clean_passwords[:VAL_SIZE]
    training_pool = clean_passwords[VAL_SIZE:]
    
    dataset_a_realistic = training_pool                 
    dataset_b_structural = list(set(training_pool))     

    with open('validation_set.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(validation_set))
        
    with open('dataset_A_realistic.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(dataset_a_realistic))
        
    with open('dataset_B_structural.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(dataset_b_structural))

    print(f"[*] Dataset A saved: {len(dataset_a_realistic):,} credentials.")
    print(f"[*] Dataset B saved: {len(dataset_b_structural):,} credentials.")
    print(f"[*] Validation Lockbox saved: {len(validation_set):,} credentials.")
    
    return dataset_a_realistic

def build_pcfg_model(dataset_a):
    print("\n[*] Initiating Phase 2: PCFG Structural Mapping...")
    structures = []
    
    for pwd in dataset_a:
        struct = []
        for char in pwd:
            if char.isupper(): struct.append('U')
            elif char.islower(): struct.append('L')
            elif char.isdigit(): struct.append('D')
            else: struct.append('S')
        structures.append("".join(struct))
        
    pcfg_counts = Counter(structures)
    
    with open('pcfg_top_templates.txt', 'w', encoding='utf-8') as f:
        for struct, count in pcfg_counts.most_common(100):
            f.write(f"{struct}: {count}\n")
            
    print(f"[*] Extracted {len(pcfg_counts):,} unique structural templates.")
    print("[*] Top 3 most common structures:")
    for struct, count in pcfg_counts.most_common(3):
        print(f"    - {struct} ({count:,} occurrences)")

if __name__ == "__main__":
    dataset_a = build_datasets()
    if dataset_a:
        build_pcfg_model(dataset_a)
        print("\n[+] Pipeline Prep Complete. Ready for PyTorch LSTM.")