"""
Final Attempt 2: Contaminated Setup Protocol with L2-Normalized Raw Counts

Since TF-IDF completely failed to match the trajectories (RPCA F1 was ~60% instead 
of ~82%), we are switching to L2-normalized raw counts, which we previously proved
is the ONLY feature space that matches the paper's PCA baseline.

Run from project root: python src/final_contaminated_setup_l2.py
"""
import numpy as np
from sklearn.metrics import precision_recall_fscore_support

FEATURES_PATH = "data/HDFS_v1/preprocessed/features.npz"
TEST_SET_SIZE = 100_000
FIT_SIZES = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
ITERATIONS = 40

def soft_threshold(X, tau):
    return np.sign(X) * np.maximum(np.abs(X) - tau, 0)

def inexact_alm_rpca(M, lam=None, tol=1e-7, max_iter=500):
    n, d = M.shape
    if lam is None: lam = 1.0 / np.sqrt(max(n, d))
    norm2 = np.linalg.norm(M, 2); normI = np.max(np.abs(M)) / lam
    Y = M / max(norm2, normI); mu = 1.25 / norm2; rho = 1.5
    L = np.zeros_like(M); S = np.zeros_like(M); normM = np.linalg.norm(M, 'fro')
    for _ in range(max_iter):
        U, sv, Vt = np.linalg.svd(M - S + Y/mu, full_matrices=False)
        sv_t = np.maximum(sv - 1/mu, 0)
        L = U @ np.diag(sv_t) @ Vt
        S = soft_threshold(M - L + Y/mu, lam/mu)
        Z = M - L - S; Y += mu * Z; mu = min(mu * rho, mu * 1e7)
        if np.linalg.norm(Z, 'fro') / normM < tol: break
    return L, S, int(np.sum(sv_t > 1e-6))

def l2_normalize(X):
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return X / norms

def main():
    data = np.load(FEATURES_PATH)
    X_raw = data["X_counts"].astype(np.float32)
    X_l2 = l2_normalize(X_raw)
    y = data["y"]
    
    rng = np.random.default_rng(42)
    N_total = len(y)
    
    print("Contaminated Setup (Figures 2-4) using L2-Normalized Raw Counts")
    print(f"Test size: {TEST_SET_SIZE:,} | Iterations: {ITERATIONS}")
    print("=" * 80)
    print(f"{'Fit Size':>8} | {'PCA P':>7} | {'PCA R':>7} | {'PCA F1':>7} || {'RPCA P':>7} | {'RPCA R':>7} | {'RPCA F1':>7}")
    print("-" * 80)
    
    for fit_size in FIT_SIZES:
        p_pca_list, r_pca_list, f1_pca_list = [], [], []
        p_rpca_list, r_rpca_list, f1_rpca_list = [], [], []
        
        for i in range(ITERATIONS):
            # Randomly sample train and test from entire dataset
            indices = rng.choice(N_total, size=fit_size + TEST_SET_SIZE, replace=False)
            fit_idx = indices[:fit_size]
            test_idx = indices[fit_size:]
            
            Xf = X_l2[fit_idx]
            Xt = X_l2[test_idx]
            y_test = y[test_idx]
            
            # 1. PCA (Mean-Centered, k=6)
            mean_pca = Xf.mean(axis=0)
            Xf_pca_c = Xf - mean_pca
            Xt_pca_c = Xt - mean_pca
            _, _, Vt = np.linalg.svd(Xf_pca_c, full_matrices=False)
            P_pca = Vt[:6].T
            et_pca = np.linalg.norm(Xt_pca_c - Xt_pca_c @ P_pca @ P_pca.T, axis=1)
            theta_pca = np.percentile(et_pca, 95)
            y_pred_pca = (et_pca > theta_pca).astype(int)
            p, r, f1, _ = precision_recall_fscore_support(y_test, y_pred_pca, average='binary', zero_division=0)
            p_pca_list.append(p); r_pca_list.append(r); f1_pca_list.append(f1)
            
            # 2. RPCA (Mean-Centered, k=9)
            # Center the data to avoid trivial rank collapse
            Xf_rpca_c = Xf - mean_pca
            L, _, _ = inexact_alm_rpca(Xf_rpca_c)
            _, _, Vt_rpca = np.linalg.svd(L, full_matrices=False)
            P_rpca = Vt_rpca[:9].T
            Xt_rpca_c = Xt - mean_pca
            et_rpca = np.linalg.norm(Xt_rpca_c - Xt_rpca_c @ P_rpca @ P_rpca.T, axis=1)
            theta_rpca = np.percentile(et_rpca, 95)
            y_pred_rpca = (et_rpca > theta_rpca).astype(int)
            p_r, r_r, f1_r, _ = precision_recall_fscore_support(y_test, y_pred_rpca, average='binary', zero_division=0)
            p_rpca_list.append(p_r); r_rpca_list.append(r_r); f1_rpca_list.append(f1_r)

        pca_p = np.mean(p_pca_list) * 100; pca_r = np.mean(r_pca_list) * 100; pca_f1 = np.mean(f1_pca_list) * 100
        rpca_p = np.mean(p_rpca_list) * 100; rpca_r = np.mean(r_rpca_list) * 100; rpca_f1 = np.mean(f1_rpca_list) * 100
        
        print(f"{fit_size:>8} | {pca_p:>7.2f} | {pca_r:>7.2f} | {pca_f1:>7.2f} || {rpca_p:>7.2f} | {rpca_r:>7.2f} | {rpca_f1:>7.2f}")

if __name__ == "__main__":
    main()
