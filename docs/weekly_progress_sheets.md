# Weekly Progress Sheets

## Week 0 (July 28 - August 3)
**Tasks Completed:**
* Brainstormed potential capstone projects, identified log anomaly detection as a critical problem, and finalized the topic. 
* Outlined the initial tasks, objectives, and overall architecture for the project.

**Tasks Planned for next week:**
* Study base research papers and analyze existing log anomaly detection methods.
* Prepare initial structured datasets for baseline testing.

---

## Week 1 (August 4 - August 10)
**Tasks Completed:**
* Studied the base research paper and analyzed existing log anomaly detection methods.
* Downloaded and prepared the structured HDFS dataset for initial testing.

**Tasks Planned for next week:**
* Write the code for the lightweight baseline models (PCA and RPCA).
* Run the PCA model on the HDFS dataset.

---

## Week 2 (August 11 - August 17)
**Tasks Completed:**
* Wrote the code for PCA and RPCA baseline models. 
* Successfully ran the PCA model on the HDFS dataset and matched the paper's high accuracy.

**Tasks Planned for next week:**
* Test the RPCA model and evaluate its performance limitations.
* Acquire the BGL supercomputer dataset, which is much more complex and unstructured.

---

## Week 3 (August 18 - August 24)
**Tasks Completed:**
* Tested the RPCA model and noted its performance limitations compared to PCA.
* Acquired the BGL supercomputer dataset and set up the initial pipeline for it.

**Tasks Planned for next week:**
* Test the baseline models on this new BGL data to evaluate their robustness on complex data.
* Analyze why models might fail on unstructured logs.

---

## Week 4 (August 25 - August 31)
**Tasks Completed:**
* Ran the baseline models on the BGL dataset and proved that they fail on complex, unstructured data.
* Discovered that extracting logs purely by time mixes up unrelated events and ruins accuracy.

**Tasks Planned for next week:**
* Create a better way to extract logs by grouping them by their physical hardware node.
* Research NLP (Natural Language Processing) techniques like Word2Vec to help the AI understand the meaning of the logs.

---

## Week 5 (September 1 - September 7)
**Tasks Completed:**
* Built the node-based log grouping logic to correctly organize the messy BGL logs.
* Added the Word2Vec algorithm to convert the text logs into numerical data the AI can understand.

**Tasks Planned for next week:**
* Replace the basic linear math models with advanced Deep Learning models.
* Design and build a Deep Autoencoder Neural Network.

---

## Week 6 (September 8 - September 14)
**Tasks Completed:**
* Successfully built and trained the Deep Learning Autoencoder on the complex BGL data.
* Proved that the Autoencoder significantly outperforms the older baseline models.

**Tasks Planned for next week:**
* Find a way to automate the anomaly threshold instead of relying on human guessing (the top 5% rule).
* Research statistical methods to make the threshold adapt on its own.

---

## Week 7 (September 15 - September 21)
**Tasks Completed:**
* Added the dynamic POT (Peaks-Over-Threshold) mathematical algorithm to our pipeline.
* Successfully made the system autonomous, allowing it to flag anomalies automatically without human input.

**Tasks Planned for next week:**
* Audit the code to ensure there is no unfair data leakage between the training and testing phases.
* Write a strict testing loop to guarantee the results are mathematically stable.

---

## Week 8 (September 22 - September 28)
**Tasks Completed:**
* Implemented a strict 10-fold cross-validation testing loop to ensure zero data leakage.
* Finalized all the code, permanently saved the best models, and locked in a highly robust final accuracy score.

**Tasks Planned for next week:**
* Prepare presentation slides and comprehensive report for the Capstone Review.

---

## Week 9 (September 29 - October 5)
**Tasks Completed:**
* Prepared presentation slides for the Capstone Review.
* Practiced answering anticipated reviewer questions and delivered the final presentation.

**Tasks Planned for next week:**
* Review project feedback from Review 2 and plan future architectural enhancements.
* Investigate transitioning evaluation from prototype balanced data to natural operational prevalence.

---

## Week 10 (October 6 - October 12)
**Tasks Completed:**
* Evaluated Review 2 feedback and transitioned testing methodology from prototype balanced sets to natural operational base-rate prevalence (10.07%).
* Designed a strict stratified 10-fold cross-validation scheme ensuring pure normal training with zero anomaly exposure.

**Tasks Planned for next week:**
* Upgrade the log window feature representation from single pooling to dual Mean+Max pooling.
* Re-architect the autoencoder to accommodate higher-dimensional semantic embeddings.

---

## Week 11 (October 13 - October 19)
**Tasks Completed:**
* Implemented 64-dimensional dual Mean+Max semantic pooling to capture both operational baseline context and rare error bursts.
* Built and optimized a 5-layer regularized bottleneck Autoencoder (64 -> 32 -> 16 -> 32 -> 64) with L2 weight decay to prevent overfitting.

**Tasks Planned for next week:**
* Formulate and integrate autonomous Extreme Value Theory (POT) thresholding to eliminate manual threshold selection.
* Run full 10-fold cross-validation on BGL to evaluate the upgraded pipeline under natural operational conditions.

---

## Week 12 (October 20 - October 26)
**Tasks Completed:**
* Integrated autonomous Peaks-Over-Threshold (EVT / POT) mathematical thresholding fitted strictly on normal training data (Mode A).
* Executed the canonical 10-fold benchmark on BGL, locking in 87.80% Mode A F1 and 91.05% PR-AUC (with 90.16% confirmed under the balanced view).

**Tasks Planned for next week:**
* Perform architectural ablation studies comparing the Autoencoder against linear PCA and Isolation Forest on identical features.
* Test model resilience across time using a chronological split over the 7-month BGL operational history.

---

## Week 13 (October 27 - November 2)
**Tasks Completed:**
* Completed 10-fold ablation studies proving the Autoencoder outperforms linear PCA (+27.8% F1) and Isolation Forest (+85.7% F1) on the same features.
* Evaluated an 80/20 chronological time-split across 7 months of logs, discovering a 68.91% out-of-vocabulary concept drift requiring periodic updates.

**Tasks Planned for next week:**
* Measure physical hardware inference latency, throughput, and memory consumption on commodity CPU.
* Consolidate and cross-verify all experimental metrics across both HDFS and BGL datasets.

---

## Week 14 (November 3 - November 9)
**Tasks Completed:**
* Benchmarked physical edge execution on CPU, proving sub-millisecond latency (43.2 µs), 62,076 windows/sec throughput, and a 70.25 KB model footprint.
* Built a comprehensive State-Of-The-Art comparison table contrasting our framework against published models like LogBERT, DeepLog, and LogFIT.

**Tasks Planned for next week:**
* Draft the comprehensive 6-chapter B.Tech capstone thesis and compile the final research paper manuscript.
* Package clean, path-agnostic scripts and serialized models into a standalone submission repository.

---

## Week 15 (November 10 - November 16)
**Tasks Completed:**
* Authored the complete 6-chapter LaTeX capstone thesis and finalized the camera-ready research paper draft.
* Built the self-contained FINAL_SUBMISSION suite with path-agnostic reproduction scripts and created the final presentation slide decks.

**Tasks Planned for next week:**
* Deliver the final Capstone Review 3 grand defense and present project outcomes to the evaluation panel.
* Submit the finalized project thesis, repository artifacts, and research paper documentation for graduation clearance.

