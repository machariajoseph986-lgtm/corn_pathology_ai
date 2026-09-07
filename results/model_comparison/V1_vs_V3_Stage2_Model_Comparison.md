# V1 vs V3 Stage 2 Model Comparison

## Purpose

This document records the evidence used to select the final model for the Plant Health Maize Project.

V1 is the established custom CNN baseline. V3 Stage 2 is the fine-tuned MobileNetV2 transfer-learning model.

The purpose of this comparison is to determine which model provides the stronger overall solution while paying particular attention to the known Blight ↔ Gray Leaf Spot confusion boundary.

## Fair Comparison Basis

Both models were evaluated on the same audited stratified test set of 628 images:

- Blight: 172
- Common_Rust: 196
- Gray_Leaf_Spot: 86
- Healthy: 174

Using the same held-out test set makes the comparison directly interpretable.

## Model Comparison

| Metric | V1 | V3 Stage 2 | Change (V3 vs V1) |
|---|---:|---:|---:|
| Test accuracy (%) | 93.6306 | 94.4268 | +0.7962 percentage points |
| Correct test predictions | 588 | 593 | +5 |
| Incorrect test predictions | 40 | 35 | -5 |
| Macro F1 (%) | 92.32 | 92.97 | +0.65 percentage points |
| Weighted F1 (%) | 93.69 | 94.42 | +0.73 percentage points |
| Blight precision (%) | 91.87 | 91.76 | -0.11 percentage points |
| Blight recall (%) | 85.47 | 90.70 | +5.23 percentage points |
| Blight F1 (%) | 88.55 | 91.23 | +2.68 percentage points |
| Gray Leaf Spot precision (%) | 78.00 | 83.72 | +5.72 percentage points |
| Gray Leaf Spot recall (%) | 90.70 | 83.72 | -6.98 percentage points |
| Gray Leaf Spot F1 (%) | 83.87 | 83.72 | -0.15 percentage points |
| Blight → Gray Leaf Spot errors | 20 | 13 | -7 |
| Gray Leaf Spot → Blight errors | 8 | 10 | +2 |
| Combined Blight ↔ Gray Leaf Spot errors | 28 | 23 | -5 (17.9% reduction) |

## Primary Evidence for Selecting V3

V3 Stage 2 was selected over V1 for three main reasons.

### 1. Higher Overall Test Accuracy

V3 Stage 2 achieved:

- V1: 93.6306%
- V3 Stage 2: 94.4268%

This is an improvement of 0.7962 percentage points.

V3 also produced 593 correct predictions compared with 588 for V1.

### 2. Improved Blight Recall

Blight recall improved from:

- V1: 85.47%
- V3 Stage 2: 90.70%

This is an improvement of 5.23 percentage points.

This was important because Blight was one of the two classes involved in the project's primary confusion boundary.

### 3. Reduced Blight ↔ Gray Leaf Spot Confusion

The combined number of errors between Blight and Gray Leaf Spot decreased from:

- V1: 28 errors
- V3 Stage 2: 23 errors

This represents 5 fewer boundary errors, or a 17.9% reduction.

The directional errors changed as follows:

- Blight → Gray Leaf Spot: 20 → 13
- Gray Leaf Spot → Blight: 8 → 10

Therefore, V3 substantially reduced the number of Blight cases being classified as Gray Leaf Spot, although the reverse direction increased slightly.

## Important Trade-Off

V3 should not be described as better on every individual metric.

Gray Leaf Spot recall decreased from 90.70% with V1 to 83.72% with V3 Stage 2.

At the same time, Gray Leaf Spot precision improved from 78.00% to 83.72%, and its F1 score remained approximately stable:

- V1 F1: 83.87%
- V3 Stage 2 F1: 83.72%

This indicates that V3 shifted the decision boundary between Blight and Gray Leaf Spot rather than eliminating the underlying difficulty.

## Final Model Selection Decision

**V3 MobileNetV2 Stage 2 was selected over V1 because it achieved higher overall test accuracy (94.43% vs. 93.63%), improved Blight recall (90.70% vs. 85.47%), and reduced combined Blight–Gray Leaf Spot boundary errors from 28 to 23. Although Gray Leaf Spot recall decreased, the overall improvement and reduction in the primary confusion boundary made V3 Stage 2 the stronger final model.**

## Why V1 Was Retained

V1 remains part of the project as the baseline model and historical reference.

It should not be deleted or overwritten because it provides:

- the original custom CNN baseline;
- evidence for model comparison;
- reproducibility of the development process;
- a reference point for future improvements.

## Why V2 Was Not Selected

V2 was evaluated as an intermediate experiment using a 320×320 input and controlled augmentation.

Its test accuracy was 89.01%, compared with 93.63% for V1.

Its combined Blight ↔ Gray Leaf Spot errors also increased from 28 to 47.

Therefore, V2 was rejected and V1 was retained until V3 Stage 2 produced the strongest overall result.

## Final Selected Model

**Final model: V3 MobileNetV2 Stage 2**

Final test performance:

- Test accuracy: 94.4268%
- Correct predictions: 593 / 628
- Incorrect predictions: 35 / 628
- Macro F1: 92.97%
- Weighted F1: 94.42%
- Combined Blight ↔ Gray Leaf Spot errors: 23

## Reproducibility Note

The model comparison is based on the same audited test set used for the project's final evaluation.

V1 and V2 artifacts are retained as historical experiments. The active diagnosis backend has been updated to use the V3 MobileNetV2 Stage 2 model.

The V3 backend subsequently passed the predictor decision-layer, database integration, missing-profile, and end-to-end diagnosis regression tests.

## Relationship to the Master Notebook

The master notebook:

`notebooks/Corn_Pathology_AI_Analysis.ipynb`

contains the complete chronological CRISP-DM analysis.

This document provides a focused model-selection record that can be used independently during project presentations, group discussions, and technical review.
