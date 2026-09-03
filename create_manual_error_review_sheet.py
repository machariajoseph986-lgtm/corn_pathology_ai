"""
Manual Blight ↔ Gray Leaf Spot Error Review Sheet

Purpose:
    Create a structured manual-review package containing ONLY
    the 27 actual Blight ↔ Gray Leaf Spot classification errors.

This script:
    - does NOT modify the dataset
    - does NOT change labels
    - does NOT modify the CNN
    - does NOT retrain the model

Outputs:
    results/visual_analysis/manual_error_review/
"""

import os
import math
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

INPUT_CSV = os.path.join(
    PROJECT_DIR,
    "results",
    "visual_analysis",
    "focused_boundary_review",
    "focused_review_inventory.csv"
)

OUTPUT_DIR = os.path.join(
    PROJECT_DIR,
    "results",
    "visual_analysis",
    "manual_error_review"
)

HIGH_CSV = os.path.join(
    OUTPUT_DIR,
    "01_high_priority_errors_review.csv"
)

MEDIUM_CSV = os.path.join(
    OUTPUT_DIR,
    "02_medium_priority_errors_review.csv"
)

ALL_CSV = os.path.join(
    OUTPUT_DIR,
    "03_all_27_errors_review.csv"
)

HIGH_SHEET = os.path.join(
    OUTPUT_DIR,
    "04_high_priority_errors.png"
)

MEDIUM_SHEET = os.path.join(
    OUTPUT_DIR,
    "05_medium_priority_errors.png"
)

ALL_SHEET = os.path.join(
    OUTPUT_DIR,
    "06_all_27_errors.png"
)


# ============================================================
# REVIEW FIELDS
# ============================================================

REVIEW_COLUMNS = [

    "visual_review",

    "boundary_case",

    "label_review_needed",

    "severity",

    "image_quality",

    "lesion_shape",

    "lesion_distribution",

    "lesion_boundary_visibility",

    "background_difficulty",

    "notes"
]


# ============================================================
# VALID REVIEW VALUES
# ============================================================

VALID_VALUES = {

    "visual_review":
        "clear / difficult / ambiguous",

    "boundary_case":
        "yes / no",

    "label_review_needed":
        "yes / no / uncertain",

    "severity":
        "early / moderate / advanced / unclear",

    "image_quality":
        "good / acceptable / poor",

    "lesion_shape":
        "elongated / rectangular / irregular / mixed / unclear",

    "lesion_distribution":
        "isolated / sparse / moderate / dense / widespread / unclear",

    "lesion_boundary_visibility":
        "clear / moderate / poor",

    "background_difficulty":
        "simple / moderate / difficult",

    "notes":
        "free text"
}


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("MANUAL BLIGHT ↔ GRAY LEAF SPOT ERROR REVIEW")
print("=" * 70)

print("""
Purpose:

Create a 27-image manual-review package containing only
the actual Blight ↔ Gray Leaf Spot classification errors.

NO DATASET CHANGES WILL BE MADE.
NO LABELS WILL BE CHANGED.
NO MODEL WILL BE MODIFIED.
NO MODEL WILL BE RETRAINED.
""")


# ============================================================
# CHECK INPUT
# ============================================================

print("-" * 70)
print("CHECKING INPUT")
print("-" * 70)

print(f"\nInput:\n  {INPUT_CSV}")

if not os.path.exists(INPUT_CSV):

    raise FileNotFoundError(
        f"\nInput CSV not found:\n{INPUT_CSV}"
    )

print("\nInput CSV found.")


# ============================================================
# LOAD DATA
# ============================================================

print("-" * 70)
print("LOADING FOCUSED REVIEW INVENTORY")
print("-" * 70)

df = pd.read_csv(
    INPUT_CSV
)

print(f"\nRows loaded: {len(df)}")


# ============================================================
# SELECT ERROR CASES
# ============================================================

error_groups = [
    "Blight_to_Gray_Error",
    "Gray_to_Blight_Error"
]

errors = df[
    df["analysis_group"].isin(error_groups)
].copy()


# ============================================================
# SORT
# ============================================================

priority_order = {
    "HIGH": 0,
    "MEDIUM": 1,
    "REFERENCE": 2
}

errors["_priority_order"] = (
    errors["review_priority"]
    .map(priority_order)
    .fillna(99)
)

errors = errors.sort_values(
    by=[
        "_priority_order",
        "confidence"
    ],
    ascending=[
        True,
        False
    ]
).copy()

errors = errors.drop(
    columns=["_priority_order"]
)


# ============================================================
# VERIFY 27 CASES
# ============================================================

print("\n" + "-" * 70)
print("ERROR INVENTORY")
print("-" * 70)

high = errors[
    errors["review_priority"] == "HIGH"
].copy()

medium = errors[
    errors["review_priority"] == "MEDIUM"
].copy()

print(
    f"\nHigh-priority errors   : {len(high)}"
)

print(
    f"Medium-priority errors : {len(medium)}"
)

print(
    f"Total error cases      : {len(errors)}"
)

if len(errors) != 27:

    raise ValueError(
        f"\nExpected exactly 27 error cases, "
        f"but found {len(errors)}."
    )


# ============================================================
# ADD MANUAL REVIEW COLUMNS
# ============================================================

for frame in [high, medium, errors]:

    frame["manual_review_id"] = ""

    for column in REVIEW_COLUMNS:

        frame[column] = ""


# ============================================================
# CREATE STABLE REVIEW IDs
# ============================================================

counter = 1

for index in errors.index:

    errors.loc[
        index,
        "manual_review_id"
    ] = f"ERR_{counter:02d}"

    counter += 1


# Recreate the same IDs in the subsets
id_map = errors[
    ["image_path", "manual_review_id"]
].drop_duplicates(
    subset=["image_path"]
)

high = high.drop(
    columns=["manual_review_id"]
).merge(
    id_map,
    on="image_path",
    how="left"
)

medium = medium.drop(
    columns=["manual_review_id"]
).merge(
    id_map,
    on="image_path",
    how="left"
)


# ============================================================
# COLUMN ORDER
# ============================================================

base_columns = [
    "manual_review_id",
    "actual_class",
    "predicted_class",
    "confidence",
    "analysis_group",
    "review_priority",
    "image_path"
]

final_columns = (
    base_columns +
    REVIEW_COLUMNS
)


errors = errors[
    final_columns
]

high = high[
    final_columns
]

medium = medium[
    final_columns
]


# ============================================================
# SAVE CSV FILES
# ============================================================

print("\n" + "-" * 70)
print("SAVING REVIEW CSV FILES")
print("-" * 70)

high.to_csv(
    HIGH_CSV,
    index=False
)

print(
    f"\nHigh priority:\n  {HIGH_CSV}"
)

medium.to_csv(
    MEDIUM_CSV,
    index=False
)

print(
    f"\nMedium priority:\n  {MEDIUM_CSV}"
)

errors.to_csv(
    ALL_CSV,
    index=False
)

print(
    f"\nAll 27 errors:\n  {ALL_CSV}"
)


# ============================================================
# IMAGE SHEET FUNCTION
# ============================================================

def create_visual_sheet(
    data,
    output_path,
    title,
    columns=4
):

    if len(data) == 0:
        print(
            f"\nNo images available for: {title}"
        )
        return

    rows = math.ceil(
        len(data) / columns
    )

    fig, axes = plt.subplots(
        rows,
        columns,
        figsize=(18, 4.8 * rows)
    )

    if hasattr(axes, "flat"):
        axes = list(axes.flat)
    else:
        axes = [axes]

    for ax in axes:
        ax.axis("off")

    for i, (_, record) in enumerate(
        data.iterrows()
    ):

        ax = axes[i]

        image_path = record[
            "image_path"
        ]

        review_id = record[
            "manual_review_id"
        ]

        actual = record[
            "actual_class"
        ]

        predicted = record[
            "predicted_class"
        ]

        confidence = float(
            record["confidence"]
        )

        try:

            image = Image.open(
                image_path
            )

            ax.imshow(image)

        except Exception as e:

            ax.text(
                0.5,
                0.5,
                "IMAGE COULD NOT BE LOADED",
                ha="center",
                va="center"
            )

        ax.axis("off")

        ax.set_title(
            f"{review_id}\n"
            f"Actual: {actual}\n"
            f"Predicted: {predicted}\n"
            f"Confidence: {confidence * 100:.2f}%",
            fontsize=10
        )

    fig.suptitle(
        title,
        fontsize=18
    )

    plt.tight_layout(
        rect=[0, 0, 1, 0.97]
    )

    plt.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"\nVisual sheet saved:\n  {output_path}"
    )


# ============================================================
# CREATE VISUAL SHEETS
# ============================================================

print("\n" + "-" * 70)
print("CREATING VISUAL REVIEW SHEETS")
print("-" * 70)

create_visual_sheet(
    high,
    HIGH_SHEET,
    "HIGH-PRIORITY BLIGHT ↔ GRAY LEAF SPOT ERRORS"
)

create_visual_sheet(
    medium,
    MEDIUM_SHEET,
    "MEDIUM-PRIORITY BLIGHT ↔ GRAY LEAF SPOT ERRORS"
)

create_visual_sheet(
    errors,
    ALL_SHEET,
    "ALL 27 BLIGHT ↔ GRAY LEAF SPOT ERRORS"
)


# ============================================================
# PRINT REVIEW INSTRUCTIONS
# ============================================================

print("\n" + "=" * 70)
print("MANUAL REVIEW INSTRUCTIONS")
print("=" * 70)

print("""
Open:

  04_high_priority_errors.png

Start with ERR_01 onward.

For each image, enter your observations into:

  01_high_priority_errors_review.csv
  02_medium_priority_errors_review.csv

You can also use:

  03_all_27_errors_review.csv

Review the following fields:

  visual_review
  boundary_case
  label_review_needed
  severity
  image_quality
  lesion_shape
  lesion_distribution
  lesion_boundary_visibility
  background_difficulty
  notes
""")

print("\nAllowed values:")

for field, values in VALID_VALUES.items():

    print(
        f"  {field}: {values}"
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("MANUAL ERROR REVIEW PACKAGE COMPLETE")
print("=" * 70)

print("""
Created:

  results/visual_analysis/manual_error_review/

    01_high_priority_errors_review.csv
    02_medium_priority_errors_review.csv
    03_all_27_errors_review.csv

    04_high_priority_errors.png
    05_medium_priority_errors.png
    06_all_27_errors.png

Total images:
  27

High priority:
  13

Medium priority:
  14

NO DATASET CHANGES WERE MADE.
NO LABELS WERE CHANGED.
NO MODEL WAS MODIFIED.
NO MODEL WAS RETRAINED.

Next step:

Manually review the 27 error images.

DO NOT change the original dataset.

After the CSV has been completed, run the
severity/error analysis again.
""")

print("=" * 70)