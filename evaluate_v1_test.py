"""
V1 CNN FINAL TEST-SET EVALUATION

Purpose:
    Evaluate the finalized V1 CNN on the untouched test dataset.

Important:
    The test set is NOT used for:
        - model training
        - threshold selection
        - model tuning

The 70% confidence threshold was selected using validation data.

This script evaluates:
    1. Overall CNN performance
    2. Confusion matrix
    3. Classification report
    4. Blight ↔ Gray Leaf Spot confusion
    5. Confidence behavior
    6. 70% decision-layer behavior
    7. High-confidence errors
"""

import os
import json

import numpy as np
import tensorflow as tf

from sklearn.metrics import (
    confusion_matrix,
    classification_report
)


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

TEST_DIR = os.path.join(
    PROJECT_DIR,
    "dataset_split",
    "test"
)

MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "training_output",
    "best_maize_disease_cnn.keras"
)

RESULTS_DIR = os.path.join(
    PROJECT_DIR,
    "results",
    "test_evaluation"
)

os.makedirs(
    RESULTS_DIR,
    exist_ok=True
)

IMAGE_SIZE = (256, 256)
BATCH_SIZE = 32

CONFIDENCE_THRESHOLD = 0.70

CLASS_NAMES = [
    "Blight",
    "Common_Rust",
    "Gray_Leaf_Spot",
    "Healthy"
]


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("V1 CNN FINAL TEST-SET EVALUATION")
print("=" * 70)

print("\nImportant:")
print(
    "The test set is being used only for final independent evaluation."
)

print(
    "\nModel:"
    f"\n  {MODEL_PATH}"
)

print(
    "\nTest dataset:"
    f"\n  {TEST_DIR}"
)

print(
    "\nDecision threshold:"
    f"\n  {CONFIDENCE_THRESHOLD * 100:.0f}%"
)


# ============================================================
# VERIFY PATHS
# ============================================================

if not os.path.exists(MODEL_PATH):

    raise FileNotFoundError(
        f"\nModel not found:\n{MODEL_PATH}"
    )

if not os.path.exists(TEST_DIR):

    raise FileNotFoundError(
        f"\nTest dataset not found:\n{TEST_DIR}"
    )


# ============================================================
# LOAD TEST DATASET
# ============================================================

print("\n" + "-" * 70)
print("LOADING TEST DATASET")
print("-" * 70)

test_dataset = tf.keras.utils.image_dataset_from_directory(

    TEST_DIR,

    image_size=IMAGE_SIZE,

    batch_size=BATCH_SIZE,

    shuffle=False
)

print(
    f"\nImages found: "
    f"{len(test_dataset.file_paths)}"
)

print("\nClasses:")

for index, class_name in enumerate(
    test_dataset.class_names
):

    print(
        f"  {index}: {class_name}"
    )


# ============================================================
# PREPROCESSING
# ============================================================

test_dataset = test_dataset.map(

    lambda images, labels: (
        tf.cast(images, tf.float32) / 255.0,
        labels
    ),

    num_parallel_calls=tf.data.AUTOTUNE
)

test_dataset = test_dataset.prefetch(
    tf.data.AUTOTUNE
)


# ============================================================
# LOAD MODEL
# ============================================================

print("\n" + "-" * 70)
print("LOADING V1 CNN MODEL")
print("-" * 70)

model = tf.keras.models.load_model(
    MODEL_PATH
)

print(
    "\nV1 model loaded successfully."
)


# ============================================================
# GENERATE PREDICTIONS
# ============================================================

print("\n" + "-" * 70)
print("GENERATING TEST PREDICTIONS")
print("-" * 70)

probabilities = model.predict(
    test_dataset,
    verbose=1
)

predicted_classes = np.argmax(
    probabilities,
    axis=1
)

confidence = np.max(
    probabilities,
    axis=1
)

true_classes = np.concatenate(
    [
        labels.numpy()
        for _, labels in test_dataset
    ]
)


# ============================================================
# OVERALL PERFORMANCE
# ============================================================

correct = (
    predicted_classes
    == true_classes
)

total_images = len(
    true_classes
)

correct_count = int(
    np.sum(correct)
)

incorrect_count = (
    total_images
    - correct_count
)

accuracy = (
    correct_count
    / total_images
)


print("\n" + "=" * 70)
print("1. OVERALL TEST PERFORMANCE")
print("=" * 70)

print(
    f"\nImages analyzed : {total_images}"
)

print(
    f"Correct         : {correct_count}"
)

print(
    f"Incorrect       : {incorrect_count}"
)

print(
    f"Accuracy        : {accuracy * 100:.2f}%"
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    true_classes,
    predicted_classes
)


print("\n" + "=" * 70)
print("2. V1 TEST CONFUSION MATRIX")
print("=" * 70)

print("\nRows = Actual")
print("Columns = Predicted\n")

print(
    f"{'':20}"
    f"{CLASS_NAMES[0]:18}"
    f"{CLASS_NAMES[1]:18}"
    f"{CLASS_NAMES[2]:18}"
    f"{CLASS_NAMES[3]:18}"
)

for index, class_name in enumerate(
    CLASS_NAMES
):

    print(
        f"{class_name:20}"
        f"{cm[index, 0]:18}"
        f"{cm[index, 1]:18}"
        f"{cm[index, 2]:18}"
        f"{cm[index, 3]:18}"
    )


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

report = classification_report(

    true_classes,

    predicted_classes,

    target_names=CLASS_NAMES,

    digits=4
)


print("\n" + "=" * 70)
print("3. V1 TEST CLASSIFICATION REPORT")
print("=" * 70)

print()
print(report)


# ============================================================
# BLIGHT ↔ GRAY LEAF SPOT
# ============================================================

blight_to_gray = int(
    cm[0, 2]
)

gray_to_blight = int(
    cm[2, 0]
)

total_pair_confusion = (
    blight_to_gray
    + gray_to_blight
)


print("\n" + "=" * 70)
print("4. BLIGHT ↔ GRAY LEAF SPOT")
print("=" * 70)

print(
    f"\nBlight → Gray Leaf Spot : "
    f"{blight_to_gray}"
)

print(
    f"Gray Leaf Spot → Blight : "
    f"{gray_to_blight}"
)

print(
    f"Total two-way confusion : "
    f"{total_pair_confusion}"
)


# ============================================================
# CONFIDENCE ANALYSIS
# ============================================================

correct_confidence = confidence[
    correct
]

incorrect_confidence = confidence[
    ~correct
]


print("\n" + "=" * 70)
print("5. CONFIDENCE ANALYSIS")
print("=" * 70)

if len(correct_confidence) > 0:

    print("\nCorrect predictions:")

    print(
        f"  Minimum : "
        f"{np.min(correct_confidence) * 100:.2f}%"
    )

    print(
        f"  Average : "
        f"{np.mean(correct_confidence) * 100:.2f}%"
    )

    print(
        f"  Maximum : "
        f"{np.max(correct_confidence) * 100:.2f}%"
    )


if len(incorrect_confidence) > 0:

    print("\nIncorrect predictions:")

    print(
        f"  Minimum : "
        f"{np.min(incorrect_confidence) * 100:.2f}%"
    )

    print(
        f"  Average : "
        f"{np.mean(incorrect_confidence) * 100:.2f}%"
    )

    print(
        f"  Maximum : "
        f"{np.max(incorrect_confidence) * 100:.2f}%"
    )


# ============================================================
# 70% DECISION-LAYER ANALYSIS
# ============================================================

accepted = (
    confidence >= CONFIDENCE_THRESHOLD
)

rejected = ~accepted

accepted_correct = np.sum(
    accepted & correct
)

accepted_wrong = np.sum(
    accepted & ~correct
)

rejected_correct = np.sum(
    rejected & correct
)

rejected_wrong = np.sum(
    rejected & ~correct
)

accepted_count = np.sum(
    accepted
)

rejected_count = np.sum(
    rejected
)


print("\n" + "=" * 70)
print("6. 70% DECISION-LAYER ANALYSIS")
print("=" * 70)

print(
    f"\nThreshold : "
    f"{CONFIDENCE_THRESHOLD * 100:.0f}%"
)

print(
    f"\nAccepted : "
    f"{accepted_count}"
)

print(
    f"Rejected / Uncertain : "
    f"{rejected_count}"
)

print(
    f"\nAccepted and correct : "
    f"{accepted_correct}"
)

print(
    f"Accepted but wrong   : "
    f"{accepted_wrong}"
)

print(
    f"Correct but uncertain : "
    f"{rejected_correct}"
)

print(
    f"Wrong and uncertain   : "
    f"{rejected_wrong}"
)

if accepted_count > 0:

    accepted_accuracy = (
        accepted_correct
        / accepted_count
    )

    print(
        f"\nAccuracy among accepted predictions : "
        f"{accepted_accuracy * 100:.2f}%"
    )


# ============================================================
# HIGH-CONFIDENCE ERRORS
# ============================================================

high_confidence_errors = (
    (~correct)
    & (confidence >= CONFIDENCE_THRESHOLD)
)

high_confidence_error_count = int(
    np.sum(high_confidence_errors)
)


print("\n" + "=" * 70)
print("7. HIGH-CONFIDENCE ERRORS")
print("=" * 70)

print(
    f"\nIncorrect predictions with "
    f"≥70% confidence : "
    f"{high_confidence_error_count}"
)


if high_confidence_error_count > 0:

    print(
        "\nTop high-confidence errors:"
    )

    error_indices = np.where(
        high_confidence_errors
    )[0]

    sorted_indices = error_indices[
        np.argsort(
            confidence[error_indices]
        )[::-1]
    ]

    for index in sorted_indices[:10]:

        print(
            f"\n  Actual      : "
            f"{CLASS_NAMES[true_classes[index]]}"
        )

        print(
            f"  Predicted   : "
            f"{CLASS_NAMES[predicted_classes[index]]}"
        )

        print(
            f"  Confidence  : "
            f"{confidence[index] * 100:.2f}%"
        )


# ============================================================
# BLIGHT ↔ GRAY CONFIDENCE
# ============================================================

pair_errors = (

    (
        (true_classes == 0)
        & (predicted_classes == 2)
    )

    |

    (
        (true_classes == 2)
        & (predicted_classes == 0)
    )

)


pair_confidence = confidence[
    pair_errors
]


print("\n" + "=" * 70)
print("8. BLIGHT ↔ GRAY LEAF SPOT CONFIDENCE")
print("=" * 70)

print(
    f"\nTwo-way confusion cases : "
    f"{len(pair_confidence)}"
)

if len(pair_confidence) > 0:

    print(
        f"Minimum confidence : "
        f"{np.min(pair_confidence) * 100:.2f}%"
    )

    print(
        f"Average confidence : "
        f"{np.mean(pair_confidence) * 100:.2f}%"
    )

    print(
        f"Maximum confidence : "
        f"{np.max(pair_confidence) * 100:.2f}%"
    )

    pair_high_confidence = np.sum(
        pair_confidence
        >= CONFIDENCE_THRESHOLD
    )

    print(
        f"\nPair errors ≥70% confidence : "
        f"{pair_high_confidence}"
    )


# ============================================================
# SAVE SUMMARY
# ============================================================

summary = {

    "model": MODEL_PATH,

    "test_dataset": TEST_DIR,

    "total_images": int(
        total_images
    ),

    "correct": int(
        correct_count
    ),

    "incorrect": int(
        incorrect_count
    ),

    "accuracy": float(
        accuracy
    ),

    "confidence_threshold": float(
        CONFIDENCE_THRESHOLD
    ),

    "accepted_predictions": int(
        accepted_count
    ),

    "uncertain_predictions": int(
        rejected_count
    ),

    "accepted_correct": int(
        accepted_correct
    ),

    "accepted_wrong": int(
        accepted_wrong
    ),

    "uncertain_correct": int(
        rejected_correct
    ),

    "uncertain_wrong": int(
        rejected_wrong
    ),

    "blight_to_gray_leaf_spot": int(
        blight_to_gray
    ),

    "gray_leaf_spot_to_blight": int(
        gray_to_blight
    ),

    "total_blight_gray_confusion": int(
        total_pair_confusion
    ),

    "high_confidence_errors": int(
        high_confidence_error_count
    ),

    "classification_report": report
}


summary_path = os.path.join(
    RESULTS_DIR,
    "v1_test_evaluation_summary.json"
)


with open(
    summary_path,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        summary,
        file,
        indent=4
    )


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 70)
print("V1 FINAL TEST EVALUATION COMPLETE")
print("=" * 70)

print(
    f"\nSummary saved to:"
    f"\n  {summary_path}"
)

print(
    "\nThe test set has now been evaluated "
    "without changing the V1 model or the "
    "70% threshold."
)

print("\nNext step:")
print(
    "Interpret the final test-set evidence "
    "before moving to the next project phase."
)