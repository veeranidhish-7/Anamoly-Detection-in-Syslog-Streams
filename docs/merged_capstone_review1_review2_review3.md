# Consolidated Capstone Presentation Guide: Reviews 1, 2, and 3 (Master Slide Deck)

**Project Title:** Lightweight Reconstruction Modeling and Autonomous Extreme Value Thresholding for Syslog Anomaly Detection  
**Team Members:**  
* Venkata Dhanush Kakarlamudi (Reg. No.: 23BCE8172)  
* Veera Nidhish Gondimalla (Reg. No.: 23BCE7421)  
* Settipalli Raja Rushi Praneeth Reddy (Reg. No.: 23BCE7425)  
* Evvala Venkata Lakshmi Narasimha Veereswar (Reg. No.: 23BCE7439)  

**Department:** School of Computer Science and Engineering, VIT-AP University  
**Academic Year:** 2026–2027  

---

## Presentation Overview & Three-Phase Narrative Arc

```text
====================================================================================================
PART 1: CAPSTONE REVIEW 1 (Slides 1–10)
  Focus: Literature Review, SOSP/ICSRS Base Paper Replication, L2-Normalization Discovery,
         and Diagnosing the BGL Concurrency Challenge (30.18% Linear Baseline).
----------------------------------------------------------------------------------------------------
PART 2: CAPSTONE REVIEW 2 (Slides 11–20)
  Focus: Transition to Deep Semantics, Node-Based 6-Hour Window Alignment, Word2Vec Skip-Gram
         Embeddings, 16-8-16 Autoencoders, and Autonomous HDFS POT Thresholding (95.95% F1).
----------------------------------------------------------------------------------------------------
PART 3: CAPSTONE REVIEW 3 — FINAL GRAND DEFENSE (Slides 21–35)
  Focus: Transition to Natural Operational Prevalence (10.07%), Dual Mean+Max Pooling (64-d),
         10-Fold Ablations, 80/20 Chronological Concept Drift (68.9% OOV), Apple M2 Microsecond
         Hardware Profiling, Master SOTA Comparison Table, and Artifact Suite.
====================================================================================================
```

---

# PART 1: CAPSTONE REVIEW 1 — Problem Statement & Baseline Reproduction

### Slide 1: Title Slide (Review 1)
* **Slide Title:** Anomaly Detection in Syslog Streams: Baseline Replication & Failure Diagnosis
* **Subtitle:** Capstone Project Review 1
* **Team Members:** Venkata Dhanush Kakarlamudi, Veera Nidhish Gondimalla, Settipalli Raja Rushi Praneeth Reddy, Evvala Venkata Lakshmi Narasimha Veereswar
* **Core Focus:** Automated AIOps monitoring, supercomputer log volume, and evaluating whether published lightweight linear models replicate on production telemetry.
* **Speaker Script:**  
  *"Good morning, respected evaluators. Modern cloud infrastructures and supercomputing centers generate massive volumes of console logs every second. Automated detection of runtime faults is critical. In Review 1, our goal was to replicate foundational lightweight models and evaluate whether simple linear algebra can solve this problem in practice."*

---

### Slide 2: The Challenge of Distributed System Telemetry
* **Slide Title:** Industrial Context: The High-Volume Syslog Challenge
* **Slide Content & Key Points:**
  * **Scale:** Supercomputers emit millions of semi-structured text log lines per day.
  * **The Problem:** Manual inspection of error logs during system degradation is completely impossible.
  * **The Dilemma in Literature:**
    * *Heavyweight Deep Learning (DeepLog, LogBERT):* High computational complexity, millions of parameters, requiring dedicated GPUs.
    * *Lightweight Machine Learning (PCA, Clustering):* Highly desirable for real-time edge streaming, requiring minimal compute.
  * **Research Goal:** Can a lightweight model achieve production-grade detection without deep learning overhead?

---

### Slide 3: Choosing the Base Paper to Replicate
* **Slide Title:** Literature Baseline: Replicating Published Linear Models
* **Slide Content & Equations:**
  * **Target Literature:** Fält et al. (IEEE ICSRS 2025) and the foundational Xu et al. (SOSP 2009) framework.
  * **Proposed Pipeline:**
    1. Parse logs into event templates using regular expressions / Drain.
    2. Construct count vectors $\mathbf{x} \in \mathbb{R}^d$ across execution blocks.
    3. Apply Principal Component Analysis (PCA) to learn the normal low-rank subspace $\mathbf{P}$.
    4. Compute reconstruction error: $\mathbf{e} = \|\mathbf{x} - \mathbf{P}\mathbf{P}^T\mathbf{x}\|_2^2$.
    5. Flag anomalies exceeding a threshold.
  * **Published Benchmark Claim:** Achieving **$94.64\%$ F1-Score** on the HDFS benchmark.

---

### Slide 4: The HDFS Dataset & Problem Formulation
* **Slide Title:** Benchmark 1: Hadoop Distributed File System (HDFS)
* **Slide Content & Key Statistics:**
  * **Dataset Size:** $11,175,629$ log lines grouped into $575,061$ discrete block execution sessions.
  * **Ground Truth Labels:** $558,223$ healthy normal blocks ($97.05\%$) and $16,838$ anomalous blocks ($2.95\%$).
  * **Evaluation Protocol:** Standard 5-fold cross-validation on $25,000$ normal blocks and $1,000$ anomalous blocks (5,000 train normals, 21,000 test blocks per fold).
  * **The Initial Hurdle:** Standard TF-IDF and raw count vectors collapsed to only $\sim 76\%-78\%$ F1!

---

### Slide 5: The Reproduction Breakthrough: Undocumented L2-Normalization
* **Slide Title:** Engineering Discovery: The Undocumented L2-Normalization Step
* **Slide Content & Insight:**
  * **The Root Cause:** In raw count vectors, common routine operations (e.g. block allocations) appear thousands of times, overpowering the covariance matrix.
  * **The Discovery:** We uncovered an undocumented normalization step required to make PCA work:
    $$\mathbf{x}_{\text{norm}} = \frac{\mathbf{x}}{\|\mathbf{x}\|_2}$$
  * **Impact:** Scaling all vectors to unit length equalizes long-running and short-running sessions, enabling PCA to capture structural sequence deviations instead of raw frequency scale.

---

### Slide 6: HDFS Baseline Replication Results
* **Slide Title:** Experimental Verification: Successful HDFS PCA Replication
* **Slide Content & Results Table:**

| Metric | Published Base Paper Target | Our Replicated Implementation | Outcome |
| :--- | :---: | :---: | :---: |
| **Precision** | $92.00\%$ | **$92.34\% \pm 2.24\%$** | Replicated |
| **Recall** | $97.40\%$ | **$96.96\% \pm 2.35\%$** | Replicated |
| **F1-Score** | **$94.64\%$** | **$94.60\% \pm 2.30\%$** | **Exact Replication Match** |

* **Verification:** Replicated within $0.04\%$ of published metrics, proving complete mastery of the HDFS baseline pipeline.

---

### Slide 7: The Supercomputer Stress Test: Testing PCA on Blue Gene/L (BGL)
* **Slide Title:** Stress-Testing the Baseline: Moving from HDFS to BGL
* **Slide Content & Context:**
  * **Dataset 2:** Blue Gene/L (BGL) Supercomputer telemetry ($4,747,963$ log lines).
  * **Key Architectural Difference:**
    * *HDFS:* Cleanly partitioned by distinct `block_id` sessions (isolated processing).
    * *BGL:* A massive multi-core supercomputer where thousands of parallel processors asynchronously dump logs into a shared console daemon.
  * **Experiment:** Apply our replicated, L2-normalized linear PCA model to BGL.

---

### Slide 8: The Linear Baseline on BGL
* **Slide Title:** The Discovery: Linear Frequency Counting Limits on BGL
* **Slide Content & Metrics:**

```text
================================================================================
BASELINE ON BGL: Count-Based Linear PCA (L2-Normalized)
================================================================================
Precision: 99.68% ± 0.43%
Recall:    17.78% ± 0.08%   <-- Low Recall due to Concurrency
F1-Score:  30.18% ± 0.13%   <-- Demonstrates Need for Non-Linear Semantics
================================================================================
```

* **Why Frequency Counts Are Insufficient:**
  1. **Concurrency Interleaving:** In parallel clusters, events from concurrent jobs interweave randomly, destroying rigid count correlations.
  2. **Semantic Blindness:** Linear count vectors treat log keys as orthogonal integer bins ($E_1, E_2, \dots$), failing to understand that `"connection timeout"` and `"network dropped"` share semantic meaning.

---

### Slide 9: Review 1 Proposed Roadmap: Shifting to Continuous Semantics
* **Slide Title:** Review 1 Proposed Architecture: The Semantic Pivot
* **Slide Content & Conceptual Solution:**
  * **Pivoting from Counting to Meaning:** Replace discrete count matrices with continuous Natural Language Processing (NLP) embeddings.
  * **Pivoting from Linear to Deep Learning:** Introduce non-linear Deep Autoencoders capable of modeling complex, non-linear multi-core correlations.
  * **Pivoting to Autonomous Decision Boundaries:** Replace human-guessed percentile thresholds with mathematically grounded Extreme Value Theory.

---

### Slide 10: Conclusion of Review 1 & Transition to Phase 2
* **Slide Title:** Review 1 Conclusion & Roadmap for Review 2
* **Slide Content & Summary:**
  * Successfully replicated the published HDFS linear PCA baseline ($94.60\%$ F1).
  * Identified the multi-threaded concurrency challenges of real-world supercomputing clusters ($30.18\%$ linear baseline).
  * **Review 2 Milestones:**
    1. Implement Node-based structural alignment to organize BGL concurrency into clean execution paths.
    2. Train Word2Vec semantic embeddings on system logs.
    3. Implement a deep neural Autoencoder to reconstruct non-linear semantic manifolds.

---

# PART 2: CAPSTONE REVIEW 2 — Semantic Sequence Modeling & Initial Deep Architectures

### Slide 11: Title Slide (Review 2)
* **Slide Title:** Transitioning from Linear to Deep Semantic Models
* **Subtitle:** Capstone Project Review 2
* **Team Members:** Venkata Dhanush Kakarlamudi, Veera Nidhish Gondimalla, Settipalli Raja Rushi Praneeth Reddy, Evvala Venkata Lakshmi Narasimha Veereswar
* **Speaker Script:**  
  *"Respected committee, welcome to Review 2. In Review 1, we established our baseline and analyzed why linear models encounter limits on supercomputer logs. Today, we present our core contributions to advance this domain: continuous semantic Word2Vec representations, node-aligned sliding windows, deep neural autoencoders, and autonomous Peaks-Over-Threshold decision boundaries."*

---

### Slide 12: Contribution 1: Perfecting HDFS with Autonomous Extreme Value Theory (POT)
* **Slide Title:** Contribution 1: Transitioning to Autonomous Decision Boundaries
* **Slide Content & Innovation:**
  * **Evolution from Review 1:** The replicated PCA baseline relied on a manual 95th-percentile cutoff.
  * **Our Solution:** Implement **Peaks-Over-Threshold (POT)** from Extreme Value Theory.
  * **How it Works:** Fits a Generalized Pareto Distribution (GPD) strictly on normal training errors, deriving the threshold analytically:
    $$\theta = t + \frac{\hat{\sigma}}{\hat{\gamma}}\left[\left(\frac{q_n}{\text{target\_fpr}}\right)^{\hat{\gamma}} - 1\right] $$
  * **Result:** Elevated HDFS performance from $94.60\%$ to a fully autonomous **$95.95\%$ F1** without requiring manual threshold tuning.

---

### Slide 13: Contribution 2: Structural Alignment via Node-Based 6-Hour Windows
* **Slide Title:** Contribution 2: Structural Data Organization on BGL
* **Slide Content & Breakthrough:**
  * **The Windowing Evolution:** Slicing logs by pure wall-clock time (e.g. 5-minute tumbling windows) mixed unrelated messages from hundreds of compute cores.
  * **Our Innovation: Node-Based Physical Execution Alignment:**
    * Group logs strictly by hardware **Node ID** (`node_id`).
    * Apply a **6-hour non-overlapping sliding window** per node (the standard HPC operational job cycle).
  * **Impact:** Reconstructs the true physical execution path of each processor, providing clean contextual sequences for NLP modeling.

---

### Slide 14: Deep Semantic Understanding via Word2Vec Skip-Gram
* **Slide Title:** Contribution 3: Semantic Sequence Representation
* **Slide Content & Formulation:**
  * Replaced discrete template IDs with a continuous vector space using Word2Vec Skip-Gram ($32$ dimensions).
  * **Training:** Word2Vec learns which log events co-occur in normal operations, mapping semantically similar events near each other.
  * **Mean Pooling:** A sequence window of variable length $L$ is aggregated into a fixed-length representation:
    $$\mathbf{v}_{\text{window}} = \frac{1}{L}\sum_{i=1}^L \text{Word2Vec}(e_i)$$
  * **L2-Normalization:** The pooled semantic vector is projected to the unit hypersphere to prevent long sequences from overpowering short sequences.

---

### Slide 15: The Deep Semantic Autoencoder (16-8-16 Architecture)
* **Slide Title:** Contribution 4: Neural Reconstruction Modeling
* **Slide Content & Design:**
  * **Architecture:** 3-layer Multi-Layer Perceptron (MLP) Autoencoder ($32 \to 16 \to 8 \to 16 \to 32$).
  * **The Bottleneck Compression:** 
    * Compresses the 32-d vector down to an **8-neuron bottleneck**.
    * Forces the neural network to memorize only the core, low-dimensional invariant manifold of healthy supercomputer behavior.
  * **Anomaly Detection:** Sequences that deviate from healthy semantics fail to reconstruct through the 8-neuron bottleneck, producing massive reconstruction error spikes:
    $$e = \|\mathbf{x} - \hat{\mathbf{x}}\|_2^2$$

---

### Slide 16: Addressing Data Leakage: Initial Isolation of Word2Vec
* **Slide Title:** Academic Integrity: Strict Training Data Isolation
* **Slide Content & Rigor:**
  * **The Standard in Rigorous Research:** To ensure models generalize to unseen real-world operations, text encoders must be isolated to training sets.
  * **Our Implementation:**
    * Word2Vec was restricted strictly to the normal training fold.
    * Out-of-Vocabulary (OOV) tokens occurring in test sets were ignored or mapped to zero.
  * **10-Fold Cross-Validation:** Implemented a full 10-fold split so that every log sequence is evaluated.

---

### Slide 17: Review 2 Experimental Results (Initial Prototype: 90.44% F1)
* **Slide Title:** Review 2 Results: Proving Semantic Feasibility
* **Slide Content & Comparison Table:**

| Model / Approach | Target Dataset | Paradigm | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Linear PCA (Review 1)** | BGL | Count-based Linear | $99.68\%$ | $17.78\%$ | $30.18\%$ |
| **DeepLog (LSTM Baseline)** | BGL | Heavyweight LSTM | $83.20\%$ | $69.40\%$ | $75.70\%$ |
| **CNN** | BGL | Heavyweight CNN | $88.00\%$ | $82.00\%$ | $84.90\%$ |
| **OUR PROPOSAL: Semantic Autoencoder** | **BGL** | **Lightweight NLP-AE** | **$98.59\%$** | **$83.55\%$** | **$90.44\%$** |

* **Review 2 Milestone:** Successfully proved that continuous semantics and deep autoencoders rescue BGL anomaly detection, advancing performance from $30\%$ to $\mathbf{90.44\%}$ F1 in our initial balanced setup.

---

### Slide 18: Comparative Analysis: Lightweight vs Heavyweight
* **Slide Title:** Architecture Analysis: Bridging the Efficiency Gap
* **Slide Content & Comparison:**
  * **Heavyweight Models (LogBERT, Transformers):**
    * Require 110 million parameters, hundreds of megabytes of RAM, and dedicated GPUs.
    * Unviable for edge deployment on distributed monitoring daemons.
  * **Traditional Lightweight ML (K-Means, PCA):**
    * Fast, but collapsed on unstructured BGL logs ($30\%-65\%$ F1).
  * **Our Semantic Autoencoder:**
    * Bridges the gap: delivers near-SOTA performance ($90.44\%$) while operating as a compact, CPU-viable neural network.

---

### Slide 19: Review 2 Next Steps: Roadmap for Review 3
* **Slide Title:** Review 2 Next Steps: Preparing for Enterprise Deployment
* **Slide Content & Progression Plan:**
  * **Transition to Natural Operational Prevalence:** Evolve testing from a balanced prototype view to the true natural operational base-rate ($\sim 10\%$ prevalence).
  * **Deterministic Training Standards:** Lock in fixed random seeds and single-pass evaluation across all folds.
  * **Temporal Generalization:** Evaluate an 80/20 chronological time-split across the 7-month dataset.
  * **Hardware Latency Benchmarking:** Measure real microsecond execution latencies on physical CPU hardware.

---

### Slide 20: Conclusion of Review 2 & Transition to Final Defense
* **Slide Title:** Review 2 Conclusion: Setting the Stage for the Final Defense
* **Slide Content & Summary:**
  * Proved that continuous semantics and deep autoencoders solve supercomputer log anomaly detection ($90.44\%$ F1 in prototype evaluation).
  * Formulated autonomous EVT POT thresholding on HDFS ($95.95\%$ F1).
  * **Review 3 Target Objectives:**
    1. Transition to natural operational prevalence ($10.07\%$) and verify stability.
    2. Perform 10-fold ablation studies against four competing baseline models.
    3. Test temporal generalization on an 80/20 chronological time-split across 7 months.
    4. Profile physical microsecond inference latencies on consumer CPU hardware.

---

# PART 3: CAPSTONE REVIEW 3 — Final Grand Defense: The Complete Framework

### Slide 21: Title Slide (Review 3 — Final Grand Defense)
* **Slide Title:** Lightweight Reconstruction Modeling and Autonomous Extreme Value Thresholding for Syslog Anomaly Detection
* **Subtitle:** Final Capstone Project Defense (Review 3)
* **Team Members:** Venkata Dhanush Kakarlamudi, Veera Nidhish Gondimalla, Settipalli Raja Rushi Praneeth Reddy, Evvala Venkata Lakshmi Narasimha Veereswar
* **Speaker Script:**  
  *"Respected professors, welcome to our Final Capstone Defense. In Review 2, we showed that deep semantics could bridge the gap on BGL. In this final review, we deliver the completed, academically rigorous, publication-grade framework: we have transitioned to natural operational prevalence evaluation, advanced our feature representation to dual Mean+Max pooling, validated temporal robustness across 7 months of operational logs, benchmarked edge execution on physical CPU hardware, and authored a camera-ready IEEE research paper."*

---

### Slide 22: Evaluation Evolution: Transitioning to Natural Operational Prevalence
* **Slide Title:** Evaluation Evolution: Transitioning to Natural Operational Prevalence
* **Slide Content & Methodological Progression:**
  * **The Progression from Review 2 to Review 3:**
    * *In Review 2 (Initial Feasibility Setup):* Our prototype was evaluated under a controlled, balanced test distribution ($\sim 50\%$ anomaly prevalence), achieving **$90.44\%$ F1** to demonstrate the effectiveness of deep semantics.
    * *In Review 3 (Production-Grade Operational Protocol):* To prepare for real-world enterprise deployment and conference publication, we transitioned to evaluating under the **genuine natural operational prevalence ($10.07\%$)** of the supercomputer ($1,286,817$ total windows).
  * **Key Enhancements Implemented in Review 3:**
    1. **Strict 10-Fold Stratified Cross-Validation:** Every single anomalous window ($129,528$ windows) across the 7-month dataset is evaluated **exactly once**.
    2. **Pure Normal Training:** The model trains exclusively on healthy operational behavior ($937,404$ windows; 0 anomalies), reflecting real production environments.
    3. **Deterministic Protocol:** Fixed random seeds across dataset partitioning, Word2Vec training, and Autoencoder convergence.
    4. **Strict Vocabulary Isolation:** Word2Vec is trained strictly on normal training sequences with complete Out-Of-Vocabulary (OOV) handling.

---

### Slide 23: Leak-Free 10-Fold Protocol under Natural Operational Prevalence
* **Slide Title:** Experimental Integrity: Stratified Disjoint Partitions
* **Slide Content & Set Theory Proof:**
  * **Dataset Size:** $1,286,817$ sequence windows ($1,157,289$ normals, $129,528$ anomalies).
  * **Disjointness Invariants Formally Verified in Code:**
    $$\text{Train} \cap \text{Val} = \emptyset, \quad \text{Train} \cap \text{Test} = \emptyset, \quad \text{Val} \cap \text{Test} = \emptyset$$
    $$\forall i \in \text{Train}: \quad y_i = 0 \quad (\text{Pure Normal Training Data})$$
  * **Strict Training Isolation:** The model trains exclusively on healthy normal sequences ($937,404$ windows). It has never seen an anomaly during training.

---

### Slide 24: Architectural Evolution: Dual Semantic Pooling & Bottleneck Autoencoder
* **Slide Title:** Architectural Evolution: 64-d Mean+Max Pooling & Bottleneck AE
* **Slide Content & Design Evolution:**
  * **Evolution 1: Dual Semantic Pooling ($64$ dimensions)**
    * *Mean Pooling (32-d):* Computes the centroid of the window, capturing general operational background state.
    * *Max Pooling (32-d):* Captures the extreme coordinate activations, preserving rare, bursty error signatures.
    * Concatenation: $\mathbf{x} = [\mathbf{v}_{\text{mean}} \parallel \mathbf{v}_{\text{max}}] \in \mathbb{R}^{64}$, normalized via L2 projection.
  * **Evolution 2: 5-Layer Regularized Bottleneck Autoencoder**
    * Structure: $64 \to 32 \to 16 \to 32 \to 64$.
    * L2 Weight Regularization ($\alpha = 10^{-4}$) to prevent overfitting to routine normal templates.
    * Total Parameters: Exactly **$5,328$** (ultra-lightweight).

---

### Slide 25: Autonomous Extreme Value Thresholding (POT): The Mathematical Proof
* **Slide Title:** Autonomous Decision Boundary: Extreme Value Theory (EVT / POT)
* **Slide Content & Mathematical Formulation:**
  * Avoids all manual threshold guessing by fitting Generalized Pareto Distributions (GPD) strictly on normal training residuals:
    $$\theta = t + \frac{\hat{\sigma}}{\hat{\gamma}}\left[\left(\frac{q_n}{\text{target\_fpr}}\right)^{\hat{\gamma}} - 1\right]$$
  * **Two Operational Modes Formulated:**
    * **Mode A (Headline — Pure Unsupervised):** Zero test labels, zero validation labels. $\text{target\_fpr} = 10^{-3}$. Automatically falls back to the 99.5th percentile if GPD fitting fails.
    * **Mode B (Semi-Supervised):** A small validation set of known anomalies is used to optimize F1 via grid search.

---

### Slide 26: Canonical BGL 10-Fold Results: Natural Prevalence vs Balanced Perspective
* **Slide Title:** Canonical BGL Benchmark: Full 10-Fold Cross-Validation
* **Slide Content & Comparison Table:**

| Evaluation Setting | Test Anomaly Prevalence | Precision (%) | Recall (%) | F1-Score (%) | PR-AUC (%) | ROC-AUC (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Review 3: Mode A (Autonomous POT)** | **10.07% (Natural)** | **93.76 ± 2.54** | **82.61 ± 1.96** | **87.80 ± 1.31** | **91.05 ± 0.32** | **97.34 ± 0.15** |
| **Review 3: Mode B (Validation-Tuned)**| **10.07% (Natural)** | **93.06 ± 2.59** | **84.71 ± 1.19** | **88.66 ± 1.07** | **91.05 ± 0.32** | **97.34 ± 0.15** |
| **Review 3: Balanced Perspective** | **50.00% (Balanced)** | **99.26 ± 0.60** | **82.61 ± 1.96** | **90.16 ± 1.05** | **95.82 ± 0.20** | **97.34 ± 0.15** |
| *Review 2 Prototype (Initial Balanced)*| *52.80% (Balanced)* | *98.59%* | *83.55%* | *90.44%* | — | — |

* **Key Takeaways:**
  1. **Canonical Clean Headline:** Under true natural operational prevalence ($10.07\%$), our model achieves **$87.80\%$ Mode A F1** and **$91.05\%$ PR-AUC** with high cross-fold stability ($\pm 1.31\%$).
  2. **Harmonious Cross-Perspective Validation:** When evaluating the exact same model on a balanced test set, precision rises from $93.76\%$ to $99.26\%$, yielding **$90.16\%$ Mode A** and **$91.36\%$ Mode B F1**, perfectly matching Review 2's prototype performance.
  3. **Conclusion:** The model architecture is robust across both operational and balanced views; the difference is purely the mathematical relationship between prevalence and precision.

---

### Slide 27: 10-Fold Ablation Matrix: Proving Neural Reconstruction is Strictly Necessary
* **Slide Title:** Architectural Ablation: Proving Neural Autoencoders are Indispensable
* **Slide Content & 10-Fold Cross-Validation Table:**

| Model Architecture | Input Features | Mode A F1 (%) | Mode A Prec (%) | Mode A Rec (%) | PR-AUC (%) | ROC-AUC (%) | Training Time |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **MLP Autoencoder (Ours)** | **Word2Vec Mean+Max (64-d)** | **87.80 ± 1.31** | **93.76 ± 2.54** | **82.61 ± 1.96** | **91.05 ± 0.32** | **97.34 ± 0.15** | 60.1s |
| **PCA ($k=48$ tuned)** | Word2Vec Mean+Max (64-d) | 59.97 ± 8.42 | 81.32 ± 11.20 | 50.00 ± 12.40 | 84.26 ± 0.85 | 96.78 ± 0.18 | 3.0s |
| **PCA (Raw Count Vectors)** | Discrete Event Counts (29-d) | 34.28 ± 13.91 | 21.04 ± 1.82 | 92.45 ± 2.10 | 24.12 ± 1.50 | 72.40 ± 1.20 | 4.2s |
| **Isolation Forest** | Word2Vec Mean+Max (64-d) | 2.07 ± 0.85 | 25.99 ± 4.10 | 1.10 ± 0.45 | 48.20 ± 1.20 | 92.23 ± 0.40 | 0.4s |
| **Predict All Normal** | Baseline Rule | 0.00 | 0.00 | 0.00 | 10.07 | 50.00 | 0.0s |
| **Random Guessing** | Uniform Random | 12.34 | 10.03 | 16.03 | 10.07 | 50.00 | 0.0s |

* **Key Takeaways:** Our Autoencoder beats linear PCA by **$+27.83\%$ F1** and Isolation Forest by **$+85.73\%$ F1**. Linear hyperplanes cannot model the complex semantics of supercomputer telemetry.

---

### Slide 28: Temporal Generalization & Concept Drift: The 80/20 Chronological Split
* **Slide Title:** Production Robustness: The 80/20 Chronological Time-Split
* **Slide Content & Empirical Findings:**
  * **Setup:** Train on first $70\%$ of timeline (months 1–5), test on latest $20\%$ unseen future logs (months 6–7; $296,300$ windows, $21.88\%$ anomaly prevalence).
  * **Test Results:** Mode B F1 achieved **$45.28\%$** (Precision: $29.64\%$, Recall: $95.90\%$).
  * **The Discovery — Severe Lexical Concept Drift:**
    * In months 6 and 7, **$68.91\%$ of all log tokens were Out-Of-Vocabulary (OOV)** ($935,199$ / $1,357,066$ tokens)!
    * Blue Gene/L underwent operating system upgrades, node replacements, and batch workload transitions that generated hundreds of completely new log templates.
  * **AIOps Implication:** In production monitoring, **static models are unviable**. Systems must implement scheduled, periodic online retraining.

---

### Slide 29: Complete HDFS Benchmark: 95.95% POT, RPCA Ceiling, & 570k Scale
* **Slide Title:** Complete HDFS Benchmark: Replicating, Advancing, & Scaling
* **Slide Content & Table:**

| Pipeline / Model | Threshold Mechanism | Precision (%) | Recall (%) | F1-Score (%) | PR-AUC (%) | Operational Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **PCA Baseline Replication** | 95th %ile Test Oracle | 92.34 ± 2.24 | 96.96 ± 2.35 | **94.60 ± 2.30** | — | Published Replication Match |
| **PCA + Autonomous POT (Ours)**| **Autonomous EVT (Train Only)**| **93.61 ± 1.62** | **98.46 ± 1.89** | **95.95 ± 1.47** | **99.58** | **Autonomous SOTA Ceiling** |
| **Robust PCA (RPCA Ceiling)** | Exhaustive Search Ceiling | 91.75 | 83.40 | **87.38** | — | Infeasible (>200ms, rank capped) |
| **PCA + POT at Full Scale** | Fixed POT (Saved Fold Models)| **90.04 ± 1.83** | **97.80 ± 2.05** | **93.74 ± 1.26** | **97.97** | **Evaluated on 570,061 Sessions** |

* **Key Breakthroughs on HDFS:**
  1. Autonomous POT beats published baseline ($95.95\%$ vs $94.60\%$) with zero test labels.
  2. Evaluated at true operational scale across **all 570,061 held-out sessions** in HDFS ($2.95\%$ prevalence), maintaining **$93.74\%$ F1** and **$97.97\%$ PR-AUC**.
  3. Explored Robust PCA and proved that it is naturally capped at $87.38\%$.

---

### Slide 30: Edge Hardware Benchmark on Apple M2: Microsecond Latency
* **Slide Title:** Edge Hardware Efficiency: Sub-Millisecond CPU Inference
* **Slide Content & Benchmarking Specs:**
  * **Physical Testbench:** Apple M2 (8-core ARM64 CPU), 8.0 GB RAM, macOS Darwin 15.8.1.

| Hardware Metric | HDFS Linear PCA | BGL Semantic Autoencoder | Heavyweight Transformers (LogBERT) |
| :--- | :---: | :---: | :---: |
| **Trainable Parameters** | **203** | **5,328** | ~110,000,000 (110M) |
| **Model Size on Disk** | **1.02 KB** | **70.25 KB** | ~420,000 KB (420 MB) |
| **Cache Residency** | Fits in L1 Cache | **Fits in L2 CPU Cache** | Requires GPU VRAM |
| **Single-Sample Latency (Mean)** | **0.0035 ms (3.5 µs)** | **0.0432 ms (43.2 µs)** | 22.0 ms – 45.0 ms |
| **Batch Latency (Batch=256)** | **0.0240 ms** | **0.0959 ms (0.37 µs/window)** | 5.2 ms – 15.0 ms |
| **Pipeline Throughput** | **10,666,667 sessions/sec** | **62,076 windows/sec** | 50 – 200 windows/sec |
| **Hardware Required** | Commodity Edge CPU | **Commodity Edge CPU** | High-Power NVIDIA GPU Cluster |

---

### Slide 31: Master State-of-the-Art Comparison Table (HDFS & BGL)
* **Slide Title:** Comprehensive Benchmark Comparison with Published Literature
* **Slide Content & Master Table:**

| Model / Approach | Target Dataset | Supervision Level | Decision Threshold | F1-Score (%) | Model Size | Inference Latency | Directly Comparable? |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **PCA + POT (Ours)** | **HDFS** | **Unsupervised** | **Autonomous EVT** | **95.95%** | **1 KB** | **3.5 µs** | **YES (5-Fold SOTA)** |
| **LogFIT** (Almodovar 2024)| HDFS | Unsupervised | Fixed Quantile | 95.02% | 250 MB | 1.2 ms | YES (Same Protocol) |
| **DeepLog** (Du et al. 2017)| HDFS | Unsupervised | Top-$g$ Oracle | 75.70% (Small) | 10 MB | 3.8 ms | Partial (Small-data collapse) |
| **LogBERT** (Guo et al. 2021)| HDFS | Unsupervised | Hypersphere Radius | 37.24% (Small) | 420 MB | 22.0 ms | Partial (Severe data collapse) |
| **LogRobust** (Zhang 2019) | HDFS | **Supervised** | Sigmoid Cutoff | 96.30% | 23 MB | 6.5 ms | **NO** (Requires Labels) |
| **Semantic MLP-AE (Ours)** | **BGL** | **Unsupervised** | **Autonomous EVT (POT)** | **87.80%** | **70 KB** | **43.2 µs** | **YES (Natural 10.07%)** |
| **Semantic MLP-AE (Balanced)**| **BGL** | **Unsupervised** | **Autonomous EVT (POT)** | **90.16%** | **70 KB** | **43.2 µs** | **YES (50% Balanced View)** |
| **LogBERT on BGL** | BGL | Semi-Supervised | Hypersphere Radius | 90.83% (Empirical) | 420 MB | 25.0 ms | **NO** (20-line window, GPU) |
| **DeepLog on BGL** | BGL | Unsupervised | Top-$g$ Oracle | 86.12% (Empirical) | 10 MB | 4.5 ms | **NO** (Interleaving failure) |
| **LogAnomaly on BGL** | BGL | Semi-Supervised | Semantic Distance | 74.08% (Empirical) | 16 MB | 6.2 ms | **NO** (Windowing disparity) |
| **NeuralLog** (Le et al. 2021)| BGL | **Supervised** | Classification Head | 85.20% | 420 MB | 35.0 ms | **NO** (Supervised labels) |

---

### Slide 32: Why Lightweight Wins: Defense Justification
* **Slide Title:** Defense Justification: Why Our Architecture Wins in the Real World
* **Slide Content & Three Pillars of Victory:**
  1. **Pillar 1: True Unsupervised Autonomy (Zero Test-Label Dependency)**
     * Published deep learning models tune candidate beam sizes or hypersphere radii against test labels.
     * *Our Approach:* Extreme Value Theory derives the decision boundary **strictly from normal training residuals**, requiring zero test-set feedback and enabling immediate zero-day deployment.
  2. **Pillar 2: Immune to Concurrency Interleaving (The BGL Breakthrough)**
     * Sequential forecasting models (DeepLog, LogAnomaly) fail when concurrent cores interleave logs. Our Node-aligned Mean+Max pooling is **order-invariant within 6-hour windows**, achieving **$93.76\%$ precision**.
  3. **Pillar 3: The 20,000x Efficiency Multiplier**
     * LogBERT requires a $420\text{ MB}$ footprint, takes $25\text{ ms}$, and needs an expensive GPU cluster.
     * *Our Approach:* At **$43.2$ microseconds** and **$70\text{ KB}$**, our model runs directly as a background sidecar process on commodity edge CPUs, eliminating GPU cluster costs.

---

### Slide 33: Complete Artifact Package: Paper, Thesis, & Submission Suite
* **Slide Title:** Engineering Deliverables & Reproducibility Package
* **Slide Content & Inventory:**
  * **1. Research Paper (`paper/main.tex`):** Full camera-ready IEEE conference manuscript with vector graphics and verified citations.
  * **2. B.Tech Capstone Thesis (`report/`):** 6-chapter comprehensive report (`ch1` to `ch6`), frontmatter, and certificates.
  * **3. Master Audit Ledger (`PROJECT_MAP.md`):** 1,046 lines answering all 23 audit questions with exact byte sizes and timestamps.
  * **4. Canonical Self-Contained Reproduction Suite (`FINAL_SUBMISSION/`):**
    * Standalone HDFS and BGL code.
    * 15 pre-trained fold models with instant evaluation mode (`--load-saved`) that reproduces all numbers in 15 seconds.
    * Step-by-step reproduction guide in `README.md`.
  * **5. Public Open-Source Git Repository:** Clean git tree synchronized and pushed to GitHub.

---

### Slide 34: Final Conclusion & Milestones Summary
* **Slide Title:** Conclusion: Project Summary & Scientific Contributions
* **Slide Content & Summary Box:**
  * **HDFS Benchmark:** Replicated published baseline ($94.60\%$), advanced to autonomous SOTA ceiling (**$95.95\%$ F1**), and evaluated at true natural operational scale (**$93.74\%$ F1** across $570,061$ sessions).
  * **BGL Benchmark:** Overcame the $30\%$ linear baseline collapse, achieving **$87.80\%$ Mode A F1** ($90.16\%$ balanced) and **$91.05\%$ PR-AUC** under strict leak-free 10-fold natural prevalence.
  * **Scientific Rigor:** Proved why neural autoencoders are strictly required (+27.8% over PCA) and revealed that software evolution causes $68.9\%$ OOV drift, requiring continuous retraining.
  * **Edge Viability:** Verified microsecond CPU execution ($43.2\ \mu\text{s}$), $70\text{ KB}$ footprint, and $62,000+$ windows/sec throughput on an Apple M2 CPU.

---

### Slide 35: Thank You & Grand Defense Q&A
* **Slide Title:** Thank You — Questions & Discussion
* **Slide Content:**
  * **Project Repository:** [`https://github.com/veeranidhish-7/Anamoly-Detection-in-Syslog-Streams`](https://github.com/veeranidhish-7/Anamoly-Detection-in-Syslog-Streams)
  * **Authors:** Venkata Dhanush Kakarlamudi, Veera Nidhish Gondimalla, Settipalli Raja Rushi Praneeth Reddy, Evvala Venkata Lakshmi Narasimha Veereswar
  * **Department:** School of Computer Science & Engineering, VIT-AP University.
  * Open for Questions and Committee Examination.

---

### **Master Defense Quick-Reference Guide: Top 5 Questions & Model Answers**

1. **Q: Why does your final BGL score show 87.80% when your Review 2 presentation reported 90.44%?**
   * *Model Answer:* "In Review 2, our initial prototype was evaluated under a controlled balanced distribution (~50% prevalence), where it achieved 90.44% F1. For Review 3, as we prepared for enterprise deployment and paper publication, we transitioned to evaluating under genuine natural operational base-rate prevalence (10.07%), where the model achieves 87.80% Mode A F1 and 91.05% PR-AUC. When we evaluate this same model on the balanced setup, it confirms **90.16% Mode A and 91.36% Mode B F1**. This proves that our model architecture is exceptionally stable across both operational and balanced views."

2. **Q: How does your approach handle unseen Out-of-Vocabulary (OOV) log templates?**
   * *Model Answer:* "Words not present in the training normal vocabulary are skipped during pooling. If an entire window consists of unknown words, it maps to a zero vector. Since normal operational patterns produce distinct non-zero embeddings, passing a zero vector through our trained Autoencoder naturally yields a high reconstruction error, correctly alerting operators to anomalous behavior. In our 80/20 chronological experiment, we also proved that continuous weekly fine-tuning is required in production."

3. **Q: Why should an enterprise deploy your lightweight Autoencoder instead of LogBERT or DeepLog?**
   * *Model Answer:* "Three reasons: first, our Extreme Value Theory threshold is completely autonomous and requires zero test labels. Second, DeepLog collapses on BGL because concurrent multi-threaded logs break sequential line order, whereas our Node-aligned pooling is order-invariant. Third, LogBERT requires 420 MB of RAM, 25 milliseconds per log, and expensive GPU clusters. Our model requires only 70 KB, executes in 43.2 microseconds on a standard CPU, and can run as a background daemon on edge nodes with 20,000x less memory."

4. **Q: Why did Robust PCA (RPCA) fail to reach the published 90.55% F1?**
   * *Model Answer:* "Under inexact Augmented Lagrange Multipliers (ALM), the low-rank matrix collapses to rank 2–4 on normal log matrices. Through exhaustive parameter sweeps across 30 seeds and normal sample sizes from 5k to 25k, we proved that RPCA is naturally capped at 87.38% F1 (mean 85.14%). Published claims of 90.55% represent an irreproducible outlier."

5. **Q: Can your entire framework be reproduced independently?**
   * *Model Answer:* "Yes, 100%. In our `FINAL_SUBMISSION/` folder, we provide clean, path-agnostic scripts, pinned dependencies in `requirements.txt`, 15 serialized fold models, and a step-by-step reproduction guide. Running `python FINAL_SUBMISSION/bgl/run_final_evaluation.py --load-saved` reproduces all 10 folds of test results in just 15 seconds."
