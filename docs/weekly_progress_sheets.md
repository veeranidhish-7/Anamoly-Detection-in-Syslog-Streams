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
* Review the feedback given by the review panel and identify areas to improve.
* Work on testing the model in more realistic, real-world conditions instead of simplified test sets.

---

## Week 10 (October 6 - October 12)
**Tasks Completed:**
* Analyzed the panel feedback and updated our testing strategy to reflect real-world anomaly rates.
* Set up a proper training pipeline that trains only on normal system logs without seeing any anomalies.

**Tasks Planned for next week:**
* Improve the log feature extraction so the model can catch both normal background activity and sudden error bursts.
* Upgrade the Autoencoder architecture to better learn these richer log features.

---

## Week 11 (October 13 - October 19)
**Tasks Completed:**
* Improved the feature extraction using both average and peak pooling to capture rare error signals.
* Redesigned and tuned a deeper Autoencoder network with regularization to prevent overfitting on routine logs.

**Tasks Planned for next week:**
* Combine our automatic threshold algorithm with the new Autoencoder.
* Run full cross-validation tests across the entire dataset to verify consistent accuracy.

---

## Week 12 (October 20 - October 26)
**Tasks Completed:**
* Successfully integrated the automatic thresholding method with our updated Autoencoder.
* Ran complete cross-validation tests across all folds and confirmed high, reliable detection performance.

**Tasks Planned for next week:**
* Compare our Autoencoder against simpler models like PCA and Isolation Forest on the exact same features.
* Test how well the trained model holds up over time as system logs change over several months.

---

## Week 13 (October 27 - November 2)
**Tasks Completed:**
* Ran comparison tests and proved that our deep learning Autoencoder clearly beats traditional machine learning baselines.
* Tested the model over a chronological timeline and observed how new system updates introduce unfamiliar log patterns.

**Tasks Planned for next week:**
* Measure the speed and memory usage of the model to prove it can run efficiently on regular computers.
* Compare our results against existing published models from top research papers.

---

## Week 14 (November 3 - November 9)
**Tasks Completed:**
* Tested the model's speed and memory footprint, proving it runs fast enough for real-time edge monitoring on a standard CPU.
* Built a comprehensive comparison table showing how our lightweight model compares with large language models and transformers.

**Tasks Planned for next week:**
* Work on drafting the final project report chapters and research paper.
* Clean up the codebase and organize all saved models and scripts so anyone can easily re-run them.

---

## Week 15 (November 10 - November 16)
**Tasks Completed:**
* Wrote and finalized the complete final project report and paper draft covering all our methodology and findings.
* Packaged the clean code, saved models, and presentation slides into the final submission folder for the upcoming defense.

**Tasks Planned for next week:**
* Deliver the final Capstone Review presentation and defend our work in front of the evaluation committee.
* Complete all remaining departmental submission requirements and archive the final project files.

