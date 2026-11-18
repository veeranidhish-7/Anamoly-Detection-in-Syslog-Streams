# Capstone Review 3: Final Grand Defense Presentation Guide (Review 3 Alone)

**Project Title:** Lightweight Reconstruction Modeling and Autonomous Extreme Value Thresholding for Syslog Anomaly Detection  
**Team Members:**  
* Venkata Dhanush Kakarlamudi (Reg. No.: 23BCE8172)  
* Veera Nidhish Gondimalla (Reg. No.: 23BCE7421)  
* Settipalli Raja Rushi Praneeth Reddy (Reg. No.: 23BCE7425)  
* Evvala Venkata Lakshmi Narasimha Veereswar (Reg. No.: 23BCE7439)  

**Department:** School of Computer Science and Engineering, VIT-AP University  
**Academic Year:** 2026–2027  
**Presentation Context:** Standalone Capstone Review 3 (Final Grand Defense). This guide contains the exact continuation from where Review 2 ended, completing the research arc with rigorous leak-free evaluation, architectural ablations, temporal generalization, edge hardware benchmarking, and state-of-the-art comparative defense.

---

## Slide 1: Title Slide (Review 3 — Final Capstone Defense)

* **Slide Title:** Lightweight Reconstruction Modeling and Autonomous Extreme Value Thresholding for Syslog Anomaly Detection
* **Subtitle:** Final Capstone Project Defense (Review 3)
* **Team Members:**
  * Venkata Dhanush Kakarlamudi (23BCE8172)
  * Veera Nidhish Gondimalla (23BCE7421)
  * Settipalli Raja Rushi Praneeth Reddy (23BCE7425)
  * Evvala Venkata Lakshmi Narasimha Veereswar (23BCE7439)
* **Project Guide & Department:** School of Computer Science and Engineering, VIT-AP University
* **Slide Content / Visual Highlights:**
  * Official academic header with VIT-AP University seal.
  * Three foundational pillars of the completed project:
    1. *Lightweight Reconstruction:* Linear PCA on HDFS (203 params), 5-layer MLP-AE on BGL (5,328 params).
    2. *Autonomous Extreme Value Thresholding:* Peaks-Over-Threshold (EVT / POT) — Zero Test Leakage.
    3. *Real-World Edge Viability:* Sub-millisecond CPU latency (43.2 µs), 62,000+ windows/sec throughput.

> **Speaker Script:**  
> *"Good morning, respected evaluators and professors. Welcome to our Final Capstone Defense (Review 3). In Review 1, we replicated linear baselines on HDFS and discovered why they collapse on complex supercomputers. In Review 2, we introduced continuous semantics and initial deep autoencoders. Today, in our final defense, we present the completed, fully validated, leak-free framework: we have eliminated all test-set contamination, solved autonomous thresholding using Extreme Value Theory, validated temporal robustness on real operational logs, benchmarked edge execution on physical hardware, and proved how our lightweight architecture competes with—and in real-world deployment surpasses—heavyweight 100-million parameter deep learning models."*

---

## Slide 2: The Project Journey Recap (Review 1 $\rightarrow$ Review 2 $\rightarrow$ Review 3)

* **Slide Title:** Project Trajectory: From Linear Reproduction to Edge-Viable Deep Framework
* **Slide Content / Visuals (3-Column Flowchart):**
  * **Phase 1 (Review 1 — Baseline Replication & Failure Diagnosis):**
    * Replicated SOSP 2009 / ICSRS 2025 PCA baseline on HDFS ($94.60\%$ F1) via undocumented L2-normalization.
    * Applied linear PCA to BGL supercomputer: **Catastrophic collapse to $30.18\%$ F1**.
    * *Diagnosis:* Frequency counts ignore interleaved multi-core process execution.
  * **Phase 2 (Review 2 — Semantic Representation & Initial Deep Modeling):**
    * Solved "Semantic Soup" via Node-based 6-hour sequence alignment.
    * Replaced word counts with Word2Vec continuous embeddings + MLP Autoencoder ($16 \to 8 \to 16$).
    * Formulated Extreme Value Theory (POT) on HDFS ($95.95\%$ F1).
    * Preliminary BGL score reported: $\sim 90.44\%$ F1.
  * **Phase 3 (Review 3 — Rigorous Final Validation & Contributions):**
    * **Audit & Leak Elimination:** Deconstructed the $90.44\%$ figure as an artifact of $50\%$ test prevalence; established genuine **$87.80\%$ Mode A F1** under natural operational prevalence ($10.07\%$).
    * **Architectural Evolution:** 64-d Mean+Max pooling + bottleneck MLP Autoencoder.
    * **Temporal Generalization:** Evaluated 80/20 chronological time-split across 7 months.
    * **Hardware Edge Profiling:** Verified sub-millisecond CPU latency ($43.2\ \mu\text{s}$) on Apple M2.
    * **Deliverables:** Camera-ready IEEE paper, 6-chapter B.Tech thesis, and canonical artifact package.

> **Speaker Script:**  
> *"To orient everyone on our progression: Review 1 proved that traditional count-based linear models work on structured logs like HDFS but fail completely on complex supercomputers like BGL, crashing to 30% F1. In Review 2, we showed that node alignment and continuous semantics rescue this performance, pushing initial scores to ~90%. In this final phase, we conducted an exhaustive scientific audit: we eliminated all test contamination, benchmarked real hardware latency, performed rigorous ablations against four baseline architectures, and tested temporal concept drift on 7 months of continuous telemetry."*

---

## Slide 3: The Critical Review 2 Audit: Prevalence Inflation & Test Leakage

* **Slide Title:** Scientific Rigor: Eliminating Literature Flaws & Test Contamination
* **Slide Objective:** Honestly explain why the Review 2 score was $\sim 90.44\%$ and how Review 3 established the gold-standard leak-free ground truth.
* **Slide Content / Visuals:**
  * **Flaw 1 in Prior Literature & Early Drafts: Artificial Test Prevalence**
    * Older code collected all 129,528 anomalies from the whole dataset and placed them into every test fold alongside $\sim 115,729$ normals, inflating anomaly prevalence to **$52.8\%$** (a 1:1 balanced distribution).
    * *Real World:* Anomalies account for only **$10.07\%$** of operational windows ($1,286,817$ total windows).
  * **Flaw 2: Test-Label Feedback in Automated Loops**
    * Older scripts contained retry logic (`while f1 < 0.80: seed_offset += 1`), implicitly allowing test set performance to influence model selection.
  * **Flaw 3: Lookahead Vocabulary Leakage**
    * Word2Vec was previously trained on the entire dataset prior to splitting, leaking test tokens into the embedding dictionary.
  * **The Review 3 Golden Protocol:**
    1. **Strict 10-Fold Stratification:** Each fold tests on natural $10.07\%$ prevalence. Every anomaly is tested **exactly once**.
    2. **Zero Test Access:** Word2Vec and Autoencoders are trained **exclusively on training normals**.
    3. **Zero Test-Label Feedback:** Validated by automated static analysis (`grep y_test` returns 0 matches in development scripts).

> **Speaker Script:**  
> *"The most important hallmark of good engineering is scientific honesty. Following Review 2, we conducted a forensic code audit. We discovered that, like many published papers in this domain, our earlier script had an inflated test set prevalence of ~53% anomalies and allowed automated seed-retries. Under real operational conditions, anomalies represent only 10% of supercomputer logs. In Review 3, we completely rebuilt the pipeline from the ground up: every single test fold now reflects the exact 10.07% natural operational prevalence, the training set contains zero anomalies, and no test label is ever observed during model selection."*

---

## Slide 4: Methodology: The Leak-Free Architecture Pipeline

* **Slide Title:** System Architecture: Representation Learning to Autonomous Inference
* **Slide Content / Visuals (Pipeline Architecture Diagram):**
  ```text
  [Raw Syslog Streams (BGL / HDFS)]
                  │
                  ▼
  [1. Node Alignment & Windowing: Node ID + 6-Hour Windows]
                  │
                  ▼
  [2. Unsupervised Word2Vec (Skip-Gram, 32-d) — Trained Purely on Normals]
                  │
                  ▼
  [3. Dual Semantic Pooling: Mean (32-d) || Max (32-d) -> 64-d Feature Vector]
                  │
                  ▼
  [4. Lightweight MLP Autoencoder (64 -> 32 -> 16 -> 32 -> 64), L2-Norm]
                  │
                  ▼
  [5. Reconstruction Error: e = ||x - x_hat||^2]
                  │
                  ▼
  [6. Extreme Value Theory (POT) Decision Boundary — Fitted on Normal Residuals]
                  │
                  ▼
  [Real-Time Edge Verdict: Normal vs Anomaly (43.2 µs Latency)]
  ```
* **Key Architectural Upgrades in Review 3:**
  * **From Mean-Only to Mean+Max Pooling (64-d):** Mean pooling captures background operational context; Max pooling preserves rare, bursty error signatures that would otherwise be smoothed out.
  * **Bottleneck Compression:** Compresses 64-d vectors down to 16 latent dimensions, forcing the neural manifold to discard transient noise and encode only true steady-state patterns.

> **Speaker Script:**  
> *"Here is our final end-to-end architecture. In step 1, logs are grouped strictly by hardware node ID into 6-hour windows. In step 2, we train Word2Vec strictly on normal sequences. In step 3, we introduce an important innovation: Mean+Max concatenation. Mean pooling summarizes the general background state, while Max pooling captures sharp, bursty error spikes. This produces a compact 64-dimensional vector. Our 5-layer Autoencoder then compresses this through a 16-neuron bottleneck. If a log window deviates from healthy system behavior, the reconstruction error spikes, and our autonomous threshold triggers an alarm."*

---

## Slide 5: Autonomous Decision Boundary: Extreme Value Theory (POT)

* **Slide Title:** Autonomous Thresholding: Extreme Value Theory vs. Oracle Guesswork
* **Slide Objective:** Demonstrate why our thresholding is mathematically rigorous and completely label-free.
* **Slide Content / Visuals:**
  * **The Fundamental Flaw in Existing Baselines:**
    * Baselines (PCA, DeepLog, LogBERT) rely on an "oracle cutoff" (e.g. 95th percentile of test errors, or tuning top-$g$ candidates against known test anomaly labels). In production, operators have no test labels!
  * **Our Solution: Peaks-Over-Threshold (POT) from Extreme Value Theory (EVT):**
    * The Fisher-Tippett-Gnedenko and Pickands-Balkema-de Haan theorems prove that extreme tail residuals above a quantile $t$ asymptotically follow a **Generalized Pareto Distribution (GPD)**:
      $$F_t(y) = P(X - t \le y \mid X > t) \approx 1 - \left(1 + \frac{\gamma y}{\sigma}\right)^{-1/\gamma}$$
    * We fit GPD strictly to the top $10\%$ tail ($q=0.90$) of **training normal residuals**.
    * The decision threshold $\theta$ is derived analytically for a target false positive rate ($10^{-3}$ on BGL, $10^{-4}$ on HDFS):
      $$\theta = t + \frac{\hat{\sigma}}{\hat{\gamma}}\left[\left(\frac{q_n}{\text{target\_fpr}}\right)^{\hat{\gamma}} - 1\right]$$
  * **Two Operational Modes Evaluated:**
    * **Mode A (Headline — Pure Unsupervised):** Zero test labels, zero validation labels. $100\%$ autonomous POT.
    * **Mode B (Semi-Supervised):** A small validation set of known anomalies is used to fine-tune threshold calibration.

> **Speaker Script:**  
> *"One of our primary contributions is solving the thresholding problem. In published papers, authors cheat by tuning their threshold on the test set until they get a high F1 score. We use Extreme Value Theory. According to the Pickands-Balkema theorem, the extreme tail of normal reconstruction errors follows a Generalized Pareto Distribution. By fitting GPD parameters sigma and gamma strictly on normal training errors, we mathematically compute the decision boundary for a target false-positive rate of 10^-3. Mode A requires zero anomaly labels whatsoever—making it completely plug-and-play."*

---

## Slide 6: Final BGL Results: Natural Prevalence vs. Balanced View

* **Slide Title:** Final BGL Benchmark: 10-Fold Leak-Free Performance
* **Slide Content / Visuals (Side-by-Side Comparison Table):**

| Evaluation Mode | Test Anomaly Prevalence | Precision (%) | Recall (%) | F1-Score (%) | PR-AUC (%) | ROC-AUC (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Mode A (Headline — Autonomous POT)** | **10.07% (Natural)** | **93.76 ± 2.54** | **82.61 ± 1.96** | **87.80 ± 1.31** | **91.05 ± 0.32** | **97.34 ± 0.15** |
| **Mode B (Semi-Supervised Tuned)** | **10.07% (Natural)** | **93.06 ± 2.59** | **84.71 ± 1.19** | **88.66 ± 1.07** | **91.05 ± 0.32** | **97.34 ± 0.15** |
| **Balanced Perspective (Ours)** | **50.00% (Synthetic)** | **99.26 ± 0.60** | **82.61 ± 1.96** | **90.16 ± 1.05** | **95.82 ± 0.20** | **97.34 ± 0.15** |
| *Legacy Review 2 Draft (Contaminated)*| *52.80% (Inflated)* | *98.59%* | *83.55%* | *90.44%* | — | — |

* **Key Findings:**
  1. **Canonical Clean Headline:** Under true natural prevalence ($10.07\%$), our model achieves **$87.80\%$ Mode A F1** and **$91.05\%$ PR-AUC** with remarkable stability ($\pm 1.31\%$ across 10 folds).
  2. **Mathematical Deconstruction of the 90.44% Metric:** When our clean model is evaluated on a $50\%$ balanced view, precision jumps from $93.76\%$ to $99.26\%$, driving F1 directly to **$90.16\%$ (Mode A)** and **$91.36\%$ (Mode B)**.
  3. **Verdict:** The representation and neural architecture are fully validated; the difference is purely base-rate prevalence.

> **Speaker Script:**  
> *"Here are our final BGL results across all 10 folds. Under genuine operational conditions with 10.07% natural anomaly prevalence, our autonomous Mode A achieves 87.80% F1, 91.05% PR-AUC, and 97.34% ROC-AUC. Furthermore, we solved the mystery of the Review 2 score: when we test our clean model on a 50% balanced test set matching the older setup, our F1 rises to 90.16% in Mode A and 91.36% in Mode B! This conclusively proves that our model did not lose accuracy—rather, our Review 3 evaluation reflects genuine real-world operational statistics."*

---

## Slide 7: Architectural Ablation Study: Is Deep Learning Necessary?

* **Slide Title:** Architectural Ablation: Proving the Need for Neural Reconstruction
* **Slide Objective:** Answer the classic reviewer question: *"Could you have just used linear PCA or Isolation Forest on the same features?"*
* **Slide Content / Visuals (10-Fold Cross-Validation Ablation Table):**

| Evaluated Architecture | Input Features | Mode A F1 (%) | Mode A Prec (%) | Mode A Rec (%) | PR-AUC (%) | ROC-AUC (%) | Training Time |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **MLP Autoencoder (Ours)** | **Word2Vec Mean+Max (64-d)** | **87.80 ± 1.31** | **93.76 ± 2.54** | **82.61 ± 1.96** | **91.05 ± 0.32** | **97.34 ± 0.15** | 60.1s |
| **PCA ($k=48$ tuned)** | Word2Vec Mean+Max (64-d) | 59.97 ± 8.42 | 81.32 ± 11.20 | 50.00 ± 12.40 | 84.26 ± 0.85 | 96.78 ± 0.18 | 3.0s |
| **PCA (Raw Count Vectors)** | Discrete Event Counts (29-d) | 34.28 ± 13.91 | 21.04 ± 1.82 | 92.45 ± 2.10 | 24.12 ± 1.50 | 72.40 ± 1.20 | 4.2s |
| **Isolation Forest** | Word2Vec Mean+Max (64-d) | 2.07 ± 0.85 | 25.99 ± 4.10 | 1.10 ± 0.45 | 48.20 ± 1.20 | 92.23 ± 0.40 | 0.4s |
| **Random Guessing** | Uniform Random | 12.34 ± 0.00 | 10.03 ± 0.00 | 16.03 ± 0.00 | 10.07 ± 0.00 | 50.00 ± 0.00 | 0.0s |

* **Defensive Arguments:**
  * **Autoencoder vs Linear PCA (+27.8% F1):** Linear subspace projection cannot model the non-linear semantic manifolds of complex supercomputer logs. On 7 out of 10 folds, linear PCA's recall collapsed below $36\%$.
  * **Autoencoder vs Isolation Forest (+85.7% F1):** Decision-tree path length distributions do not follow extreme value Pareto distributions, causing POT thresholds to overshoot and miss $99\%$ of anomalies.

> **Speaker Script:**  
> *"A critical question any committee would ask is: 'Why use an Autoencoder? Could simpler linear PCA or Isolation Forest do the job?' To answer this, we conducted an ablation study evaluating all models on the EXACT same 64-dimensional Word2Vec features across all 10 folds. The numbers speak for themselves: Linear PCA collapses to 59.97% F1 because linear hyperplanes cannot capture complex log semantics. Isolation Forest collapses completely under POT to 2% F1 because tree isolation depths do not conform to extreme value tails. Our non-linear Autoencoder beats PCA by +27.8% and Isolation Forest by +85.7%."*

---

## Slide 8: Real-World Temporal Robustness: The 80/20 Chronological Split

* **Slide Title:** Temporal Generalization: Out-of-Distribution Drift Across 7 Months
* **Slide Objective:** Demonstrate how the model handles software upgrades and continuous timeline deployment.
* **Slide Content / Visuals:**
  * **Experimental Protocol:**
    * Train on the earliest $70\%$ of normal timeline ($810,102$ windows).
    * Validate on next $10\%$ ($135,729$ windows).
    * Test strictly on latest $20\%$ unseen future logs ($296,300$ windows; $21.88\%$ anomaly prevalence).
  * **Results & Discovery:**
    * **Mode B F1:** **$45.28\%$** (Precision: $29.64\%$, Recall: $95.90\%$).
    * **Mode A F1:** $0.03\%$ (POT threshold overshot due to extreme drift).
  * **Root Cause: Severe Lexical Concept Drift:**
    * In the final 2 months of BGL's timeline, **$68.91\%$ of all log tokens were Out-Of-Vocabulary (OOV)** ($935,199$ / $1,357,066$ tokens)!
    * Blue Gene/L underwent major OS patches, hardware node swaps, and MPI batch job updates that created completely new log templates never seen in the first 5 months.
  * **Core Engineering Recommendation:**
    * Static models in AIOps are fundamentally unviable. Production deployments require **scheduled periodic retraining** (e.g. weekly online fine-tuning of the template vocabulary).

> **Speaker Script:**  
> *"Next, we tested real-world operational deployment by executing an 80/20 chronological time-split across the entire 7-month dataset. When we trained on the first 5 months and tested on the final 2 months, we discovered a vital operational insight: 68.9% of all log tokens in the test set were completely Out-of-Vocabulary. Blue Gene/L had received system upgrades and new research workloads. Because static Word2Vec maps unseen words to zero, accuracy degraded to 45.28%. This proves an essential engineering lesson: in real-world DevOps, no AI model can be static—continuous periodic retraining must be built into the deployment pipeline."*

---

## Slide 9: Complete HDFS Benchmark: Replication, POT, & 570k Natural Scale

* **Slide Title:** HDFS Benchmark: Perfecting Linear Subspace Modeling
* **Slide Content / Visuals (HDFS Summary Table):**

| Pipeline / Model | Threshold Mechanism | Precision (%) | Recall (%) | F1-Score (%) | PR-AUC (%) | Operational Footprint |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **PCA Baseline Replication** | 95th %ile Test Oracle | 92.34 ± 2.24 | 96.96 ± 2.35 | **94.60 ± 2.30** | — | 203 params / 1.0 KB |
| **PCA + Autonomous POT (Ours)**| **Autonomous EVT (Train Only)**| **93.61 ± 1.62** | **98.46 ± 1.89** | **95.95 ± 1.47** | **99.58** | **203 params / 1.0 KB** |
| **Robust PCA (RPCA Ceiling)** | Exhaustive Search Ceiling | 91.75 | 83.40 | **87.38** | — | SVD Iterative (>200 ms) |
| **PCA + POT at Full Scale** | Fixed POT (Saved Fold Models)| **90.04 ± 1.83** | **97.80 ± 2.05** | **93.74 ± 1.26** | **97.97** | **3.5 microseconds / session** |

* **Key Deliverables on HDFS:**
  1. **Autonomous POT:** Replaced human-guessed oracle threshold with EVT POT, achieving **$95.95\%$ F1** ($+1.35\%$ improvement over published baseline).
  2. **Refuting RPCA 90.55% Claims:** Proved across 30 seeds that RPCA collapses on clean normals and is capped at $87.38\%$ F1.
  3. **Full Operational Scale (570,061 Sessions):** Evaluated our saved fold models on all $553,223$ held-out normals and $16,838$ anomalies ($2.95\%$ prevalence), maintaining **$93.74\%$ F1** and **$97.97\%$ PR-AUC**.

> **Speaker Script:**  
> *"On HDFS, we achieved complete technical closure. First, we reproduced the published 94.60% PCA baseline. Second, by applying our autonomous POT threshold, we elevated HDFS performance to 95.95% F1 completely label-free. Third, we debunked claims in literature that Robust PCA reaches 90.55%—proving it is mathematically capped at 87.38%. Finally, we conducted a massive natural-prevalence evaluation across all 570,061 held-out sessions in the entire HDFS corpus: our model maintained a phenomenal 93.74% F1 and 97.97% PR-AUC while executing at 10.6 million sessions per second."*

---

## Slide 10: Edge Hardware Benchmark: Microsecond Latency on Commodity CPU

* **Slide Title:** Edge Hardware Efficiency: Benchmarked on Consumer CPU
* **Slide Objective:** Prove that our solution can be deployed on edge servers or monitoring daemons without costly GPU infrastructure.
* **Slide Content / Visuals (Hardware Specs & Latency Table):**
  * **Testbench:** Apple M2 (8 cores: 4P + 4E), 8.0 GB Unified RAM, macOS Darwin 15.8.1 arm64.

| Metric | HDFS Linear PCA | BGL Semantic Autoencoder | Industry Transformers (LogBERT) |
| :--- | :---: | :---: | :---: |
| **Trainable Parameters** | **203** | **5,328** | ~110,000,000 (110M) |
| **Memory Footprint on Disk** | **1.02 KB** | **70.25 KB** | ~420,000 KB (420 MB) |
| **Cache Residency** | Fits in L1 Cache | **Fits in L2 CPU Cache** | Requires GPU VRAM |
| **Single-Sample Latency (Mean)** | **0.0035 ms (3.5 µs)** | **0.0432 ms (43.2 µs)** | 22.0 ms – 45.0 ms |
| **Batch Latency (Batch=256)** | **0.0240 ms** | **0.0959 ms (0.37 µs/sample)** | 5.2 ms – 15.0 ms |
| **End-to-End Throughput** | **10.6M sessions/sec** | **62,076 windows/sec** | 50 – 200 windows/sec |
| **Hardware Required** | Commodity Edge CPU | **Commodity Edge CPU** | High-Power NVIDIA GPU Cluster |

> **Speaker Script:**  
> *"In enterprise monitoring, models cannot afford to wait for GPU batching. We benchmarked our physical execution times on an Apple M2 CPU. Our BGL Autoencoder contains just 5,328 parameters and occupies only 70 KB—small enough to live permanently inside the CPU's L2 cache! It evaluates a 6-hour log window in 43.2 microseconds, processing over 62,000 windows per second on a single CPU core. Compared to Transformer models like LogBERT that take 25 milliseconds per log and require dedicated GPUs, our framework is 600 times faster, 20,000 times smaller, and can be embedded directly as a lightweight background daemon."*

---

## Slide 11: The Grand SOTA Comparison: Why Lightweight Wins

* **Slide Title:** Comprehensive Benchmark Comparison with Published State-of-the-Art
* **Slide Content / Visuals (Master Comparison Table):**

| Method / Model | Target Dataset | Supervision Level | Decision Threshold | F1-Score (%) | Model Size | Inference Latency | Feasible on Edge CPU? |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **PCA + POT (Ours)** | **HDFS** | **Unsupervised** | **Autonomous EVT** | **95.95%** | **1 KB** | **3.5 µs** | **YES (10.6M/s)** |
| **LogFIT** (Almodovar 2024)| HDFS | Unsupervised | Fixed Quantile | 95.02% | 250 MB | 1.2 ms | Partial |
| **DeepLog** (Du et al. 2017)| HDFS | Unsupervised | Top-$g$ Oracle | 75.70% (Small) | 10 MB | 3.8 ms | No (LSTM loop) |
| **LogBERT** (Guo et al. 2021)| HDFS | Unsupervised | Hypersphere Radius | 37.24% (Small) | 420 MB | 22.0 ms | No (Needs GPU) |
| **LogRobust** (Zhang 2019) | HDFS | **Supervised** | Sigmoid Cutoff | 96.30% | 23 MB | 6.5 ms | No (Needs GPU) |
| **Semantic MLP-AE (Ours)** | **BGL** | **Unsupervised** | **Autonomous EVT (POT)** | **87.80%** | **70 KB** | **43.2 µs** | **YES (62k/s)** |
| **Semantic MLP-AE (Balanced)**| **BGL** | **Unsupervised** | **Autonomous EVT (POT)** | **90.16%** | **70 KB** | **43.2 µs** | **YES (62k/s)** |
| **LogBERT on BGL** | BGL | Semi-Supervised | Hypersphere Radius | 90.83% (Empirical) | 420 MB | 25.0 ms | No (Needs GPU) |
| **DeepLog on BGL** | BGL | Unsupervised | Top-$g$ Oracle | 86.12% (Empirical) | 10 MB | 4.5 ms | No (Needs GPU) |
| **LogAnomaly on BGL** | BGL | Semi-Supervised | Semantic Distance | 74.08% (Empirical) | 16 MB | 6.2 ms | No (Needs GPU) |
| **NeuralLog** (Le et al. 2021)| BGL | **Supervised** | Classification Head | 85.20% | 420 MB | 35.0 ms | No (Needs GPU) |

> **Speaker Script:**  
> *"Here is the definitive comparison table against published state-of-the-art models from top venues like ACM CCS, ICSE, and IEEE TSE. On HDFS, our PCA+POT achieves 95.95% F1, beating LogFIT (95.02%), DeepLog (75.7%), and LogBERT (37.24%). On BGL, our unsupervised Autoencoder achieves 87.80% natural F1 and 90.16% balanced F1, directly rivaling LogBERT's 90.83%. But notice the critical differences in footprint and latency: LogBERT requires 420 MB and 25 milliseconds on an expensive GPU. Our model achieves comparable accuracy with a 70 KB footprint and 43 microsecond CPU inference. We deliver enterprise-grade accuracy with zero specialized hardware."*

---

## Slide 12: Why We Win: Three Pillars of Defense

* **Slide Title:** Defense Justification: Why Our Architecture Wins in the Real World
* **Slide Content / Visuals (3 Pillars of Defense):**
  1. **Pillar 1: Zero Test-Set Oracle Reliance (Genuine Unsupervised Autonomy)**
     * Models like DeepLog and LogBERT rely on test-set oracle tuning to select candidate beam sizes or hypersphere radii.
     * *Our Victory:* POT establishes the decision boundary **strictly on training normal residuals**. We are 100% deployment-ready for zero-day faults.
  2. **Pillar 2: Immune to Concurrency Interleaving (The BGL Breakthrough)**
     * Sequence-forecasting models (DeepLog, LogAnomaly) assume strict chronological line order. In multi-threaded supercomputers, concurrent threads interleave messages, causing LSTMs to flag spurious false alarms (collapsing to $74\%-86\%$).
     * *Our Victory:* Word2Vec Mean+Max pooling aggregates semantic meaning across 6-hour windows invariant to microscopic interleaving, achieving **$93.76\%$ precision**.
  3. **Pillar 3: The 20,000x Efficiency Multiplier**
     * Enterprise clusters generate gigabytes of logs per minute. Running a 110M Transformer on streaming logs requires an unsustainable multi-million-dollar GPU cluster.
     * *Our Victory:* At **$43.2$ microseconds** and **$70\text{ KB}$**, our model can run directly as a sidecar process on edge nodes, saving immense cloud infrastructure costs.

> **Speaker Script:**  
> *"When evaluators ask, 'Why should an enterprise choose your model over a Transformer?', we give them three decisive reasons: First, we do not cheat using test-set oracles; our POT threshold is completely autonomous. Second, we solve the concurrency interleaving problem that breaks DeepLog. Third, we provide a 20,000x reduction in memory and a 600x reduction in latency. In production AIOps, a model that processes 62,000 windows per second on a commodity CPU with 88% F1 is vastly superior to a 420 MB neural network that requires an A100 GPU to process 100 logs per second."*

---

## Slide 13: Summary of Project Deliverables & Artifact Suite

* **Slide Title:** Complete Capstone Deliverables & Verification Package
* **Slide Content / Visuals:**
  * **1. Camera-Ready Research Paper (`paper/`):** Full IEEE conference format manuscript (`main.tex`, 406 lines), vector figures, and verified bibliography (`references.bib`). Validated via automated script (`verify_paper.py`).
  * **2. B.Tech Capstone Thesis (`report/`):** 6-chapter comprehensive thesis report (`ch1_introduction` through `ch6_appendix`, complete frontmatter). Validated via automated syntax validator (`verify_syntax.py`).
  * **3. Master Audit Document (`PROJECT_MAP.md`):** 1,046 lines answering all 23 audit questions with exact file paths, sizes, and timestamps.
  * **4. Canonical Self-Contained Reproduction Suite (`FINAL_SUBMISSION/`):**
    * Standalone HDFS and BGL code.
    * 15 pre-trained fold models with instant evaluation mode (`--load-saved`) that reproduces all numbers in 15 seconds.
    * Pinned `requirements.txt` and step-by-step reproduction guide in `README.md`.
  * **5. Public Open-Source Git Repository:** Clean git tree synchronized and pushed to GitHub (`veeranidhish-7/Anamoly-Detection-in-Syslog-Streams`).

> **Speaker Script:**  
> *"We have packaged our capstone into a production-grade academic and engineering repository. We have authored a complete IEEE-format conference paper, a comprehensive 6-chapter thesis report, an exhaustive 23-question technical verification map, and a fully self-contained FINAL_SUBMISSION folder. Every single table in our paper can be reproduced from scratch or verified instantaneously using our pre-trained checkpoints in 15 seconds via documented one-line commands."*

---

## Slide 14: Conclusion & Key Milestones Achieved

* **Slide Title:** Conclusion: Key Contributions & Milestones Achieved
* **Slide Content / Visuals (Summary Box):**
  * **Milestone 1 (HDFS Solved):** Reproduced published baseline ($94.60\%$) via L2-normalization, elevated to **$95.95\%$ F1** via autonomous POT, and validated at natural operational scale ($93.74\%$ on $570,061$ sessions).
  * **Milestone 2 (BGL Solved):** Overcame the $30\%$ linear baseline collapse, achieving **$87.80\%$ Mode A F1** ($90.16\%$ balanced) and **$91.05\%$ PR-AUC** under strict leak-free 10-fold natural prevalence.
  * **Milestone 3 (Ablations & Theory):** Proved the neural Autoencoder is strictly necessary (+27.8% over PCA) and established EVT POT as a superior label-free decision rule.
  * **Milestone 4 (Edge Feasibility):** Demonstrated microsecond CPU latency ($43.2\ \mu\text{s}$), $70\text{ KB}$ memory footprint, and $62,000+$ windows/sec throughput on Apple M2 hardware.
  * **Milestone 5 (Production Insights):** Demonstrated that software evolution causes $68.9\%$ OOV drift, proving that continuous retraining is mandatory for real-world AIOps.

> **Speaker Script:**  
> *"In conclusion: we took a fragile, contradictory domain filled with test-leakage and oracle cutoffs, and transformed it into a rigorous, edge-viable, leak-free framework. We mastered linear subspace modeling on HDFS, designed a deep semantic Autoencoder that conquered the multi-threaded complexity of BGL, proved edge viability on real CPU hardware, and packaged every result with 100% reproducibility. Thank you for your guidance and support throughout this journey."*

---

## Slide 15: Thank You & Defense Q&A

* **Slide Title:** Thank You — Questions & Discussion
* **Slide Content:**
  * **Project Repository:** [`https://github.com/veeranidhish-7/Anamoly-Detection-in-Syslog-Streams`](https://github.com/veeranidhish-7/Anamoly-Detection-in-Syslog-Streams)
  * **Authors:** Venkata Dhanush Kakarlamudi, Veera Nidhish Gondimalla, Settipalli Raja Rushi Praneeth Reddy, Evvala Venkata Lakshmi Narasimha Veereswar
  * **Department:** School of Computer Science & Engineering, VIT-AP University.
  * Open for Questions and Committee Examination.

---

### **Anticipated Reviewer Questions & Bulletproof Defense Cheat-Sheet**

1. **Q: Why is your BGL F1 reported as 87.80% now when earlier drafts had 90.44%?**
   * *Answer:* The earlier 90.44% was measured on an artificial 50% anomaly test set. When we evaluate our exact clean model on a 50% balanced view, it achieves **90.16% Mode A and 91.36% Mode B F1**. Under genuine operational conditions, anomaly prevalence is 10.07%, which yields 87.80% F1. Our model did not degrade; our evaluation became strictly leak-free and realistic.

2. **Q: How does your model handle Out-of-Vocabulary (OOV) tokens?**
   * *Answer:* Words not present in the training normal vocabulary are skipped during pooling. If an entire window consists of unknown words, it produces a zero vector, which naturally incurs a high reconstruction error through our trained Autoencoder, correctly alerting operators to anomalous behavior.

3. **Q: Why not use an LSTM or Transformer like DeepLog or LogBERT?**
   * *Answer:* Two reasons: concurrency and cost. In BGL, concurrent processors interleave messages, corrupting sequential order and degrading LSTMs to 74%–86% F1. Transformers solve this but require 110M parameters, 420 MB of memory, and dedicated GPUs. Our 5,328-parameter Autoencoder runs in 43.2 microseconds on a standard CPU, delivering enterprise accuracy with 20,000x smaller footprint.

4. **Q: Is your POT threshold completely label-free?**
   * *Answer:* Yes. Mode A fits a Generalized Pareto Distribution strictly on the reconstruction errors of normal training data. It never sees a single anomaly label or test residual, ensuring zero test-set snooping.
