import os
import sys
import copy
import numpy as np
import pickle
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from gensim.models import Word2Vec
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import KFold

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from models.thresholding import compute_threshold_pot

os.makedirs("saved_models_our_contributions", exist_ok=True)
BGL_SEQUENCES = "data/BGL/preprocessed/bgl_sequences.pkl"
MAX_LEN = 50
VECTOR_SIZE = 32

class LSTMAutoencoder(nn.Module):
    def __init__(self, seq_len, n_features, embedding_dim=16):
        super().__init__()
        self.seq_len = seq_len
        self.n_features = n_features
        self.embedding_dim = embedding_dim
        
        self.encoder = nn.LSTM(
            input_size=n_features,
            hidden_size=embedding_dim,
            num_layers=1,
            batch_first=True
        )
        
        self.decoder = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=n_features,
            num_layers=1,
            batch_first=True
        )
        
    def forward(self, x):
        _, (hidden_n, _) = self.encoder(x)
        encoded = hidden_n.permute(1, 0, 2).repeat(1, self.seq_len, 1)
        decoded, _ = self.decoder(encoded)
        return decoded

def get_seq_w2v(sequences, w2v_model, max_len=MAX_LEN):
    vector_size = w2v_model.vector_size
    X_seq = np.zeros((len(sequences), max_len, vector_size), dtype=np.float32)
    for i, seq in enumerate(sequences):
        if len(seq) == 0: continue
        vecs = [w2v_model.wv[token] for token in seq if token in w2v_model.wv]
        if vecs:
            length = min(len(vecs), max_len)
            X_seq[i, :length, :] = np.array(vecs)[:length]
    return X_seq

def train_lstm_ae(model, X_train, epochs=5, batch_size=256, device='cpu'):
    model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.MSELoss()
    dataset = TensorDataset(torch.tensor(X_train))
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    model.train()
    for epoch in range(epochs):
        epoch_loss = 0
        for batch in dataloader:
            x = batch[0].to(device)
            optimizer.zero_grad()
            outputs = model(x)
            loss = criterion(outputs, x)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        # print(f"Epoch {epoch+1}/{epochs} Loss: {epoch_loss/len(dataloader):.4f}")

def predict_lstm_errors(model, X, batch_size=256, device='cpu'):
    model.to(device)
    model.eval()
    dataset = TensorDataset(torch.tensor(X))
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
    
    errors = []
    with torch.no_grad():
        for batch in dataloader:
            x = batch[0].to(device)
            outputs = model(x)
            batch_errors = torch.mean((outputs - x)**2, dim=(1,2))
            errors.extend(batch_errors.cpu().numpy())
    return np.array(errors)

def run_lstm():
    print(f"{'='*80}")
    print(f"Deep Sequence Modeling: BGL LSTM Autoencoder (Leak-Free)")
    print(f"{'='*80}")
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    with open(BGL_SEQUENCES, 'rb') as f:
        data = pickle.load(f)
    
    sequences = np.array(data['sequences'], dtype=object)
    y = data['y']
    
    normal_idx = np.where(y == 0)[0]
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    metrics = {"p": [], "r": [], "f1": []}
    
    fold = 1
    for fit_idx, test_normal_idx in kf.split(normal_idx):
        print(f"\n--- Fold {fold} ---")
        train_normal_idx = normal_idx[fit_idx]
        test_idx = np.concatenate([normal_idx[test_normal_idx], np.where(y == 1)[0]])
        
        train_sequences = sequences[train_normal_idx].tolist()
        test_sequences = sequences[test_idx].tolist()
        y_test = y[test_idx]
        
        print("Training Word2Vec...")
        w2v_model = Word2Vec(sentences=train_sequences, vector_size=VECTOR_SIZE, window=5, min_count=1, workers=4, sg=1)
        
        print("Extracting sequential features...")
        Xf = get_seq_w2v(train_sequences, w2v_model, max_len=MAX_LEN)
        Xt = get_seq_w2v(test_sequences, w2v_model, max_len=MAX_LEN)
        
        model = LSTMAutoencoder(seq_len=MAX_LEN, n_features=VECTOR_SIZE, embedding_dim=16)
        
        print(f"Training LSTM Autoencoder on {len(Xf)} sequences...")
        train_lstm_ae(model, Xf, epochs=5, batch_size=1024, device=device)
        
        print("Predicting errors...")
        ef = predict_lstm_errors(model, Xf, batch_size=1024, device=device)
        et = predict_lstm_errors(model, Xt, batch_size=1024, device=device)
        
        theta = compute_threshold_pot(ef, q=0.90, target_fpr=1e-3)
        y_pred = (et > theta).astype(int)
        
        p, r, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='binary', zero_division=0)
        print(f"Fold {fold}: P: {p*100:.2f}%, R: {r*100:.2f}%, F1: {f1*100:.2f}% (Threshold: {theta:.4f})")
        
        metrics["p"].append(p); metrics["r"].append(r); metrics["f1"].append(f1)
        fold += 1

    print("-" * 80)
    print(f"FINAL LSTM AUTOENCODER RESULT:")
    print(f"Precision: {np.mean(metrics['p'])*100:.2f}% ± {np.std(metrics['p'])*100:.2f}%")
    print(f"Recall:    {np.mean(metrics['r'])*100:.2f}% ± {np.std(metrics['r'])*100:.2f}%")
    print(f"F1 Score:  {np.mean(metrics['f1'])*100:.2f}% ± {np.std(metrics['f1'])*100:.2f}%")

if __name__ == "__main__":
    run_lstm()
