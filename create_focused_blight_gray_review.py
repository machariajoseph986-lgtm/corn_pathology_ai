"""
FOCUSED BLIGHT ↔ GRAY LEAF SPOT VISUAL REVIEW

Purpose:
    Create focused visual comparison sheets for manual review
    of the Blight ↔ Gray Leaf Spot decision boundary.

IMPORTANT:
    - No dataset changes.
    - No label changes.
    - No model changes.
    - No retraining.
"""

import os
import math
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


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
    "blight_gray_boundary_review.csv"
)

OUTPUT_DIR = os.path.join(
    PROJECT_DIR,
    "results",
    "visual_analysis",
    "focused_boundary_review"
)

REFERENCE_BLIGHT_COUNT = 10
REFERENCE_GRAY_COUNT = 10

IMAGES_PER_ROW = 4
TILE_WIDTH = 300
TILE_HEIGHT = 330


# ============================================================
# START
# ============================================================

print("=" * 70)
print("FOCUSED BLIGHT ↔ GRAY LEAF SPOT VISUAL REVIEW")
print("=" * 70)

print("""
Purpose:

Prepare a smaller, structured visual-review set from the existing
Blight ↔ Gray Leaf Spot boundary inventory.

This step does NOT change the dataset or CNN.
""")

print("-" * 70)
print("CHECKING INPUT")
print("-" * 70)

print(f"\nInput:")
print(f"  {INPUT_CSV}")

if not os.path.exists(INPUT_CSV):
    raise FileNotFoundError(
        f"\nBoundary review inventory not found:\n{INPUT_CSV}"
    )

print("\nInput CSV found.")

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# LOAD CSV
# ============================================================

print("-" * 70)
print("LOADING REVIEW INVENTORY")
print("-" * 70)

df = pd.read_csv(INPUT_CSV)

print(f"\nRows loaded: {len(df)}")

print("\nColumns:")
for column in df.columns:
    print(f"  {column}")


# ============================================================
# VERIFY REQUIRED COLUMNS
# ============================================================

required_columns = [
    "actual_class",
    "predicted_class",
    "confidence",
    "image_path",
    "analysis_group",
    "review_priority"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    raise ValueError(
        "\nRequired columns missing from input CSV:\n"
        + "\n".join(
            f"  {column}"
            for column in missing_columns
        )
    )


# ============================================================
# NORMALIZE COLUMNS
# ============================================================

df["confidence"] = pd.to_numeric(
    df["confidence"],
    errors="coerce"
)

df["review_priority"] = (
    df["review_priority"]
    .astype(str)
    .str.strip()
)

df["analysis_group"] = (
    df["analysis_group"]
    .astype(str)
    .str.strip()
)

df["actual_class"] = (
    df["actual_class"]
    .astype(str)
    .str.strip()
)

df["predicted_class"] = (
    df["predicted_class"]
    .astype(str)
    .str.strip()
)


# ============================================================
# HIGH PRIORITY
# ============================================================

high_df = df[
    df["review_priority"].str.upper() == "HIGH"
].copy()

high_df = high_df.sort_values(
    by="confidence",
    ascending=False
)


# ============================================================
# MEDIUM PRIORITY
# ============================================================

medium_df = df[
    df["review_priority"].str.upper() == "MEDIUM"
].copy()

medium_df = medium_df.sort_values(
    by="confidence",
    ascending=False
)


# ============================================================
# CORRECT REFERENCE IMAGES
# ============================================================

reference_df = df[
    (
        df["review_priority"].str.upper()
        == "REFERENCE"
    )
    &
    (
        df["actual_class"].isin(
            [
                "Blight",
                "Gray_Leaf_Spot"
            ]
        )
    )
    &
    (
        df["actual_class"]
        == df["predicted_class"]
    )
].copy()


# ============================================================
# SPREAD SELECTION
# ============================================================

def select_spread(
    input_df,
    count
):

    if len(input_df) <= count:
        return input_df.copy()

    if count <= 1:
        return input_df.iloc[[0]].copy()

    positions = [
        round(
            i * (len(input_df) - 1)
            / (count - 1)
        )
        for i in range(count)
    ]

    return input_df.iloc[
        positions
    ].copy()


blight_reference = reference_df[
    reference_df["actual_class"]
    == "Blight"
].sort_values(
    by="confidence"
)

gray_reference = reference_df[
    reference_df["actual_class"]
    == "Gray_Leaf_Spot"
].sort_values(
    by="confidence"
)

blight_reference = select_spread(
    blight_reference,
    REFERENCE_BLIGHT_COUNT
)

gray_reference = select_spread(
    gray_reference,
    REFERENCE_GRAY_COUNT
)

reference_selected = pd.concat(
    [
        blight_reference,
        gray_reference
    ],
    ignore_index=True
)


# ============================================================
# ADD MANUAL REVIEW COLUMNS
# ============================================================

manual_columns = [
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

for column in manual_columns:

    if column not in df.columns:

        df[column] = ""


# Make sure selected data contains those columns too.

for column in manual_columns:

    if column not in high_df.columns:
        high_df[column] = ""

    if column not in medium_df.columns:
        medium_df[column] = ""

    if column not in reference_selected.columns:
        reference_selected[column] = ""


# ============================================================
# COMBINED INVENTORY
# ============================================================

focused_df = pd.concat(
    [
        high_df,
        medium_df,
        reference_selected
    ],
    ignore_index=True
)


# ============================================================
# SAVE INVENTORIES
# ============================================================

print("\n" + "-" * 70)
print("SAVING FOCUSED REVIEW INVENTORIES")
print("-" * 70)

high_path = os.path.join(
    OUTPUT_DIR,
    "high_priority_errors.csv"
)

medium_path = os.path.join(
    OUTPUT_DIR,
    "medium_priority_errors.csv"
)

reference_path = os.path.join(
    OUTPUT_DIR,
    "reference_images.csv"
)

combined_path = os.path.join(
    OUTPUT_DIR,
    "focused_review_inventory.csv"
)

high_df.to_csv(
    high_path,
    index=False
)

medium_df.to_csv(
    medium_path,
    index=False
)

reference_selected.to_csv(
    reference_path,
    index=False
)

focused_df.to_csv(
    combined_path,
    index=False
)

print(f"\nHIGH errors:")
print(f"  {high_path}")

print(f"\nMEDIUM errors:")
print(f"  {medium_path}")

print(f"\nReferences:")
print(f"  {reference_path}")

print(f"\nCombined:")
print(f"  {combined_path}")


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FOCUSED REVIEW SUMMARY")
print("=" * 70)

print(
    f"\nHIGH-priority errors       : {len(high_df)}"
)

print(
    f"MEDIUM-priority errors     : {len(medium_df)}"
)

print(
    f"Correct Blight references  : "
    f"{len(blight_reference)}"
)

print(
    f"Correct Gray references    : "
    f"{len(gray_reference)}"
)

print(
    f"Total focused images       : "
    f"{len(focused_df)}"
)


# ============================================================
# FONT
# ============================================================

try:

    font = ImageFont.truetype(
        "arial.ttf",
        16
    )

    small_font = ImageFont.truetype(
        "arial.ttf",
        13
    )

except:

    font = ImageFont.load_default()
    small_font = ImageFont.load_default()


# ============================================================
# CREATE VISUAL SHEET
# ============================================================

def create_sheet(
    data,
    output_path,
    title
):

    if len(data) == 0:

        print(
            f"\nNo images available for:"
            f"\n  {title}"
        )

        return

    rows = math.ceil(
        len(data)
        / IMAGES_PER_ROW
    )

    sheet_width = (
        IMAGES_PER_ROW
        * TILE_WIDTH
    )

    title_height = 60

    sheet_height = (
        title_height
        + rows * TILE_HEIGHT
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
        (15, 15),
        title,
        fill="black",
        font=font
    )

    for index, (_, row) in enumerate(
        data.iterrows()
    ):

        image_path = row["image_path"]

        x = (
            index % IMAGES_PER_ROW
        ) * TILE_WIDTH

        y = (
            title_height
            + (
                index
                // IMAGES_PER_ROW
            ) * TILE_HEIGHT
        )

        try:

            image = Image.open(
                image_path
            ).convert("RGB")

            image.thumbnail(
                (
                    TILE_WIDTH - 20,
                    TILE_HEIGHT - 90
                )
            )

            image_x = (
                x
                + (
                    TILE_WIDTH
                    - image.width
                ) // 2
            )

            image_y = y + 10

            sheet.paste(
                image,
                (
                    image_x,
                    image_y
                )
            )

        except Exception as error:

            draw.text(
                (
                    x + 10,
                    y + 20
                ),
                "IMAGE ERROR",
                fill="black",
                font=font
            )

            draw.text(
                (
                    x + 10,
                    y + 45
                ),
                str(error)[:35],
                fill="black",
                font=small_font
            )

        actual = str(
            row["actual_class"]
        )

        predicted = str(
            row["predicted_class"]
        )

        confidence = float(
            row["confidence"]
        )

        group = str(
            row["analysis_group"]
        )

        metadata_y = (
            y
            + TILE_HEIGHT
            - 70
        )

        draw.text(
            (
                x + 8,
                metadata_y
            ),
            f"Actual: {actual}",
            fill="black",
            font=small_font
        )

        draw.text(
            (
                x + 8,
                metadata_y + 17
            ),
            f"Predicted: {predicted}",
            fill="black",
            font=small_font
        )

        draw.text(
            (
                x + 8,
                metadata_y + 34
            ),
            f"Confidence: "
            f"{confidence * 100:.2f}%",
            fill="black",
            font=small_font
        )

        draw.text(
            (
                x + 8,
                metadata_y + 51
            ),
            f"Group: {group}",
            fill="black",
            font=small_font
        )

    sheet.save(
        output_path
    )

    print(
        f"\nVisual sheet saved:"
        f"\n  {output_path}"
    )


# ============================================================
# CREATE SHEETS
# ============================================================

print("\n" + "-" * 70)
print("CREATING ERROR VISUAL SHEETS")
print("-" * 70)

create_sheet(
    high_df,
    os.path.join(
        OUTPUT_DIR,
        "01_high_priority_errors.png"
    ),
    "HIGH PRIORITY — BLIGHT ↔ GRAY LEAF SPOT ERRORS"
)

create_sheet(
    medium_df,
    os.path.join(
        OUTPUT_DIR,
        "02_medium_priority_errors.png"
    ),
    "MEDIUM PRIORITY — BLIGHT ↔ GRAY LEAF SPOT ERRORS"
)


print("\n" + "-" * 70)
print("CREATING REFERENCE VISUAL SHEETS")
print("-" * 70)

create_sheet(
    blight_reference,
    os.path.join(
        OUTPUT_DIR,
        "03_correct_blight_references.png"
    ),
    "REFERENCE — CORRECT BLIGHT"
)

create_sheet(
    gray_reference,
    os.path.join(
        OUTPUT_DIR,
        "04_correct_gray_references.png"
    ),
    "REFERENCE — CORRECT GRAY LEAF SPOT"
)


# ============================================================
# ALL ERRORS
# ============================================================

error_df = pd.concat(
    [
        high_df,
        medium_df
    ],
    ignore_index=True
)

create_sheet(
    error_df,
    os.path.join(
        OUTPUT_DIR,
        "05_all_boundary_errors.png"
    ),
    "ALL BLIGHT ↔ GRAY LEAF SPOT ERRORS"
)


# ============================================================
# COMPLETE COMPARISON
# ============================================================

comparison_df = pd.concat(
    [
        high_df,
        medium_df,
        blight_reference,
        gray_reference
    ],
    ignore_index=True
)

create_sheet(
    comparison_df,
    os.path.join(
        OUTPUT_DIR,
        "06_complete_focused_comparison.png"
    ),
    "FOCUSED BLIGHT ↔ GRAY LEAF SPOT COMPARISON"
)


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 70)
print("FOCUSED VISUAL REVIEW PREPARATION COMPLETE")
print("=" * 70)

print("""
Generated:

results/visual_analysis/focused_boundary_review/

    high_priority_errors.csv
    medium_priority_errors.csv
    reference_images.csv
    focused_review_inventory.csv

    01_high_priority_errors.png
    02_medium_priority_errors.png
    03_correct_blight_references.png
    04_correct_gray_references.png
    05_all_boundary_errors.png
    06_complete_focused_comparison.png

IMPORTANT:

NO DATASET CHANGES WERE MADE.
NO LABELS WERE CHANGED.
NO MODEL WAS MODIFIED.
NO MODEL WAS RETRAINED.

Next step:

Manually inspect the visual sheets.

Start with:

    01_high_priority_errors.png

Then:

    03_correct_blight_references.png
    04_correct_gray_references.png

Then:

    02_medium_priority_errors.png

Record observations in:

    focused_review_inventory.csv

Do not modify the original dataset yet.
""")

print("=" * 70)