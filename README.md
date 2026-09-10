# Plant Health Maize Project

## Corn Pathology AI

A machine-learning project for image-based diagnosis of maize leaf diseases, with a knowledge-base layer for returning disease information after classification.

The current implementation uses a validated **MobileNetV2-based maize disease classification pipeline**, integrated with a structured plant-health knowledge base and a confidence-based diagnostic decision layer.

The project has progressed through controlled V1, V2, and V3 model experiments. **V3 MobileNetV2 Stage 2 fine-tuning is the selected final model** based on overall test performance and improved handling of the primary Blight–Gray Leaf Spot confusion boundary.

---

# 1. Project Objectives

The main objective of the project is to investigate whether machine learning can support reliable image-based diagnosis of maize leaf diseases and provide useful information based on the predicted disease.

The project is guided by two central questions:

1. **Can we reliably diagnose plant diseases from images?**
2. **Can we provide useful and trustworthy information based on that diagnosis?**

The project therefore combines:

- Image dataset preparation and validation
- Exploratory dataset analysis
- Image preprocessing
- Data augmentation
- Class imbalance handling
- CNN-based image classification
- Transfer learning with MobileNetV2
- Controlled model experimentation
- Model evaluation
- Confidence-based decision handling
- Knowledge-base integration
- Diagnostic safety behavior
- Backend regression testing
- Reproducible analysis through Google Colab
- Preparation for future deployment

---

# 2. Current Maize Disease Classes

The current maize classification problem contains four classes:

1. **Blight**
2. **Common Rust**
3. **Gray Leaf Spot**
4. **Healthy**

The model therefore performs four-class image classification.

---

# 3. Dataset

The project uses the **Corn Pathology / maize disease image dataset**.

After dataset inspection and duplicate/conflict cleaning, the authoritative dataset contains:

| Class | Images |
|---|---:|
| Blight | 1,144 |
| Common_Rust | 1,306 |
| Gray_Leaf_Spot | 572 |
| Healthy | 1,162 |
| **Total** | **4,184** |

Four conflicting duplicate images were removed from the original 4,188-image collection.

The final dataset is the dataset used for the project experiments and evaluation.

---

# 4. Dataset Split

A stratified train/validation/test split was used.

| Split | Images |
|---|---:|
| Training | 2,928 |
| Validation | 628 |
| Test | 628 |
| **Total** | **4,184** |

The split preserves the class structure across the three partitions.

## Training distribution

| Class | Training Images | Percentage |
|---|---:|---:|
| Blight | 801 | 27.36% |
| Common_Rust | 914 | 31.22% |
| Gray_Leaf_Spot | 400 | 13.66% |
| Healthy | 813 | 27.77% |
| **Total** | **2,928** | **100%** |

Because Gray Leaf Spot has substantially fewer training examples, class weights were calculated and used during model training.

The final class weights were:

```text
Blight         = 0.913858
Common_Rust    = 0.800875
Gray_Leaf_Spot = 1.830000
Healthy        = 0.900369

# 5. Dataset Quality and Integrity

The final dataset was inspected before model development.

The integrity checks found:

- **Total images:** 4,184
- **Corrupted images:** 0
- **Different image dimensions detected:** 266
- **Most common dimension:** 256 × 256
- **Images at 256 × 256:** 3,852 (92.07%)
- **RGB images:** 4,179
- **RGBA images:** 4
- **CMYK images:** 1

The presence of different image dimensions was handled by the model input pipeline, which resized images to the required model input size.

The dataset cleaning process also identified conflicting duplicate files. Four conflicting duplicates were removed from the active dataset, while the corresponding files were retained in the quarantine area as cleaning evidence.

---

# 6. V1 Custom CNN Baseline

V1 was established as the project's custom CNN baseline.

The purpose of V1 was to provide a reference model against which later controlled experiments could be evaluated.

## V1 configuration

- Input size: **256 × 256**
- Channels: **RGB**
- Pixel scaling: **/255.0**
- Architecture: Custom CNN
- Convolutional layers: **4**
- Activation: **ReLU**
- Pooling: **Max Pooling**
- Regularization: **Dropout**
- Output: **4-class softmax**
- Data augmentation: Training data only
- Class imbalance: Class weights
- Training: **19 epochs**

The V1 model established a strong baseline before transfer learning was introduced.

---

# 7. V1 Evaluation

The V1 model achieved the following results on the held-out test set:

| Metric | V1 Result |
|---|---:|
| Test Loss | 0.180504 |
| Test Accuracy | **93.6306%** |
| Correct Predictions | 588 / 628 |
| Incorrect Predictions | 40 / 628 |
| Macro F1 | 92.32% |
| Weighted F1 | 93.69% |

## V1 Confusion Matrix

```text
[[147,   3,  20,   2],
 [  5, 189,   2,   0],
 [  8,   0,  78,   0],
 [  0,   0,   0, 174]]
```
---

# 8. Confidence Analysis

The final V3 MobileNetV2 model was evaluated using a confidence threshold of **70%** to distinguish accepted predictions from uncertain predictions.

The threshold was applied as:

```text
confidence >= 0.70
# 9. V2 Controlled Experiment

V2 was introduced as a controlled experiment to determine whether increasing the image input size and applying a different augmentation configuration would improve performance over the V1 baseline.

The V2 configuration used:

- Input size: **320 × 320**
- A moderate augmentation strategy
- The same four-class classification task
- The same train/validation/test split

## V2 Results

| Metric | V2 Result |
|---|---:|
| Test Accuracy | **89.01%** |
| Macro F1 | **86.83%** |
| Weighted F1 | **89.16%** |
| Blight ↔ Gray Leaf Spot errors | **47** |

V2 performed worse than the V1 baseline.

The increase in input size and the changed augmentation configuration did not provide the expected improvement. V2 was therefore **rejected as the final model**.

V1 remained the baseline for comparison while the project moved to transfer learning.

---

# 10. V3 MobileNetV2 Transfer Learning

V3 introduced transfer learning using **MobileNetV2 pretrained on ImageNet**.

The purpose of V3 was to determine whether a pretrained feature extractor could provide stronger and more generalizable image representations than the custom CNN used in V1.

## V3 Configuration

- Architecture: **MobileNetV2**
- Pretrained weights: **ImageNet**
- `include_top=False`
- Input size: **320 × 320**
- Input channels: **RGB**
- Preprocessing: MobileNetV2 `preprocess_input`
- Global Average Pooling
- Dropout: **0.30**
- Output layer: **4-class softmax**

Training-only augmentation:

```text
RandomFlip("horizontal")
RandomRotation(0.08)
RandomZoom(0.10)
RandomContrast(0.10)
```
---

# 11. V3 Stage 1 — Frozen Backbone

The first V3 training stage used the pretrained MobileNetV2 backbone with its convolutional layers frozen.

Only the classification head was trained during this stage.

## Stage 1 Configuration

- MobileNetV2 backbone: **Frozen**
- Trainable parameters: **5,124**
- Total parameters: **2,263,108**
- Global Average Pooling
- Dropout: **0.30**
- Output: **4-class softmax**

## Stage 1 Results

| Metric | V3 Stage 1 |
|---|---:|
| Test Accuracy | **92.1975%** |
| Macro F1 | **90.30%** |
| Weighted F1 | **92.24%** |

Stage 1 established the transfer-learning baseline before controlled fine-tuning of the upper portion of the MobileNetV2 backbone.

---

# 12. V3 Stage 2 — Controlled Fine-Tuning

Stage 2 fine-tuned the upper portion of the MobileNetV2 backbone while retaining the pretrained feature representations in the earlier layers.

Fine-tuning began from **layer 116 (`block_13_expand`)**.

Batch Normalization layers were excluded from fine-tuning to maintain stable pretrained representations.

## Stage 2 Configuration

- Fine-tuning start: **layer 116**
- Trainable backbone layers: **25**
- Trainable parameters: **1,668,484**
- Input size: **320 × 320**
- Training-only augmentation retained
- Output: **4-class softmax**

## Stage 2 Results

| Metric | V3 Stage 2 |
|---|---:|
| Test Loss | **0.154941** |
| Test Accuracy | **94.4268%** |
| Correct Predictions | **593 / 628** |
| Incorrect Predictions | **35 / 628** |
| Macro F1 | **92.97%** |
| Weighted F1 | **94.42%** |

Stage 2 improved the overall test performance compared with both the V1 custom CNN and V3 Stage 1.

---
# 13. V3 Primary Confusion Boundary

The most important classification boundary identified during evaluation was the confusion between:

- **Blight**
- **Gray Leaf Spot**

These two classes were therefore analyzed separately across the model experiments.

## Blight ↔ Gray Leaf Spot Errors

| Model | Combined Errors |
|---|---:|
| V1 | 28 |
| V2 | 47 |
| V3 Stage 2 | **23** |

V3 Stage 2 reduced the combined Blight–Gray Leaf Spot errors from 28 in V1 to 23.

This represents a reduction of approximately **17.9%**.

The reduction in this primary confusion boundary was an important factor in selecting V3 Stage 2 as the final model.

---

# 14. Model Comparison

The three major model configurations were compared using the same held-out test set.

| Model | Input Size | Test Accuracy | Macro F1 | Weighted F1 | Blight ↔ Gray Leaf Spot Errors |
|---|---:|---:|---:|---:|---:|
| V1 Custom CNN | 256 × 256 | 93.6306% | 92.32% | 93.69% | 28 |
| V2 Controlled Experiment | 320 × 320 | 89.01% | 86.83% | 89.16% | 47 |
| V3 Stage 1 | 320 × 320 | 92.1975% | 90.30% | 92.24% | — |
| **V3 Stage 2** | **320 × 320** | **94.4268%** | **92.97%** | **94.42%** | **23** |

V3 Stage 2 achieved the highest overall test accuracy and the strongest weighted F1 score.

It also produced the lowest number of combined Blight–Gray Leaf Spot errors among the models for which the boundary was evaluated.

---

# 15. Final Model Selection

**V3 MobileNetV2 Stage 2 was selected as the final model.**

The selection was based on the following evidence:

- Higher overall test accuracy:
  - V1: **93.6306%**
  - V3 Stage 2: **94.4268%**
- Improved Blight recall:
  - V1: **85.47%**
  - V3 Stage 2: **90.70%**
- Reduced Blight–Gray Leaf Spot boundary errors:
  - V1: **28**
  - V3 Stage 2: **23**
- Higher macro F1:
  - V1: **92.32%**
  - V3 Stage 2: **92.97%**
- Higher weighted F1:
  - V1: **93.69%**
  - V3 Stage 2: **94.42%**

Although Gray Leaf Spot recall decreased compared with V1, the overall improvement and reduction in the primary confusion boundary made V3 Stage 2 the stronger final model.
The selected model is:

```text
training_output/v3/best_maize_disease_mobilenetv2_v3_finetuned.keras
```

---

# 16. Knowledge Base

The project includes a structured knowledge base that provides disease-specific information after the image classifier produces a prediction.

The knowledge base is designed to keep **image classification** separate from **disease information retrieval**.

Each supported disease profile provides information that can be used by the diagnostic and chatbot components.

The knowledge base supports information such as:

- Disease description
- Symptoms
- Transmission
- Conditions that favour disease development
- Pathogens or causal agents
- Management information
- Sources and references
- Disease profile information

The knowledge base currently supports the maize diseases used by the classifier and additional disease information used for backend and chatbot validation.

The knowledge-base layer does not replace the image classifier. Instead, it provides contextual information based on the disease returned by the prediction layer.

---

# 17. CNN → Knowledge Base Integration

The project separates image classification from knowledge retrieval.

The overall diagnostic flow is:

```text
User Image
    ↓
Image Preprocessing
    ↓
V3 MobileNetV2 Classifier
    ↓
Predicted Disease + Confidence
    ↓
Confidence Decision Layer
    ↓
Accepted / Uncertain
    ↓
Knowledge Base Lookup
    ↓
Disease Information
    ↓
Diagnostic Response
```
````markdown
---

# 18. Confidence-Based Diagnostic Safety

The diagnostic layer uses prediction confidence to determine whether a model prediction should be presented as an accepted result or treated as uncertain.

The selected confidence threshold is:

```text
70%
```
Predictions with confidence of **70% or higher** are accepted by the diagnostic decision layer.

Predictions below the threshold are classified as **uncertain** and should not be presented as confirmed diagnoses.

The system also applies an additional caution flag to the known high-confusion disease pair:

- **Blight**
- **Gray Leaf Spot**

The caution mechanism does not change the model prediction. It provides additional context that these two diseases remain a known confusion boundary in the evaluated model.

The diagnostic layer therefore distinguishes between:

- Model prediction
- Prediction confidence
- Accepted prediction
- Uncertain prediction
- Known confusion-boundary caution

This provides a safer interface between model predictions and the information returned to the user.

---


# 21. Main Project Components

The repository contains the following major components.

## Machine Learning

- `cnn/`
  - Active V3 prediction and model-inference components
  - Database integration
  - Historical CNN testing utilities
- `cnn_model.py`
  - V1 custom CNN architecture
- `train_cnn.py`
  - Historical V1 training workflow
- `preprocessing_pipeline.py`
  - Historical V1 preprocessing and dataset preparation workflow

## Knowledge Base

- `knowledge_base/`
  - Disease profiles
  - Knowledge retrieval
  - Chatbot functionality
  - Knowledge-base validation

## Diagnostic Backend

- `diagnose.py`
  - Connects prediction, confidence decisions, and knowledge-base information
- `cnn/predictor.py`
  - Active V3 MobileNetV2 prediction layer
- `cnn/database_integration.py`
  - Connects predictions with the knowledge base

## Data and Analysis

- `data/`
  - Dataset-related utilities and supporting data resources
- `analysis/`
  - Analysis and evaluation artifacts
- `notebooks/`
  - Reproducible project analysis notebooks

## Documentation

- `README.md`
  - Project documentation and current validated results
- `LICENSE`
  - Project license information

Historical scripts and artifacts are retained where they provide useful evidence of the development and validation process.

---

# 22. Important Project Outputs

The main project outputs include:

### Final model

```text
training_output/v3/best_maize_disease_mobilenetv2_v3_finetuned.keras


#### B. Insert Section 23 and Section 24

Then, **before `# 25. Current Validation Status`**, insert:

````markdown
---

# 23. Repository and Data Policy

The Git repository contains the source code, analysis notebooks, documentation, evaluation evidence, and supporting project files required to understand and reproduce the project workflow.

The authoritative dataset is maintained separately from the Git source repository.

The trained V3 MobileNetV2 model is also maintained separately because the `.keras` model artifact is intentionally excluded from Git.

The repository therefore does not treat the large trained model file or the full dataset as ordinary Git-tracked source files.

The `.gitignore` configuration explicitly excludes the V3 trained model artifact:

```text
training_output/v3/*.keras

# 25. Current Validation Status

The current project state has been validated across the major components.

## Dataset

Total cleaned images: **4,184**

- Training: 2,928
- Validation: 628
- Test: 628

## Model Performance

| Model | Test Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|
| V1 Custom CNN | 93.6306% | 92.32% | 93.69% |
| V2 Controlled Experiment | 89.01% | 86.83% | 89.16% |
| V3 Stage 1 | 92.1975% | 90.30% | 92.24% |
| **V3 Stage 2** | **94.4268%** | **92.97%** | **94.42%** |

## Final V3 Stage 2

- Correct predictions: **593 / 628**
- Incorrect predictions: **35 / 628**
- Macro F1: **92.97%**
- Weighted F1: **94.42%**
- Blight ↔ Gray Leaf Spot errors: **23**

## Backend

| Test | Result |
|---|---|
| Predictor decision-layer tests | **3/3 PASS** |
| Database integration decision tests | **6/6 PASS** |
| Missing knowledge-base profile test | **PASS** |
| End-to-end diagnosis tests | **4/4 PASS** |

The end-to-end diagnosis tests covered:

- Blight
- Common Rust
- Gray Leaf Spot
- Healthy

## Knowledge-Base and Chatbot

The knowledge-base and chatbot components were also validated.

- Chatbot regression tests: **31/31 PASS**
- Unsupported-disease safety testing: **PASS**

The chatbot validation covered disease-specific information for:

- Maize Lethal Necrosis
- Common Rust
- Gray Leaf Spot
- Blight
- Tea Blister Blight
- Coffee Berry Disease
- Potato Bacterial Wilt

Unsupported disease examples were also tested, including:

- Banana Black Sigatoka
- Wheat Stripe Rust
- Rice Blast
- Cassava Mosaic
- Mango Powdery Mildew

These tests verified that the system does not incorrectly fabricate knowledge-base profiles for unsupported diseases.

---

# 26. Reproducibility

The project is organized so that the major analysis and validation steps can be reproduced.

The master analysis notebook is:

```text
notebooks/Corn_Pathology_AI_Analysis.ipynb

The notebook follows the **CRISP-DM** structure and documents:

1. Business Understanding
2. Data Understanding
3. Data Preparation
4. Modeling
5. Evaluation
6. Deployment Readiness
7. Final Conclusions

The authoritative dataset is stored separately from the Git source repository.

The trained V3 model is also preserved separately because the large `.keras` artifact is intentionally excluded from Git.

The active backend references the selected V3 model through:

```text
training_output/v3/best_maize_disease_mobilenetv2_v3_finetuned.keras

# 27. Project Directory

The main project structure is organized as follows:

```text
corn_pathology_ai-main/
│
├── cnn/
│   ├── predictor.py
│   ├── predictor_v1_backup.py
│   ├── mapping.py
│   ├── database_integration.py
│   ├── cnn_model.py
│   └── test_prediction.py
│
├── knowledge_base/
│   ├── chatbot.py
│   ├── database.py
│   └── ...
│
├── data/
│   ├── dataset_split/
│   │   ├── train/
│   │   ├── validation/
│   │   └── test/
│   ├── quarantine/
│   │   └── conflicting_duplicates/
│   └── ...
│
├── notebooks/
│   └── Corn_Pathology_AI_Analysis.ipynb
│
├── training_output/
│   ├── v3/
│   │   └── best_maize_disease_mobilenetv2_v3_finetuned.keras
│   └── ...
│
├── evaluation/
│   └── ...
│
├── scripts/
│   └── ...
│
├── diagnose.py
├── README.md
├── LICENSE
└── .gitignore
```

Some directories contain additional historical, evaluation, or supporting files that are not shown in the simplified structure above.

The authoritative trained V3 model is stored under:

```text
training_output/v3/
```

The V3 `.keras` model is intentionally excluded from Git through `.gitignore`.

The dataset is maintained separately from the Git source repository and is accessed by the analysis notebook through the configured project paths.

# 28. Limitations

The current system has several limitations that should be considered when interpreting its results.

1. **Dataset scope**  
   The model was developed and evaluated using the available Corn Pathology dataset and the four supported disease classes. Performance may differ on images from other datasets, geographical regions, maize varieties, or field conditions.

2. **Image quality and variation**  
   Real-world images may contain differences in lighting, background, image quality, leaf orientation, occlusion, or disease severity that are not fully represented in the evaluation dataset.

3. **Disease-class coverage**  
   The current classifier recognizes only:
   - Blight
   - Common Rust
   - Gray Leaf Spot
   - Healthy

   Images representing diseases outside these classes should not be interpreted as one of the supported classes.

4. **Blight and Gray Leaf Spot confusion**  
   Blight and Gray Leaf Spot remain the primary confusion boundary in the evaluated model. Although V3 reduced their combined errors compared with V1, some misclassification remains.

5. **Confidence is not certainty**  
   The confidence score represents the model's prediction confidence and should not be interpreted as a guaranteed diagnosis.

6. **Uncertain predictions**  
   Predictions below the configured 70% confidence threshold are treated as uncertain rather than being presented as accepted diagnoses.

7. **Knowledge-base coverage**  
   The knowledge base provides information for the supported disease and crop profiles, but it is not a substitute for expert agricultural diagnosis or laboratory confirmation.

8. **No field validation yet**  
   The current evaluation is based on the available held-out test dataset. Further validation using independently collected real-world field images would be required before making claims about broad field deployment.

9. **Model and dataset dependency**  
   Reproducing the reported results requires maintaining the same dataset split, preprocessing configuration, model configuration, and evaluation procedure.

10. **Deployment scope**  
    The current project demonstrates deployment readiness and an integrated backend pipeline. It should not be interpreted as a fully production-hardened agricultural diagnostic service.

    # 29. Future Work

The following improvements can extend the current project beyond the validated prototype.

1. **Expand the disease dataset**  
   Add more maize diseases and substantially increase the number and diversity of images available for each class.

2. **Collect real-world field images**  
   Evaluate the selected V3 model on independently collected field images containing natural variations in lighting, backgrounds, disease severity, and leaf orientation.

3. **Improve the Blight–Gray Leaf Spot boundary**  
   Investigate additional data, targeted augmentation, fine-tuning strategies, and alternative architectures to further reduce confusion between these two classes.

4. **Explore additional model architectures**  
   Compare MobileNetV2 with other suitable transfer-learning architectures to determine whether further improvements in accuracy, robustness, or efficiency are possible.

5. **Improve uncertainty handling**  
   Investigate calibration and additional uncertainty techniques so that confidence scores better reflect the reliability of individual predictions.

6. **Expand the knowledge base**  
   Add more disease profiles, symptoms, transmission information, environmental conditions, management practices, and authoritative agricultural sources.

7. **Strengthen expert validation**  
   Incorporate agricultural expert review and, where possible, laboratory-confirmed diagnoses to evaluate the reliability of the system's recommendations.

8. **Develop a production interface**  
   Build a user-facing application that allows users to upload maize leaf images, receive model predictions, and access relevant knowledge-base information.

9. **Deployment optimization**  
   Investigate model optimization techniques such as quantization or other lightweight deployment approaches for mobile and resource-constrained environments.

10. **Continuous evaluation and monitoring**  
    Establish a process for monitoring model performance after deployment and periodically updating the dataset, model, and knowledge base as new evidence becomes available.

    # 30. Conclusion

The PLANT HEALTH MAIZE PROJECT developed and validated an end-to-end maize disease diagnosis pipeline using image classification and a structured agricultural knowledge base.

The project began with a cleaned dataset of 4,184 maize leaf images across four classes: Blight, Common Rust, Gray Leaf Spot, and Healthy. The data was stratified into training, validation, and test sets to support controlled model development and evaluation.

A custom CNN was established as the V1 baseline. A controlled V2 experiment was then evaluated but rejected because its performance was lower than the V1 baseline.

The V3 MobileNetV2 transfer-learning model was subsequently developed through two stages. Stage 1 used a frozen pretrained backbone, while Stage 2 applied controlled fine-tuning. V3 Stage 2 achieved the strongest overall performance, reaching 94.43% test accuracy and a macro F1-score of 92.97%.

V3 also improved Blight recall and reduced the combined Blight–Gray Leaf Spot confusion boundary compared with the V1 baseline. For these reasons, V3 Stage 2 was selected as the final model.

The selected model was integrated with the backend prediction layer, disease mapping, knowledge base, and diagnostic logic. A 70% confidence threshold was incorporated so that lower-confidence predictions are handled as uncertain rather than being presented as accepted diagnoses.

The completed regression testing demonstrated that the core prediction, database integration, diagnostic, knowledge-base, chatbot, and safety components operate together as intended.

The project therefore provides a validated prototype for image-based maize disease classification and knowledge-supported diagnosis, while clearly identifying the limitations and additional field validation required before production-scale agricultural deployment.

# 31. License

This project is licensed under the MIT License.

See the `LICENSE` file in the repository for the complete license terms.