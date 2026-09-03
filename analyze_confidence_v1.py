import os
import csv
import numpy as np
import tensorflow as tf


# ============================================================
# V1 CONFIDENCE ANALYSIS
# ============================================================

PROJECT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

VALIDATION_DIR = os.path.join(
    PROJECT_DIR,
    "dataset_split",
    "validation"
)

MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "training_output",
    "best_maize_disease_cnn.keras"
)

RESULTS_DIR = os.path.join(
    PROJECT_DIR,
    "results",
    "confidence_analysis"
)

CSV_PATH = os.path.join(
    RESULTS_DIR,
    "v1_confidence_predictions.csv"
)

IMAGE_SIZE = (256, 256)
BATCH_SIZE = 32
SEED = 42

CLASS_NAMES = [
    "Blight",
    "Common_Rust",
    "Gray_Leaf_Spot",
    "Healthy"
]


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs(
    RESULTS_DIR,
    exist_ok=True
)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("V1 CNN CONFIDENCE ANALYSIS")
print("=" * 70)

print("\nModel:")
print(f"  {MODEL_PATH}")

print("\nValidation dataset:")
print(f"  {VALIDATION_DIR}")


# ============================================================
# LOAD VALIDATION DATASET
# ============================================================

print("\n" + "-" * 70)
print("LOADING VALIDATION DATASET")
print("-" * 70)

validation_dataset = tf.keras.utils.image_dataset_from_directory(

    VALIDATION_DIR,

    labels="inferred",

    label_mode="int",

    image_size=IMAGE_SIZE,

    batch_size=BATCH_SIZE,

    shuffle=False,

    seed=SEED
)


print("\nClasses:")

for index, class_name in enumerate(
    validation_dataset.class_names
):
    print(f"  {index}: {class_name}")


# ============================================================
# NORMALIZATION
# ============================================================

validation_dataset = validation_dataset.map(

    lambda images, labels: (
        tf.cast(images, tf.float32) / 255.0,
        labels
    ),

    num_parallel_calls=tf.data.AUTOTUNE
)


validation_dataset = validation_dataset.prefetch(
    tf.data.AUTOTUNE
)


# ============================================================
# LOAD V1 MODEL
# ============================================================

print("\n" + "-" * 70)
print("LOADING V1 CNN MODEL")
print("-" * 70)

model = tf.keras.models.load_model(
    MODEL_PATH
)

print("V1 model loaded successfully.")


# ============================================================
# GENERATE PREDICTIONS
# ============================================================

print("\n" + "-" * 70)
print("GENERATING V1 PREDICTIONS")
print("-" * 70)

probabilities = model.predict(
    validation_dataset,
    verbose=1
)


# ============================================================
# GET TRUE LABELS
# ============================================================

true_labels = np.concatenate(
    [
        labels.numpy()
        for _, labels in validation_dataset
    ]
)


# ============================================================
# PREDICTIONS
# ============================================================

predicted_labels = np.argmax(
    probabilities,
    axis=1
)

confidence_scores = np.max(
    probabilities,
    axis=1
)


# ============================================================
# BASIC COUNTS
# ============================================================

total_images = len(true_labels)

correct_mask = (
    predicted_labels == true_labels
)

incorrect_mask = (
    predicted_labels != true_labels
)

correct_count = np.sum(
    correct_mask
)

incorrect_count = np.sum(
    incorrect_mask
)

accuracy = correct_count / total_images


# ============================================================
# OVERALL CONFIDENCE
# ============================================================

correct_confidence = confidence_scores[
    correct_mask
]

incorrect_confidence = confidence_scores[
    incorrect_mask
]


print("\n" + "=" * 70)
print("OVERALL CONFIDENCE SUMMARY")
print("=" * 70)

print(f"\nImages analyzed : {total_images}")
print(f"Correct         : {correct_count}")
print(f"Incorrect       : {incorrect_count}")
print(f"Accuracy        : {accuracy * 100:.2f}%")

print("\nCorrect prediction confidence:")

print(
    f"  Minimum : "
    f"{correct_confidence.min() * 100:.2f}%"
)

print(
    f"  Maximum : "
    f"{correct_confidence.max() * 100:.2f}%"
)

print(
    f"  Average : "
    f"{correct_confidence.mean() * 100:.2f}%"
)

if len(incorrect_confidence) > 0:

    print("\nIncorrect prediction confidence:")

    print(
        f"  Minimum : "
        f"{incorrect_confidence.min() * 100:.2f}%"
    )

    print(
        f"  Maximum : "
        f"{incorrect_confidence.max() * 100:.2f}%"
    )

    print(
        f"  Average : "
        f"{incorrect_confidence.mean() * 100:.2f}%"
    )


# ============================================================
# CONFIDENCE BANDS
# ============================================================

print("\n" + "-" * 70)
print("CONFIDENCE BAND ANALYSIS")
print("-" * 70)

confidence_bands = [
    (0.00, 0.50),
    (0.50, 0.60),
    (0.60, 0.70),
    (0.70, 0.80),
    (0.80, 0.90),
    (0.90, 1.01)
]


print(
    f"\n{'Confidence':<18}"
    f"{'Total':<10}"
    f"{'Correct':<10}"
    f"{'Incorrect':<10}"
    f"{'Accuracy':<10}"
)

print("-" * 58)


for lower, upper in confidence_bands:

    mask = (
        (confidence_scores >= lower)
        &
        (confidence_scores < upper)
    )

    total = np.sum(mask)

    if total == 0:
        continue

    correct = np.sum(
        correct_mask & mask
    )

    incorrect = np.sum(
        incorrect_mask & mask
    )

    band_accuracy = correct / total

    label = (
        f"{lower * 100:.0f}%–"
        f"{min(upper, 1.0) * 100:.0f}%"
    )

    print(
        f"{label:<18}"
        f"{total:<10}"
        f"{correct:<10}"
        f"{incorrect:<10}"
        f"{band_accuracy * 100:<10.2f}"
    )


# ============================================================
# BLIGHT ↔ GRAY LEAF SPOT
# ============================================================

print("\n" + "=" * 70)
print("BLIGHT ↔ GRAY LEAF SPOT CONFIDENCE ANALYSIS")
print("=" * 70)


blight_to_gray_mask = (
    (true_labels == 0)
    &
    (predicted_labels == 2)
)

gray_to_blight_mask = (
    (true_labels == 2)
    &
    (predicted_labels == 0)
)


blight_to_gray_confidence = (
    confidence_scores[
        blight_to_gray_mask
    ]
)

gray_to_blight_confidence = (
    confidence_scores[
        gray_to_blight_mask
    ]
)


print(
    "\nBlight → Gray Leaf Spot:"
)

print(
    f"  Errors : "
    f"{len(blight_to_gray_confidence)}"
)

if len(blight_to_gray_confidence) > 0:

    print(
        f"  Minimum confidence : "
        f"{blight_to_gray_confidence.min() * 100:.2f}%"
    )

    print(
        f"  Maximum confidence : "
        f"{blight_to_gray_confidence.max() * 100:.2f}%"
    )

    print(
        f"  Average confidence : "
        f"{blight_to_gray_confidence.mean() * 100:.2f}%"
    )


print(
    "\nGray Leaf Spot → Blight:"
)

print(
    f"  Errors : "
    f"{len(gray_to_blight_confidence)}"
)

if len(gray_to_blight_confidence) > 0:

    print(
        f"  Minimum confidence : "
        f"{gray_to_blight_confidence.min() * 100:.2f}%"
    )

    print(
        f"  Maximum confidence : "
        f"{gray_to_blight_confidence.max() * 100:.2f}%"
    )

    print(
        f"  Average confidence : "
        f"{gray_to_blight_confidence.mean() * 100:.2f}%"
    )


# ============================================================
# CLASS-BY-CLASS CONFIDENCE
# ============================================================

print("\n" + "=" * 70)
print("CLASS-BY-CLASS CONFIDENCE")
print("=" * 70)


for class_index, class_name in enumerate(
    CLASS_NAMES
):

    class_mask = (
        true_labels == class_index
    )

    class_correct_mask = (
        class_mask
        &
        correct_mask
    )

    class_incorrect_mask = (
        class_mask
        &
        incorrect_mask
    )

    class_confidence = confidence_scores[
        class_mask
    ]

    class_correct_confidence = confidence_scores[
        class_correct_mask
    ]

    print(
        f"\n{class_name}"
    )

    print(
        f"  Images    : "
        f"{np.sum(class_mask)}"
    )

    print(
        f"  Correct   : "
        f"{np.sum(class_correct_mask)}"
    )

    print(
        f"  Incorrect : "
        f"{np.sum(class_incorrect_mask)}"
    )

    print(
        f"  Accuracy  : "
        f"{np.mean(class_correct_mask[class_mask]) * 100:.2f}%"
    )

    print(
        f"  Avg confidence : "
        f"{class_confidence.mean() * 100:.2f}%"
    )

    if len(class_correct_confidence) > 0:

        print(
            f"  Avg correct confidence : "
            f"{class_correct_confidence.mean() * 100:.2f}%"
        )


# ============================================================
# SAVE DETAILED CSV
# ============================================================

print("\n" + "-" * 70)
print("SAVING DETAILED CONFIDENCE DATA")
print("-" * 70)


# ------------------------------------------------------------
# ORIGINAL CLASS ORDER
# ------------------------------------------------------------

# Do NOT read class_names from the transformed dataset.
# The class order is fixed by the original dataset structure.

class_names = CLASS_NAMES


# ------------------------------------------------------------
# COLLECT IMAGE PATHS
# ------------------------------------------------------------

image_paths = []

for class_name in class_names:

    class_directory = os.path.join(
        VALIDATION_DIR,
        class_name
    )

    if not os.path.isdir(class_directory):
        continue

    for filename in sorted(
        os.listdir(class_directory)
    ):

        if filename.lower().endswith(
            (".jpg", ".jpeg", ".png", ".bmp")
        ):

            image_paths.append(
                os.path.join(
                    class_directory,
                    filename
                )
            )


# ------------------------------------------------------------
# VERIFY IMAGE/PREDICTION ALIGNMENT
# ------------------------------------------------------------

if len(image_paths) != total_images:

    print("\nWARNING:")
    print(
        f"Image paths found : {len(image_paths)}"
    )
    print(
        f"Predictions       : {total_images}"
    )

    print(
        "\nCSV was NOT created because the number "
        "of image paths does not match the predictions."
    )

else:

    # --------------------------------------------------------
    # WRITE CSV
    # --------------------------------------------------------

    with open(
        CSV_PATH,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "image_path",
            "actual_class",
            "predicted_class",
            "confidence",
            "correct",
            "blight_gray_confusion"
        ])

        for i in range(total_images):

            actual = CLASS_NAMES[
                true_labels[i]
            ]

            predicted = CLASS_NAMES[
                predicted_labels[i]
            ]

            is_correct = (
                true_labels[i]
                ==
                predicted_labels[i]
            )

            is_bl_gray_confusion = (
                (
                    true_labels[i] == 0
                    and
                    predicted_labels[i] == 2
                )
                or
                (
                    true_labels[i] == 2
                    and
                    predicted_labels[i] == 0
                )
            )

            writer.writerow([
                image_paths[i],
                actual,
                predicted,
                f"{confidence_scores[i]:.6f}",
                is_correct,
                is_bl_gray_confusion
            ])

    print(
        "\nDetailed CSV saved to:"
    )

    print(
        f"  {CSV_PATH}"
    )

    print(
        f"\nRows written: {total_images}"
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("V1 CONFIDENCE ANALYSIS COMPLETE")
print("=" * 70)

print(
    "\nIMPORTANT:"
)

print(
    "No threshold has been applied."
)

print(
    "No model has been modified."
)

print(
    "This analysis is only measuring how V1 confidence"
)

print(
    "behaves before we decide on a diagnostic threshold."
)

print("\nNext decision:")

print(
    "Use these results to determine whether a confidence"
)

print(
    "threshold can meaningfully improve diagnostic reliability."
)

print("=" * 70)