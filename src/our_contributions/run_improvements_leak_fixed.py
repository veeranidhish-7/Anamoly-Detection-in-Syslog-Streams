import os
import sys
import copy
import numpy as np
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import KFold
import pickle
from gensim.models import Word2Vec

# Add the our_contributions models folder to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from models.deep_learning import AutoencoderModel
from models.thresholding import compute_threshold_pot

os.makedirs("saved_models_our_contributions", exist_ok=True)

BGL_SEQUENCES = "data/BGL/preprocessed/bgl_sequences.pkl"

def get_mean_w2v(sequences, w2v_model):
    vector_size = w2v_model.vector_size
    X_w2v = np.zeros((len(sequences), vector_size), dtype=np.float32)
    for i, seq in enumerate(sequences):
        if len(seq) == 0:
            continue
        vecs = [w2v_model.wv[token] for token in seq if token in w2v_model.wv]
        if vecs:
            X_w2v[i] = np.mean(vecs, axis=0)
    
    # L2 normalize
    norms = np.linalg.norm(X_w2v, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return X_w2v / norms

def run_bgl_autoencoder_leak_fixed():
    print(f"{'='*80}")
    print(f"Our Contribution 2 FIXED: BGL Autoencoder (Node-Based Semantic Word2Vec - NO DATA LEAK)")
    print(f"{'='*80}")
    
    with open(BGL_SEQUENCES, 'rb') as f:
        data = pickle.load(f)
    
    sequences = np.array(data['sequences'], dtype=object)
    y = data['y']
    
    normal_idx = np.where(y == 0)[0]
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    metrics = {"p": [], "r": [], "f1": []}
    
    model = AutoencoderModel(hidden_layer_sizes=(16, 8, 16))
    fold = 1
    
    for fit_idx, test_normal_idx in kf.split(normal_idx):
        print(f"\n--- Fold {fold} ---")
        train_normal_idx = normal_idx[fit_idx]
        test_idx = np.concatenate([normal_idx[test_normal_idx], np.where(y == 1)[0]])
        
        train_sequences = sequences[train_normal_idx].tolist()
        test_sequences = sequences[test_idx].tolist()
        y_test = y[test_idx]
        
        print(f"Training Word2Vec purely on {len(train_sequences)} normal sequences (No Data Leak)...")
        w2v_model = Word2Vec(sentences=train_sequences, vector_size=32, window=5, min_count=1, workers=4, sg=1)
        
        print("Extracting features...")
        Xf = get_mean_w2v(train_sequences, w2v_model)
        Xt = get_mean_w2v(test_sequences, w2v_model)
        
        fold_model = copy.deepcopy(model)
        print(f"Fitting Autoencoder on {len(Xf)} sequences...")
        fold_model.fit(Xf)
        
        ef = fold_model.predict_errors(Xf)
        et = fold_model.predict_errors(Xt)
        
        theta = compute_threshold_pot(ef, q=0.90, target_fpr=1e-3)
        y_pred = (et > theta).astype(int)
        
        p, r, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='binary', zero_division=0)
        print(f"Fold {fold}: P: {p*100:.2f}%, R: {r*100:.2f}%, F1: {f1*100:.2f}% (Threshold: {theta:.4f})")
        
        metrics["p"].append(p); metrics["r"].append(r); metrics["f1"].append(f1)
        fold += 1

    print("-" * 80)
    print(f"FINAL LEAK-FREE BGL AUTOENCODER RESULT:")
    print(f"Precision: {np.mean(metrics['p'])*100:.2f}% ± {np.std(metrics['p'])*100:.2f}%")
    print(f"Recall:    {np.mean(metrics['r'])*100:.2f}% ± {np.std(metrics['r'])*100:.2f}%")
    print(f"F1 Score:  {np.mean(metrics['f1'])*100:.2f}% ± {np.std(metrics['f1'])*100:.2f}%")

if __name__ == "__main__":
    run_bgl_autoencoder_leak_fixed()
