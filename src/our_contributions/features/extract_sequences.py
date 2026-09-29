import os
import pandas as pd
import numpy as np
import pickle

HDFS_TRACES = "data/HDFS_v1/preprocessed/Event_traces.csv"
HDFS_OUTPUT = "data/HDFS_v1/preprocessed/hdfs_sequences.pkl"

BGL_STRUCTURED = "data/BGL/preprocessed/BGL.log_structured.csv"
BGL_OUTPUT = "data/BGL/preprocessed/bgl_sequences.pkl"

def extract_hdfs_sequences():
    print(f"\n--- Processing HDFS Sequences ---")
    if not os.path.exists(HDFS_TRACES): return
    df = pd.read_csv(HDFS_TRACES)
    
    sequences = []
    for seq_str in df['Features']:
        seq_str = seq_str.strip('[]').replace(' ', '')
        tokens = seq_str.split(',') if seq_str else []
        sequences.append(tokens)
        
    y = (df['Label'] != 'Success').astype(int).values
    
    with open(HDFS_OUTPUT, 'wb') as f:
        pickle.dump({'sequences': sequences, 'y': y}, f)
    print(f"Saved {len(sequences)} HDFS sequences.")

def extract_bgl_sequences():
    print(f"\n--- Processing BGL Sequences ---")
    if not os.path.exists(BGL_STRUCTURED): return
    df = pd.read_csv(BGL_STRUCTURED)
    
    window_size_seconds = 6 * 60 * 60
    df['Window_ID'] = df['Timestamp'] // window_size_seconds
    df['Label_Bin'] = df['Label'].apply(lambda x: 0 if x == '-' else 1)
    
    grouped = df.groupby(['Node', 'Window_ID'])
    sequences = grouped['EventId'].apply(list).values
    y = grouped['Label_Bin'].max().values
    
    with open(BGL_OUTPUT, 'wb') as f:
        pickle.dump({'sequences': sequences, 'y': y}, f)
    print(f"Saved {len(sequences)} BGL sequences.")

if __name__ == "__main__":
    extract_hdfs_sequences()
    extract_bgl_sequences()
