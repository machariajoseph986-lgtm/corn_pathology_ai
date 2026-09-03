"""
Blight ↔ Gray Leaf Spot Boundary Review Inventory

Purpose
-------
Convert the existing V1 visual-analysis CSV into a structured
manual-review inventory.

IMPORTANT
---------
This script does NOT:
    - modify the dataset
    - change image labels
    - train a model
    - modify V1
    - use the test set for retraining

It only creates a review worksheet for identifying:
    - boundary cases
    - disease severity
    - image quality issues
    - possible label-review cases
    - visual characteristics relevant to the
      Blight ↔ Gray Leaf Spot boundary
"""

import os
import pandas as pd


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
    "v1_blight_gray_visual_analysis.csv"
)

OUTPUT_DIR = os.path.join(
    PROJECT_DIR,
    "results",
    "visual_analysis"
)

OUTPUT_CSV = os.path.join(
    OUTPUT_DIR,
    "blight_gray_boundary_review.csv"
)


# ============================================================
# REVIEW VALUES
# ============================================================

REVIEW_COLUMNS = {

    "visual_review": "",

    "boundary_case": "",

    "label_review_needed": "",

    "severity": "",

    "image_quality": "",

    "lesion_shape": "",

    "lesion_distribution": "",

    "lesion_boundary_visibility": "",

    "background_difficulty": "",

    "notes": ""
}


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("BLIGHT ↔ GRAY LEAF SPOT BOUNDARY REVIEW INVENTORY")
print("=" * 70)

print("""
Purpose:

Create a structured manual-review worksheet from the existing
V1 visual-analysis results.

NO DATASET CHANGES WILL BE MADE.
NO LABELS WILL BE CHANGED.
NO MODEL WILL BE RETRAINED.
""")


# ============================================================
# CHECK INPUT
# ============================================================

print("-" * 70)
print("CHECKING INPUT CSV")
print("-" * 70)

print(f"\nInput:")
print(f"  {INPUT_CSV}")

if not os.path.exists(INPUT_CSV):

    raise FileNotFoundError(
        "\nVisual-analysis CSV not found.\n\n"
        "Expected:\n"
        f"{INPUT_CSV}\n\n"
        "Run analyze_blight_gray_visuals.py first."
    )

print("\nInput CSV found.")


# ============================================================
# LOAD CSV
# ============================================================

print("-" * 70)
print("LOADING VISUAL-ANALYSIS DATA")
print("-" * 70)

df = pd.read_csv(INPUT_CSV)

print(f"\nRows loaded: {len(df)}")

print("\nColumns found:")

for column in df.columns:
    print(f"  {column}")


# ============================================================
# IDENTIFY REQUIRED COLUMNS
# ============================================================

required_columns = [
    "actual_class",
    "predicted_class",
    "confidence"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    raise ValueError(
        "\nThe visual-analysis CSV is missing required columns:\n"
        + "\n".join(
            f"  - {column}"
            for column in missing_columns
        )
    )


# ============================================================
# FILTER BLIGHT ↔ GRAY
# ============================================================

pair_mask = (

    (
        (df["actual_class"] == "Blight")
        &
        (df["predicted_class"] == "Gray_Leaf_Spot")
    )

    |

    (
        (df["actual_class"] == "Gray_Leaf_Spot")
        &
        (df["predicted_class"] == "Blight")
    )

    |

    (
        (df["actual_class"] == "Blight")
        &
        (df["predicted_class"] == "Blight")
    )

    |

    (
        (df["actual_class"] == "Gray_Leaf_Spot")
        &
        (df["predicted_class"] == "Gray_Leaf_Spot")
    )
)

review_df = df.loc[pair_mask].copy()

print("\nBlight / Gray Leaf Spot images selected:")
print(f"  {len(review_df)}")


# ============================================================
# CREATE ANALYSIS GROUP
# ============================================================

def determine_group(row):

    actual = row["actual_class"]
    predicted = row["predicted_class"]

    if (
        actual == "Blight"
        and predicted == "Gray_Leaf_Spot"
    ):
        return "Blight_to_Gray_Error"

    if (
        actual == "Gray_Leaf_Spot"
        and predicted == "Blight"
    ):
        return "Gray_to_Blight_Error"

    if (
        actual == "Blight"
        and predicted == "Blight"
    ):
        return "Correct_Blight"

    if (
        actual == "Gray_Leaf_Spot"
        and predicted == "Gray_Leaf_Spot"
    ):
        return "Correct_Gray"

    return "Other"


review_df["analysis_group"] = review_df.apply(
    determine_group,
    axis=1
)


# ============================================================
# ADD REVIEW FIELDS
# ============================================================

for column, default_value in REVIEW_COLUMNS.items():

    if column not in review_df.columns:

        review_df[column] = default_value


# ============================================================
# REVIEW PRIORITY
# ============================================================

def determine_priority(row):

    group = row["analysis_group"]
    confidence = float(row["confidence"])

    # Highest priority:
    # confident errors between the two diseases.
    if (
        group in [
            "Blight_to_Gray_Error",
            "Gray_to_Blight_Error"
        ]
        and confidence >= 0.70
    ):
        return "HIGH"

    # Other pair errors.
    if group in [
        "Blight_to_Gray_Error",
        "Gray_to_Blight_Error"
    ]:
        return "MEDIUM"

    # Correct examples are comparison/reference examples.
    return "REFERENCE"


review_df["review_priority"] = review_df.apply(
    determine_priority,
    axis=1
)


# ============================================================
# REVIEW INSTRUCTIONS
# ============================================================

review_df["review_instructions"] = (

    "Manually inspect image. "
    "Record whether it is a boundary case, "
    "severity, image quality, lesion shape, "
    "lesion distribution, lesion-boundary visibility, "
    "background difficulty, and notes."
)


# ============================================================
# SORT
# ============================================================

priority_order = {
    "HIGH": 0,
    "MEDIUM": 1,
    "REFERENCE": 2
}

review_df["_priority_order"] = (
    review_df["review_priority"]
    .map(priority_order)
)

review_df = review_df.sort_values(
    by=[
        "_priority_order",
        "analysis_group",
        "confidence"
    ],
    ascending=[
        True,
        True,
        False
    ]
)

review_df = review_df.drop(
    columns=["_priority_order"]
)


# ============================================================
# SAVE
# ============================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

review_df.to_csv(
    OUTPUT_CSV,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("REVIEW INVENTORY SUMMARY")
print("=" * 70)

print("\nGroups:")

group_counts = (
    review_df["analysis_group"]
    .value_counts()
)

for group, count in group_counts.items():

    print(
        f"  {group:<25} : {count}"
    )


print("\nReview priority:")

priority_counts = (
    review_df["review_priority"]
    .value_counts()
)

for priority, count in priority_counts.items():

    print(
        f"  {priority:<25} : {count}"
    )


print("\n" + "-" * 70)
print("MANUAL REVIEW CATEGORIES")
print("-" * 70)

print("""
For each image, review:

1. visual_review
   - clear
   - difficult
   - ambiguous

2. boundary_case
   - yes
   - no

3. label_review_needed
   - yes
   - no
   - uncertain

4. severity
   - early
   - moderate
   - advanced
   - unclear

5. image_quality
   - good
   - acceptable
   - poor

6. lesion_shape
   - elongated
   - rectangular
   - irregular
   - mixed
   - unclear

7. lesion_distribution
   - isolated
   - sparse
   - moderate
   - dense
   - widespread
   - unclear

8. lesion_boundary_visibility
   - clear
   - moderate
   - poor

9. background_difficulty
   - simple
   - moderate
   - difficult

10. notes
    Free-text observations.
""")


# ============================================================
# FINAL MESSAGE
# ============================================================

print("=" * 70)
print("REVIEW INVENTORY CREATED")
print("=" * 70)

print("\nSaved to:")

print(
    f"  {OUTPUT_CSV}"
)

print("""
IMPORTANT:

Do NOT modify the dataset yet.

The next phase is manual visual review of this inventory.

We will use the review results to determine which visual
characteristics should be strengthened in the training data
before V2 is trained.
""")

print("=" * 70)