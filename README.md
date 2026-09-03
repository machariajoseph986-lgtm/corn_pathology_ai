# Plant Health Maize Project

## Corn Pathology AI

A machine-learning project for image-based diagnosis of maize leaf diseases, with a knowledge-base layer for returning disease information after classification.

The project currently focuses on a validated CNN-based maize disease classification pipeline and its integration with a structured plant-health knowledge base.

---

## 1. Project Objectives

The project is designed around two main questions:

1. **Can we reliably diagnose plant diseases from images?**
2. **Can we provide useful and trustworthy information based on that diagnosis?**

The current implementation addresses these questions through:

* image dataset preparation and quality control
* stratified training, validation, and test splitting
* CNN image classification
* class-imbalance handling
* model evaluation
* confidence-based decision analysis
* visual misclassification analysis
* disease-to-knowledge-base mapping
* user-facing diagnosis through a command-line interface

---

## 2. Current Maize Disease Classes

The maize image classifier uses four classes:

* `Blight`
* `Common_Rust`
* `Gray_Leaf_Spot`
* `Healthy`

The project preserves the dataset's original class terminology. The `Blight` label is therefore not silently renamed elsewhere in the pipeline.

---

## 3. Dataset

The cleaned maize dataset contains:

**4,184 images**

After cleaning, the class distribution is:

| Class          |    Images |
| -------------- | --------: |
| Blight         |     1,144 |
| Common_Rust    |     1,306 |
| Gray_Leaf_Spot |       572 |
| Healthy        |     1,162 |
| **Total**      | **4,184** |

Four conflicting duplicate images were quarantined during dataset cleaning rather than being silently discarded.

The raw dataset is intentionally excluded from Git because of its size. It remains part of the local project and is intended to be preserved through the project's Google Drive copy.

---

## 4. Dataset Split

A stratified split was performed to preserve class proportions across the three datasets:

| Dataset    |    Images |
| ---------- | --------: |
| Training   |     2,928 |
| Validation |       628 |
| Test       |       628 |
| **Total**  | **4,184** |

Training distribution:

| Class          | Training Images |
| -------------- | --------------: |
| Blight         |             801 |
| Common_Rust    |             914 |
| Gray_Leaf_Spot |             400 |
| Healthy        |             813 |

---

## 5. V1 CNN Model

The validated V1 model uses:

* input size: `256 × 256`
* RGB images
* pixel normalization using `1/255`
* training-only image augmentation
* class weighting to address class imbalance
* custom CNN architecture
* four disease/health output classes

The best V1 model is saved locally as:

`training_output/best_maize_disease_cnn.keras`

The final V1 model is saved as:

`training_output/final_maize_disease_cnn.keras`

Model files are excluded from Git because they are generated binary artifacts.

---

## 6. V1 Evaluation

The current V1 test evaluation contains:

* **628 test images**
* **93.63% test accuracy**
* **588 correct predictions**
* **40 incorrect predictions**
* **Macro F1: 0.9232**
* **Weighted F1: 0.9369**

The strongest class performance is observed for `Healthy` and `Common_Rust`.

The principal weakness is the decision boundary between:

* `Blight`
* `Gray_Leaf_Spot`

This boundary was therefore subjected to additional error and visual analysis.

Evaluation outputs are stored under:

`results/`

including:

* classification report
* confusion matrix
* evaluation summaries
* misclassification reports
* confidence analysis
* visual error analysis

---

## 7. Confidence Analysis

A confidence analysis was performed to investigate whether uncertain predictions could be separated from reasonably confident predictions.

The current V1 decision threshold is:

**70% confidence**

At this threshold:

* accepted predictions: **556**
* uncertain predictions: **72**
* accepted accuracy: **97.30%**
* coverage: **88.54%**

The threshold is treated as a decision policy rather than a guarantee of correctness.

The diagnostic system therefore uses language such as **"reasonably confident"** rather than presenting model confidence as certainty.

---

## 8. V2 Controlled Experiment

A controlled V2 experiment was also conducted using:

* `320 × 320` image input
* moderate augmentation

V1 remains preserved as the baseline and is not overwritten.

V2 artifacts are stored under:

`training_output/v2/`

The V2 experiment is intended to be compared against V1 before any decision is made about adopting it.

---

## 9. Knowledge Base

The project contains a SQLite knowledge base:

`knowledge_base/plant_health.db`

The knowledge-base layer currently contains disease information for:

* Maize — Maize Lethal Necrosis
* Tea — Blister Blight
* Coffee — Coffee Berry Disease
* Potato — Bacterial Wilt

The database contains structured information such as:

* disease name
* pathogen
* symptoms
* transmission
* favorable conditions
* management information
* sources

The CNN maize classifications are mapped to knowledge-base identifiers through:

`cnn/mapping.py`

---

## 10. CNN → Knowledge Base Integration

The integration pipeline is:

```text
User Image
    ↓
CNN Predictor
    ↓
Predicted Class
    ↓
Confidence Decision
    ↓
Disease Mapping
    ↓
Knowledge Base
    ↓
Disease Information
    ↓
Diagnosis Output
```

The main integration components are:

* `cnn/predictor.py`
* `cnn/mapping.py`
* `cnn/database_integration.py`
* `knowledge_base/database.py`
* `knowledge_base/chatbot.py`
* `diagnose.py`

Healthy predictions do not require a disease profile.

Disease predictions are mapped to the appropriate knowledge-base profile.

---

## 11. Main Project Components

### Dataset and preprocessing

* `inspect_dataset.py`
* `clean_dataset.py`
* `data/clean_dataset.py`
* `split_dataset.py`
* `class_balance.py`
* `class_weights.py`
* `preprocessing_pipeline.py`

### Model training

* `train_cnn.py`
* `train_cnn_v2.py`
* `cnn_model.py`

### Model evaluation

* `evaluate_model.py`
* `evaluate_v1_test.py`
* `analyze_confidence.py`
* `analyze_confidence_v1.py`
* `analyze_threshold_v1.py`
* `analyze_class_thresholds_v1.py`

### Error and visual analysis

* `inspect_misclassifications.py`
* `inspect_confused_images.py`
* `analyze_blight_gray_errors_v1.py`
* `analyze_blight_gray_visuals.py`
* `review_blight_gray_boundary.py`
* `analyze_blight_gray_severity_errors.py`

### CNN and knowledge-base integration

* `cnn/predictor.py`
* `cnn/mapping.py`
* `cnn/database_integration.py`
* `knowledge_base/database.py`
* `knowledge_base/chatbot.py`
* `diagnose.py`

### Testing

The repository also contains tests for:

* prediction decisions
* database integration
* missing disease profiles
* end-to-end diagnosis

---

## 12. Important Project Outputs

### Training

```text
training_output/
├── best_maize_disease_cnn.keras
├── final_maize_disease_cnn.keras
├── training_history.json
└── v2/
    ├── best_maize_disease_cnn_v2.keras
    ├── final_maize_disease_cnn_v2.keras
    └── training_history_v2.json
```

### Evaluation

```text
results/
├── classification_report.txt
├── confusion_matrix.png
├── evaluation_summary.json
├── experiment_summary.json
├── confidence_analysis/
├── misclassifications/
└── visual_analysis/
```

---

## 13. Repository and Data Policy

Git is used to track the project's source code, configuration, documentation, evaluation summaries, knowledge-base files, and selected analysis artifacts.

Large/generated data is intentionally excluded from Git, including:

* raw dataset images
* dataset splits
* quarantine files
* trained `.keras` model binaries
* temporary files
* Python caches
* virtual environments

The raw dataset and generated model files are preserved separately as project assets.

---

## 14. Project Status

### Completed

* dataset inspection
* dataset cleaning
* duplicate/conflict handling
* stratified dataset splitting
* preprocessing
* augmentation
* class weighting
* V1 CNN training
* V1 evaluation
* confusion-matrix analysis
* confidence analysis
* Blight/Gray Leaf Spot error analysis
* controlled V2 experiment
* CNN prediction layer
* CNN-to-knowledge-base mapping
* SQLite knowledge base
* diagnosis integration
* end-to-end diagnosis testing

### Next stages

The next project stages are:

1. final local project cleanup
2. Git repository commit and remote setup
3. Google Drive project preservation
4. master Google Colab notebook
5. reproducibility and consolidated analysis
6. chatbot/application refinement
7. eventual deployment/interface development

The website/deployment stage is intentionally not treated as completed at this point.

---

## 15. Reproducibility

The project is being organized so that the complete workflow can be reproduced from the preserved project directory and the master Colab notebook.

The planned master notebook is:

`Corn_Pathology_AI_Analysis.ipynb`

The notebook will document the complete analytical workflow from project setup and dataset verification through model evaluation, confidence analysis, knowledge-base integration, and example diagnosis.

---

## 16. Project Directory

The main project directory is:

```text
corn_pathology_ai-main/
```

The intended Google Drive location is:

```text
My Drive/
└── Plant Health Maize Project/
    └── corn_pathology_ai-main/
```

The corresponding Colab project path will be:

```text
/content/drive/MyDrive/Plant Health Maize Project/corn_pathology_ai-main
```

---

## 17. License

See `LICENSE` for the project's license information.
