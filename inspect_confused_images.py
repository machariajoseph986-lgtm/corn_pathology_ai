import os
import csv
import math

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_PATH = os.path.join(
    PROJECT_DIR,
    "results",
    "misclassifications",
    "misclassification_report.csv"
)

OUTPUT_DIR = os.path.join(
    PROJECT_DIR,
    "results",
    "misclassifications"
)

ALL_SHEET_PATH = os.path.join(
    OUTPUT_DIR,
    "all_bl_confused_contact_sheet.png"
)

BLIGHT_GLS_SHEET_PATH = os.path.join(
    OUTPUT_DIR,
    "blight_to_gray_leaf_spot_contact_sheet.png"
)

GLS_BLIGHT_SHEET_PATH = os.path.join(
    OUTPUT_DIR,
    "gray_leaf_spot_to_blight_contact_sheet.png"
)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("BLIGHT ↔ GRAY LEAF SPOT VISUAL DIAGNOSTIC")
print("=" * 70)

print("\nReading:")
print(f"  {CSV_PATH}")


# ============================================================
# CHECK CSV
# ============================================================

if not os.path.exists(CSV_PATH):

    raise FileNotFoundError(
        "\nERROR: Misclassification report not found:\n"
        f"{CSV_PATH}\n\n"
        "Run inspect_misclassifications.py first."
    )


# ============================================================
# LOAD CSV
# ============================================================

records = []

with open(
    CSV_PATH,
    "r",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    for row in reader:
        records.append(row)


if not records:

    raise RuntimeError(
        "\nERROR: No misclassification records found."
    )


# ============================================================
# SEPARATE CONFUSION DIRECTIONS
# ============================================================

blight_to_gls = [
    record
    for record in records
    if record["confusion"] == "Blight_to_Gray_Leaf_Spot"
]

gls_to_blight = [
    record
    for record in records
    if record["confusion"] == "Gray_Leaf_Spot_to_Blight"
]


# ============================================================
# IMAGE SHEET FUNCTION
# ============================================================

def create_contact_sheet(
    records,
    output_path,
    title
):

    if not records:
        print(
            f"\nNo images found for: {title}"
        )
        return

    columns = 4

    rows = math.ceil(
        len(records) / columns
    )

    figure, axes = plt.subplots(
        rows,
        columns,
        figsize=(16, 4 * rows)
    )

    # Make axes iterable even when only one row exists
    axes = np.array(axes).reshape(
        rows,
        columns
    )

    figure.suptitle(
        title,
        fontsize=18,
        fontweight="bold"
    )

    for index, record in enumerate(records):

        row = index // columns
        column = index % columns

        axis = axes[row, column]

        image_path = record["image_path"]

        actual = record["actual_class"]
        predicted = record["predicted_class"]

        confidence = float(
            record["confidence"]
        ) * 100

        try:

            image = Image.open(
                image_path
            ).convert("RGB")

            axis.imshow(image)

            axis.set_title(
                f"Actual: {actual}\n"
                f"Predicted: {predicted}\n"
                f"Confidence: {confidence:.2f}%",
                fontsize=10
            )

            axis.axis("off")

        except Exception as error:

            axis.text(
                0.5,
                0.5,
                f"Could not load image\n\n{error}",
                ha="center",
                va="center",
                wrap=True
            )

            axis.axis("off")


    # Hide unused panels

    for index in range(
        len(records),
        rows * columns
    ):

        row = index // columns
        column = index % columns

        axes[row, column].axis("off")


    figure.tight_layout(
        rect=[0, 0, 1, 0.96]
    )

    figure.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close(figure)

    print(
        f"\nCreated:"
        f"\n  {output_path}"
    )


# ============================================================
# CREATE ALL-CONFUSION SHEET
# ============================================================

all_records = (
    blight_to_gls
    +
    gls_to_blight
)

create_contact_sheet(
    all_records,
    ALL_SHEET_PATH,
    "Blight ↔ Gray Leaf Spot Misclassifications"
)


# ============================================================
# CREATE BLIGHT → GLS SHEET
# ============================================================

create_contact_sheet(
    blight_to_gls,
    BLIGHT_GLS_SHEET_PATH,
    "Blight → Gray Leaf Spot Misclassifications"
)


# ============================================================
# CREATE GLS → BLIGHT SHEET
# ============================================================

create_contact_sheet(
    gls_to_blight,
    GLS_BLIGHT_SHEET_PATH,
    "Gray Leaf Spot → Blight Misclassifications"
)


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("VISUAL DIAGNOSTIC COMPLETE")
print("=" * 70)

print(
    f"\nBlight → Gray Leaf Spot : "
    f"{len(blight_to_gls)} images"
)

print(
    f"Gray Leaf Spot → Blight : "
    f"{len(gls_to_blight)} images"
)

print(
    f"Total images inspected  : "
    f"{len(all_records)}"
)

print("\nGenerated visual reports:")

print(
    f"\n1. All confusion:"
    f"\n   {ALL_SHEET_PATH}"
)

print(
    f"\n2. Blight → Gray Leaf Spot:"
    f"\n   {BLIGHT_GLS_SHEET_PATH}"
)

print(
    f"\n3. Gray Leaf Spot → Blight:"
    f"\n   {GLS_BLIGHT_SHEET_PATH}"
)

print("\n" + "=" * 70)