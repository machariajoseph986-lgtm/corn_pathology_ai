"""
V1 CNN — BLIGHT ↔ GRAY LEAF SPOT ERROR ANALYSIS

Purpose:
    Visually investigate the test-set images that V1 confuses
    between Blight and Gray Leaf Spot.

This script does NOT modify the trained model.

It identifies:
    - Blight → Gray Leaf Spot errors
    - Gray Leaf Spot → Blight errors
    - High-confidence pair errors (>=70%)

It creates:
    - CSV containing error details
    - Contact sheet of all pair-confusion images
    - Contact sheet of high-confidence pair-confusion images
"""

import os

import numpy as np
import pandas as pd
import tensorflow as tf
from PIL import Image, ImageDraw, ImageFont


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
    "blight_gray_analysis"
)

os.makedirs(
    RESULTS_DIR,
    exist_ok=True
)

IMAGE_SIZE = (256, 256)
BATCH_SIZE = 32

THRESHOLD = 0.70

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
print("V1 CNN — BLIGHT ↔ GRAY LEAF SPOT ERROR ANALYSIS")
print("=" * 70)

print("\nModel:")
print(f"  {MODEL_PATH}")

print("\nTest dataset:")
print(f"  {TEST_DIR}")

print("\nTarget:")
print("  Blight ↔ Gray Leaf Spot")


# ============================================================
# LOAD DATASET
# ============================================================

print("\n" + "-" * 70)
print("LOADING TEST DATASET")
print("-" * 70)

dataset = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

file_paths = dataset.file_paths

print(
    f"\nImages found: {len(file_paths)}"
)


# ============================================================
# PREPROCESS
# ============================================================

dataset = dataset.map(
    lambda images, labels: (
        tf.cast(images, tf.float32) / 255.0,
        labels
    ),
    num_parallel_calls=tf.data.AUTOTUNE
)

dataset = dataset.prefetch(
    tf.data.AUTOTUNE
)


# ============================================================
# LOAD MODEL
# ============================================================

print("\n" + "-" * 70)
print("LOADING V1 MODEL")
print("-" * 70)

model = tf.keras.models.load_model(
    MODEL_PATH
)

print("\nV1 model loaded successfully.")


# ============================================================
# GENERATE PREDICTIONS
# ============================================================

print("\n" + "-" * 70)
print("GENERATING PREDICTIONS")
print("-" * 70)

probabilities = model.predict(
    dataset,
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
        for _, labels in dataset
    ]
)


# ============================================================
# FIND BLIGHT ↔ GRAY ERRORS
# ============================================================

pair_mask = (

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


pair_indices = np.where(
    pair_mask
)[0]


# ============================================================
# BUILD ERROR DATA
# ============================================================

records = []

for index in pair_indices:

    actual = CLASS_NAMES[
        true_classes[index]
    ]

    predicted = CLASS_NAMES[
        predicted_classes[index]
    ]

    records.append({

        "image_path": file_paths[index],

        "actual_class": actual,

        "predicted_class": predicted,

        "confidence": float(
            confidence[index]
        ),

        "confidence_percent":
            float(
                confidence[index] * 100
            ),

        "high_confidence":
            bool(
                confidence[index]
                >= THRESHOLD
            )
    })


df = pd.DataFrame(
    records
)


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("BLIGHT ↔ GRAY LEAF SPOT ERROR SUMMARY")
print("=" * 70)

blight_to_gray = df[
    (df["actual_class"] == "Blight")
    &
    (df["predicted_class"] == "Gray_Leaf_Spot")
]

gray_to_blight = df[
    (df["actual_class"] == "Gray_Leaf_Spot")
    &
    (df["predicted_class"] == "Blight")
]

high_confidence = df[
    df["high_confidence"]
]


print(
    f"\nTotal pair-confusion errors : "
    f"{len(df)}"
)

print(
    f"Blight → Gray Leaf Spot     : "
    f"{len(blight_to_gray)}"
)

print(
    f"Gray Leaf Spot → Blight     : "
    f"{len(gray_to_blight)}"
)

print(
    f"Pair errors ≥70% confidence : "
    f"{len(high_confidence)}"
)


# ============================================================
# CONFIDENCE DETAILS
# ============================================================

if len(df) > 0:

    print("\nConfidence of pair-confusion errors:")

    print(
        f"  Minimum : "
        f"{df['confidence_percent'].min():.2f}%"
    )

    print(
        f"  Average : "
        f"{df['confidence_percent'].mean():.2f}%"
    )

    print(
        f"  Maximum : "
        f"{df['confidence_percent'].max():.2f}%"
    )


# ============================================================
# SAVE CSV
# ============================================================

csv_path = os.path.join(
    RESULTS_DIR,
    "blight_gray_leaf_spot_errors.csv"
)

df.sort_values(
    "confidence",
    ascending=False
).to_csv(
    csv_path,
    index=False
)

print(
    "\nDetailed error CSV saved to:"
)

print(
    f"  {csv_path}"
)


# ============================================================
# CONTACT SHEET FUNCTION
# ============================================================

def create_contact_sheet(
    dataframe,
    output_path,
    title
):

    if dataframe.empty:

        print(
            f"\nNo images available for: "
            f"{title}"
        )

        return


    thumb_width = 220
    thumb_height = 220

    text_height = 75

    columns = 4

    rows = int(
        np.ceil(
            len(dataframe)
            / columns
        )
    )

    sheet_width = (
        columns
        * thumb_width
    )

    sheet_height = (
        80
        +
        rows
        * (
            thumb_height
            +
            text_height
        )
    )

    sheet = Image.new(
        "RGB",
        (
            sheet_width,
            sheet_height
        ),
        "white"
    )

    draw = ImageDraw.Draw(
        sheet
    )

    draw.text(
        (10, 10),
        title,
        fill="black"
    )

    for position, (_, row) in enumerate(
        dataframe.iterrows()
    ):

        image_path = row[
            "image_path"
        ]

        try:

            image = Image.open(
                image_path
            ).convert("RGB")

            image.thumbnail(
                (
                    thumb_width - 10,
                    thumb_height - 10
                )
            )

            x = (
                (position % columns)
                * thumb_width
                + 5
            )

            y = (
                80
                +
                (position // columns)
                * (
                    thumb_height
                    +
                    text_height
                )
            )

            image_x = (
                x
                +
                (
                    thumb_width
                    - image.width
                )
                // 2
            )

            image_y = (
                y
                +
                (
                    thumb_height
                    - image.height
                )
                // 2
            )

            sheet.paste(
                image,
                (
                    image_x,
                    image_y
                )
            )

            filename = os.path.basename(
                image_path
            )

            actual = row[
                "actual_class"
            ]

            predicted = row[
                "predicted_class"
            ]

            conf = row[
                "confidence_percent"
            ]

            label = (
                f"Actual: {actual}\n"
                f"Predicted: {predicted}\n"
                f"Confidence: {conf:.2f}%\n"
                f"{filename}"
            )

            draw.multiline_text(
                (
                    x + 5,
                    y + thumb_height
                ),
                label,
                fill="black"
            )

        except Exception as error:

            print(
                f"\nCould not open:"
                f"\n  {image_path}"
                f"\nReason:"
                f"\n  {error}"
            )


    sheet.save(
        output_path
    )

    print(
        f"\nContact sheet saved to:"
        f"\n  {output_path}"
    )


# ============================================================
# CONTACT SHEET 1 — ALL PAIR ERRORS
# ============================================================

all_errors_path = os.path.join(
    RESULTS_DIR,
    "all_blight_gray_errors.png"
)

create_contact_sheet(
    df,
    all_errors_path,
    "V1 Blight ↔ Gray Leaf Spot Errors"
)


# ============================================================
# CONTACT SHEET 2 — HIGH CONFIDENCE
# ============================================================

high_confidence_path = os.path.join(
    RESULTS_DIR,
    "high_confidence_blight_gray_errors.png"
)

create_contact_sheet(
    high_confidence,
    high_confidence_path,
    "V1 High-Confidence Blight ↔ Gray Leaf Spot Errors (≥70%)"
)


# ============================================================
# CONTACT SHEET 3 — BLIGHT → GRAY
# ============================================================

blight_gray_path = os.path.join(
    RESULTS_DIR,
    "blight_to_gray_errors.png"
)

create_contact_sheet(
    blight_to_gray,
    blight_gray_path,
    "Blight → Gray Leaf Spot Errors"
)


# ============================================================
# CONTACT SHEET 4 — GRAY → BLIGHT
# ============================================================

gray_blight_path = os.path.join(
    RESULTS_DIR,
    "gray_to_blight_errors.png"
)

create_contact_sheet(
    gray_to_blight,
    gray_blight_path,
    "Gray Leaf Spot → Blight Errors"
)


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 70)
print("BLIGHT ↔ GRAY LEAF SPOT ANALYSIS COMPLETE")
print("=" * 70)

print("\nGenerated:")

print(
    f"  {csv_path}"
)

print(
    f"  {all_errors_path}"
)

print(
    f"  {high_confidence_path}"
)

print(
    f"  {blight_gray_path}"
)

print(
    f"  {gray_blight_path}"
)

print(
    "\nNext:"
)

print(
    "Open the contact sheets and visually inspect "
    "the confused images."
)