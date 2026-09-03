"""
V1 Blight ↔ Gray Leaf Spot Visual Error Analysis

Purpose:
    Investigate the visual characteristics associated with
    Blight ↔ Gray Leaf Spot confusion in the V1 CNN.

Important:
    - Does NOT modify the trained CNN.
    - Uses the independent V1 test set.
    - Separates correct predictions from two-way confusion.
    - Creates visual comparison sheets.
"""

import os
import csv
import math

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "training_output",
    "best_maize_disease_cnn.keras"
)

TEST_DIR = os.path.join(
    PROJECT_DIR,
    "dataset_split",
    "test"
)

OUTPUT_DIR = os.path.join(
    PROJECT_DIR,
    "results",
    "visual_analysis"
)

IMAGE_SIZE = (256, 256)

CLASS_NAMES = [
    "Blight",
    "Common_Rust",
    "Gray_Leaf_Spot",
    "Healthy"
]

BLIGHT = "Blight"
GRAY = "Gray_Leaf_Spot"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# LOAD MODEL
# ============================================================

print("=" * 70)
print("V1 BLIGHT ↔ GRAY LEAF SPOT VISUAL ANALYSIS")
print("=" * 70)

print("\nLoading V1 CNN...")

model = tf.keras.models.load_model(
    MODEL_PATH
)

print("V1 CNN loaded successfully.")


# ============================================================
# FIND TEST IMAGES
# ============================================================

print("\n" + "-" * 70)
print("FINDING TEST IMAGES")
print("-" * 70)

image_records = []

for actual_class in CLASS_NAMES:

    class_dir = os.path.join(
        TEST_DIR,
        actual_class
    )

    if not os.path.isdir(class_dir):
        continue

    for filename in os.listdir(class_dir):

        filepath = os.path.join(
            class_dir,
            filename
        )

        if not os.path.isfile(filepath):
            continue

        if not filename.lower().endswith(
            (".jpg", ".jpeg", ".png", ".bmp")
        ):
            continue

        image_records.append(
            {
                "path": filepath,
                "actual": actual_class
            }
        )

print(
    f"Images found: {len(image_records)}"
)


# ============================================================
# GENERATE PREDICTIONS
# ============================================================

print("\n" + "-" * 70)
print("GENERATING V1 TEST PREDICTIONS")
print("-" * 70)

results = []

for index, record in enumerate(image_records):

    image = tf.keras.utils.load_img(
        record["path"],
        target_size=IMAGE_SIZE
    )

    image_array = (
        tf.keras.utils.img_to_array(image)
        / 255.0
    )

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    probabilities = model.predict(
        image_array,
        verbose=0
    )[0]

    predicted_index = int(
        np.argmax(probabilities)
    )

    predicted_class = CLASS_NAMES[
        predicted_index
    ]

    confidence = float(
        probabilities[predicted_index]
    )

    results.append(
        {
            "path": record["path"],
            "actual": record["actual"],
            "predicted": predicted_class,
            "confidence": confidence
        }
    )

    if (index + 1) % 50 == 0:
        print(
            f"Processed {index + 1}/"
            f"{len(image_records)}"
        )


# ============================================================
# IDENTIFY GROUPS
# ============================================================

blight_to_gray = [
    r for r in results
    if r["actual"] == BLIGHT
    and r["predicted"] == GRAY
]

gray_to_blight = [
    r for r in results
    if r["actual"] == GRAY
    and r["predicted"] == BLIGHT
]

correct_blight = [
    r for r in results
    if r["actual"] == BLIGHT
    and r["predicted"] == BLIGHT
]

correct_gray = [
    r for r in results
    if r["actual"] == GRAY
    and r["predicted"] == GRAY
]


# ============================================================
# SORT BY CONFIDENCE
# ============================================================

blight_to_gray.sort(
    key=lambda x: x["confidence"],
    reverse=True
)

gray_to_blight.sort(
    key=lambda x: x["confidence"],
    reverse=True
)

correct_blight.sort(
    key=lambda x: x["confidence"]
)

correct_gray.sort(
    key=lambda x: x["confidence"]
)


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("VISUAL ANALYSIS GROUPS")
print("=" * 70)

print(
    f"\nBlight → Gray Leaf Spot : "
    f"{len(blight_to_gray)}"
)

print(
    f"Gray Leaf Spot → Blight : "
    f"{len(gray_to_blight)}"
)

print(
    f"Correct Blight          : "
    f"{len(correct_blight)}"
)

print(
    f"Correct Gray Leaf Spot  : "
    f"{len(correct_gray)}"
)


# ============================================================
# SAVE CSV
# ============================================================

csv_path = os.path.join(
    OUTPUT_DIR,
    "v1_blight_gray_visual_analysis.csv"
)

with open(
    csv_path,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow(
        [
            "actual_class",
            "predicted_class",
            "confidence",
            "image_path"
        ]
    )

    for r in results:

        if (
            r["actual"] in [BLIGHT, GRAY]
            or r["predicted"] in [BLIGHT, GRAY]
        ):

            writer.writerow(
                [
                    r["actual"],
                    r["predicted"],
                    f"{r['confidence']:.6f}",
                    r["path"]
                ]
            )

print(
    "\nCSV saved to:"
    f"\n  {csv_path}"
)


# ============================================================
# VISUAL GRID FUNCTION
# ============================================================

def create_grid(
    records,
    title,
    output_filename,
    max_images=12
):

    records = records[:max_images]

    if not records:
        print(
            f"\nNo images available for: {title}"
        )
        return

    columns = 4
    rows = math.ceil(
        len(records) / columns
    )

    fig, axes = plt.subplots(
        rows,
        columns,
        figsize=(16, 4 * rows)
    )

    axes = np.array(
        axes
    ).reshape(-1)

    for ax in axes:
        ax.axis("off")

    for ax, record in zip(
        axes,
        records
    ):

        image = tf.keras.utils.load_img(
            record["path"]
        )

        ax.imshow(image)

        ax.set_title(
            f"Actual: {record['actual']}\n"
            f"Predicted: {record['predicted']}\n"
            f"Confidence: "
            f"{record['confidence'] * 100:.2f}%",
            fontsize=10
        )

        ax.axis("off")

    fig.suptitle(
        title,
        fontsize=16
    )

    plt.tight_layout(
        rect=[0, 0, 1, 0.96]
    )

    output_path = os.path.join(
        OUTPUT_DIR,
        output_filename
    )

    plt.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"\nVisual sheet saved:"
        f"\n  {output_path}"
    )


# ============================================================
# CREATE VISUAL SHEETS
# ============================================================

print("\n" + "-" * 70)
print("CREATING VISUAL COMPARISON SHEETS")
print("-" * 70)

create_grid(
    blight_to_gray,
    "V1 Errors: Blight → Gray Leaf Spot",
    "blight_to_gray_errors.png",
    max_images=12
)

create_grid(
    gray_to_blight,
    "V1 Errors: Gray Leaf Spot → Blight",
    "gray_to_blight_errors.png",
    max_images=12
)

create_grid(
    correct_blight,
    "V1 Correct Predictions: Blight",
    "correct_blight_examples.png",
    max_images=12
)

create_grid(
    correct_gray,
    "V1 Correct Predictions: Gray Leaf Spot",
    "correct_gray_examples.png",
    max_images=12
)


# ============================================================
# HIGH-CONFIDENCE CONFUSION
# ============================================================

high_confusion = [
    r for r in results
    if (
        (
            r["actual"] == BLIGHT
            and r["predicted"] == GRAY
        )
        or
        (
            r["actual"] == GRAY
            and r["predicted"] == BLIGHT
        )
    )
    and r["confidence"] >= 0.70
]

high_confusion.sort(
    key=lambda x: x["confidence"],
    reverse=True
)

create_grid(
    high_confusion,
    "High-Confidence Blight ↔ Gray Leaf Spot Errors",
    "high_confidence_blight_gray_errors.png",
    max_images=12
)


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 70)
print("VISUAL ANALYSIS COMPLETE")
print("=" * 70)

print("\nGenerated files:")

print(
    "\n  results/visual_analysis/"
)

print(
    "    blight_to_gray_errors.png"
)

print(
    "    gray_to_blight_errors.png"
)

print(
    "    correct_blight_examples.png"
)

print(
    "    correct_gray_examples.png"
)

print(
    "    high_confidence_blight_gray_errors.png"
)

print(
    "    v1_blight_gray_visual_analysis.csv"
)

print("\nNext step:")
print(
    "Compare the visual patterns across the "
    "four groups before making any changes "
    "to the dataset or CNN."
)

print("=" * 70)