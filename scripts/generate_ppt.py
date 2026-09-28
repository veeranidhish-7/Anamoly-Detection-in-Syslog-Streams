from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

def create_presentation():
    prs = Presentation()

    # Slide 1: Title Slide
    slide_layout = prs.slide_layouts[0] # Title slide layout
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    
    title.text = "Anomaly Detection in Syslog Streams"
    subtitle.text = ("Capstone Review 1\n\n"
                     "Team Members:\n"
                     "- Venkata Dhanush Kakarlamudi (23BCE8172)\n"
                     "- Veera Nidhish Gondimalla (23BCE7421)\n"
                     "- Settipalli Raja Rushi Praneeth Reddy (23BCE7425)\n"
                     "- Evvala Venkata Lakshmi Narasimha Veereswar (23BCE7439)")

    # Adjust title formatting
    for paragraph in title.text_frame.paragraphs:
        paragraph.font.size = Pt(40)

    # Slide 2: Introduction & Base Paper Study
    slide_layout = prs.slide_layouts[1] # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "1. Introduction & Base Paper Study"
    
    content = slide.placeholders[1]
    tf = content.text_frame
    tf.text = "Primary Goal: Develop robust log anomaly detection architectures across complex datasets."
    
    p = tf.add_paragraph()
    p.text = "Base Paper Studied: 'Lightweight Optimization based Log-file Anomaly Detection' (2025 IEEE ICSRS)."
    p.level = 0
    
    p = tf.add_paragraph()
    p.text = "Base Approach: Uses frequency-based linear models (PCA, RPCA) on count-based matrices."
    p.level = 0
    
    p = tf.add_paragraph()
    p.text = "The Challenge: These standard models excel on simple data (HDFS) but struggle heavily with real-world, interleaved logs (BGL)."
    p.level = 0

    # Slide 3: Baseline Replication (PCA Model)
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "2. Baseline Replication (PCA Model)"
    
    content = slide.placeholders[1]
    tf = content.text_frame
    tf.text = "Objective: Understand and replicate the linear models (PCA, RPCA) from the base paper."
    
    p = tf.add_paragraph()
    p.text = "HDFS Dataset (Structured):"
    p.level = 0
    
    p = tf.add_paragraph()
    p.text = "Discovered a hidden L2-normalization requirement."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "Successfully matched base paper: PCA achieved 94.65% F1 score."
    p.level = 1

    p = tf.add_paragraph()
    p.text = "BGL Dataset (Complex, Interleaved):"
    p.level = 0
    
    p = tf.add_paragraph()
    p.text = "Tested on 4.7 million real-world sequences."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "Linear PCA collapsed to 30.18% F1 (with a strict ceiling of ~65% even with oracle thresholding)."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "Conclusion: Count-based linear models are fundamentally dataset-dependent."
    p.level = 1

    # Slide 4: Proposed Architectural Improvements
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "3. Proposed Architecture Improvements"
    
    content = slide.placeholders[1]
    tf = content.text_frame
    tf.text = "Objective: Overcome the limitations of linear models on complex datasets."
    
    p = tf.add_paragraph()
    p.text = "Step 1: Sequence Order Embeddings (Semantic NLP)"
    p.level = 0
    
    p = tf.add_paragraph()
    p.text = "Replaced sparse event counts with dense Word2Vec embeddings."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "Captures the temporal execution context rather than just frequency."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "Step 2: Structural Node-Based Grouping"
    p.level = 0
    
    p = tf.add_paragraph()
    p.text = "Replaced arbitrary time windows with logical grouping by Server Node and sliding Window_ID."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "Accurately reflects actual physical execution paths instead of a 'semantic soup'."
    p.level = 1

    # Slide 5: Deep Learning Autoencoder & Results
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "4. Deep Learning Implementation & Results"
    
    content = slide.placeholders[1]
    tf = content.text_frame
    tf.text = "Step 3: Multi-Layer Perceptron (MLP) Autoencoder"
    
    p = tf.add_paragraph()
    p.text = "Replaced the linear PCA detector with a deep learning Autoencoder."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "Designed to map and reconstruct the non-linear semantic vector space."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "Results on BGL Dataset:"
    p.level = 0
    
    p = tf.add_paragraph()
    p.text = "The Autoencoder shattered the linear 65% ceiling."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "Achieved an average 87.46% F1-score across rigorous 5-fold cross-validation."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "Threshold Automation (Phase 5):"
    p.level = 0

    p = tf.add_paragraph()
    p.text = "Implemented dynamic Extreme Value Theory (POT) to automatically model error tails, making models deployable without hardcoded cutoffs."
    p.level = 1


    # Slide 6: Summary for Review 1
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "5. Summary for Review 1"
    
    content = slide.placeholders[1]
    tf = content.text_frame
    tf.text = "1. Studied the Research Paper: Understood the theoretical workings of baseline anomaly detection models."
    
    p = tf.add_paragraph()
    p.text = "2. Replicated PCA Models: Successfully reproduced the paper's claims on simple data, and identified its points of failure on complex systems."
    p.level = 0
    
    p = tf.add_paragraph()
    p.text = "3. Proposed Improvements: Devised and implemented a robust architecture using Node-Based Grouping, Semantic Embeddings, and Deep Learning Autoencoders."
    p.level = 0
    
    p = tf.add_paragraph()
    p.text = "4. Validation: Demonstrated significant improvements over the baseline on real-world interleaved data streams."
    p.level = 0

    prs.save('docs/Capstone_Review_1_Presentation.pptx')
    print("Presentation saved successfully at 'docs/Capstone_Review_1_Presentation.pptx'")

if __name__ == '__main__':
    create_presentation()
