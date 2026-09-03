import os
import numpy as np
import tensorflow as tf
from sklearn.metrics import accuracy_score


# ============================================================
# V1 CONFIDENCE THRESHOLD ANALYSIS
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

CLASS_NAMES = [
    "Blight",
    "Common_Rust",
    "Gray_Leaf_Spot",
    "Healthy"
]

IMAGE_SIZE = (256, 256)
BATCH_SIZE = 32


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("V1 CNN CONFIDENCE THRESHOLD ANALYSIS")
print("=" * 70)

print("\nModel:")
print(f"  {MODEL_PATH}")

print("\nTest dataset:")
print(f"  {TEST_DIR}")


# ============================================================
# LOAD TEST DATA
# ============================================================

test_ds = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    labels="inferred",
    label_mode="int",
    class_names=CLASS_NAMES,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

normalization = tf.keras.layers.Rescaling(
    1.0 / 255
)

test_ds = test_ds.map(
    lambda images, labels: (
        normalization(images),
        labels
    ),
    num_parallel_calls=tf.data.AUTOTUNE
)

test_ds = test_ds.prefetch(
    tf.data.AUTOTUNE
)


# ============================================================
# LOAD MODEL
# ============================================================

print("\nLoading V1 model...")

model = tf.keras.models.load_model(
    MODEL_PATH
)

print("Model loaded successfully.")


# ============================================================
# GENERATE PREDICTIONS
# ============================================================

print("\nGenerating predictions...")

predictions = model.predict(
    test_ds,
    verbose=1
)

y_true = np.concatenate(
    [
        labels.numpy()
        for _, labels in test_ds
    ],
    axis=0
)

y_pred = np.argmax(
    predictions,
    axis=1
)

confidence = np.max(
    predictions,
    axis=1
)

correct = (
    y_pred == y_true
)


# ============================================================
# BASIC CHECK
# ============================================================

print("\nPrediction summary:")
print(f"  Test images       : {len(y_true)}")
print(f"  Correct           : {np.sum(correct)}")
print(f"  Incorrect         : {np.sum(~correct)}")
print(
    f"  Overall accuracy  : "
    f"{accuracy_score(y_true, y_pred):.4%}"
)


# ============================================================
# THRESHOLD ANALYSIS
# ============================================================

thresholds = [
    0.50,
    0.60,
    0.70,
    0.75,
    0.80,
    0.85,
    0.90,
    0.95
]

print("\n" + "=" * 70)
print("CONFIDENCE THRESHOLD RESULTS")
print("=" * 70)

print(
    f"\n{'Threshold':<12}"
    f"{'Accepted':<12}"
    f"{'Correct':<12}"
    f"{'Incorrect':<12}"
    f"{'Coverage':<12}"
    f"{'Accuracy':<12}"
)

print("-" * 70)


for threshold in thresholds:

    accepted = confidence >= threshold

    accepted_count = np.sum(
        accepted
    )

    correct_count = np.sum(
        correct & accepted
    )

    incorrect_count = np.sum(
        (~correct) & accepted
    )

    coverage = (
        accepted_count / len(y_true)
    )

    if accepted_count > 0:

        threshold_accuracy = (
            correct_count /
            accepted_count
        )

    else:

        threshold_accuracy = 0.0

    print(
        f"{threshold:<12.0%}"
        f"{accepted_count:<12}"
        f"{correct_count:<12}"
        f"{incorrect_count:<12}"
        f"{coverage:<12.2%}"
        f"{threshold_accuracy:<12.2%}"
    )


# ============================================================
# CURRENT 70% POLICY
# ============================================================

threshold = 0.70

accepted = confidence >= threshold

accepted_count = np.sum(
    accepted
)

correct_count = np.sum(
    correct & accepted
)

incorrect_count = np.sum(
    (~correct) & accepted
)

uncertain_count = np.sum(
    ~accepted
)

print("\n" + "=" * 70)
print("CURRENT 70% POLICY")
print("=" * 70)

print(
    f"\nAccepted predictions : "
    f"{accepted_count}"
)

print(
    f"Uncertain predictions: "
    f"{uncertain_count}"
)

print(
    f"Accepted correct     : "
    f"{correct_count}"
)

print(
    f"Accepted incorrect   : "
    f"{incorrect_count}"
)

if accepted_count > 0:

    print(
        f"Accuracy when accepted: "
        f"{correct_count / accepted_count:.2%}"
    )

print(
    f"Coverage: "
    f"{accepted_count / len(y_true):.2%}"
)


# ============================================================
# CLASS-SPECIFIC ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("CLASS-SPECIFIC 70% ANALYSIS")
print("=" * 70)

for class_index, class_name in enumerate(
    CLASS_NAMES
):

    class_mask = (
        y_true == class_index
    )

    class_count = np.sum(
        class_mask
    )

    class_accepted = (
        class_mask & accepted
    )

    class_correct = (
        class_mask &
        accepted &
        correct
    )

    accepted_count = np.sum(
        class_accepted
    )

    correct_count = np.sum(
        class_correct
    )

    if accepted_count > 0:

        accepted_accuracy = (
            correct_count /
            accepted_count
        )

    else:

        accepted_accuracy = 0.0

    print(
        f"\n{class_name}"
    )

    print(
        f"  Total images       : "
        f"{class_count}"
    )

    print(
        f"  Accepted           : "
        f"{accepted_count}"
    )

    print(
        f"  Uncertain          : "
        f"{class_count - accepted_count}"
    )

    print(
        f"  Accepted correct   : "
        f"{correct_count}"
    )

    print(
        f"  Accepted incorrect : "
        f"{accepted_count - correct_count}"
    )

    print(
        f"  Accepted accuracy  : "
        f"{accepted_accuracy:.2%}"
    )


# ============================================================
# BLIGHT ↔ GRAY LEAF SPOT ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("BLIGHT ↔ GRAY LEAF SPOT ANALYSIS")
print("=" * 70)

blight_index = CLASS_NAMES.index(
    "Blight"
)

gray_index = CLASS_NAMES.index(
    "Gray_Leaf_Spot"
)

pair_mask = (
    (y_true == blight_index) |
    (y_true == gray_index)
)

pair_predictions = (
    (y_pred == blight_index) |
    (y_pred == gray_index)
)

confused_pair = (
    pair_mask &
    pair_predictions &
    (y_pred != y_true)
)

pair_confused_count = np.sum(
    confused_pair
)

print(
    f"\nTotal Blight + Gray Leaf Spot images: "
    f"{np.sum(pair_mask)}"
)

print(
    f"Blight ↔ Gray Leaf Spot confusions: "
    f"{pair_confused_count}"
)

print("\nConfused cases by direction:")

blight_to_gray = np.sum(
    (y_true == blight_index) &
    (y_pred == gray_index)
)

gray_to_blight = np.sum(
    (y_true == gray_index) &
    (y_pred == blight_index)
)

print(
    f"  Blight → Gray Leaf Spot : "
    f"{blight_to_gray}"
)

print(
    f"  Gray Leaf Spot → Blight : "
    f"{gray_to_blight}"
)


# ============================================================
# CONFIDENCE OF INCORRECT PREDICTIONS
# ============================================================

print("\n" + "=" * 70)
print("INCORRECT PREDICTION CONFIDENCE")
print("=" * 70)

incorrect_confidences = confidence[
    ~correct
]

if len(incorrect_confidences) > 0:

    print(
        f"\nIncorrect predictions: "
        f"{len(incorrect_confidences)}"
    )

    print(
        f"Minimum confidence : "
        f"{np.min(incorrect_confidences):.2%}"
    )

    print(
        f"Maximum confidence : "
        f"{np.max(incorrect_confidences):.2%}"
    )

    print(
        f"Mean confidence    : "
        f"{np.mean(incorrect_confidences):.2%}"
    )

    print(
        f"Median confidence  : "
        f"{np.median(incorrect_confidences):.2%}"
    )


# ============================================================
# HIGH-CONFIDENCE ERRORS
# ============================================================

print("\n" + "=" * 70)
print("HIGH-CONFIDENCE INCORRECT PREDICTIONS")
print("=" * 70)

for threshold in [
    0.70,
    0.80,
    0.90,
    0.95
]:

    high_confidence_errors = (
        (~correct) &
        (confidence >= threshold)
    )

    count = np.sum(
        high_confidence_errors
    )

    print(
        f"\nIncorrect predictions ≥ "
        f"{threshold:.0%}: {count}"
    )


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 70)
print("CONFIDENCE ANALYSIS COMPLETE")
print("=" * 70)
