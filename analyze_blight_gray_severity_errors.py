"""
BLIGHT ↔ GRAY LEAF SPOT SEVERITY / ERROR ANALYSIS

Purpose
-------
Analyze the manually reviewed Blight ↔ Gray Leaf Spot images to determine
whether classification errors are associated with disease severity.

This is an ANALYSIS-ONLY step.

NO dataset changes.
NO label changes.
NO model changes.
NO retraining.

Input:
    results/visual_analysis/focused_boundary_review/focused_review_inventory.csv

Output:
    results/visual_analysis/severity_analysis/
        severity_error_summary.csv
        severity_error_report.txt
        severity_error_cases.csv
"""

import os
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

INPUT_FILE = os.path.join(
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
    "severity_analysis"
)

SUMMARY_FILE = os.path.join(
    OUTPUT_DIR,
    "severity_error_summary.csv"
)

CASES_FILE = os.path.join(
    OUTPUT_DIR,
    "severity_error_cases.csv"
)

REPORT_FILE = os.path.join(
    OUTPUT_DIR,
    "severity_error_report.txt"
)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("BLIGHT ↔ GRAY LEAF SPOT SEVERITY / ERROR ANALYSIS")
print("=" * 70)

print("""
Purpose:

Determine whether manually recorded disease severity is associated
with Blight ↔ Gray Leaf Spot classification errors.

The analysis tests the hypothesis that early/mild disease and advanced
leaf damage may produce visually overlapping characteristics.

NO DATASET CHANGES WILL BE MADE.
NO LABELS WILL BE CHANGED.
NO MODEL WILL BE RETRAINED.
""")


# ============================================================
# CHECK INPUT
# ============================================================

print("-" * 70)
print("CHECKING INPUT")
print("-" * 70)

print(f"\nInput:")
print(f"  {INPUT_FILE}")

if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(
        f"\nFocused review inventory not found:\n{INPUT_FILE}"
    )

print("\nInput CSV found.")


# ============================================================
# LOAD DATA
# ============================================================

print("-" * 70)
print("LOADING FOCUSED REVIEW INVENTORY")
print("-" * 70)

df = pd.read_csv(INPUT_FILE)

print(f"\nRows loaded: {len(df)}")

required_columns = [
    "actual_class",
    "predicted_class",
    "confidence",
    "analysis_group",
    "severity",
    "visual_review",
    "boundary_case",
    "image_quality",
    "lesion_shape",
    "lesion_distribution",
    "lesion_boundary_visibility",
    "background_difficulty",
    "notes"
]

missing = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing:
    raise ValueError(
        "\nMissing required columns:\n"
        + "\n".join(f"  {column}" for column in missing)
    )


# ============================================================
# NORMALIZE TEXT
# ============================================================

text_columns = [
    "actual_class",
    "predicted_class",
    "analysis_group",
    "severity",
    "visual_review",
    "boundary_case",
    "image_quality",
    "lesion_shape",
    "lesion_distribution",
    "lesion_boundary_visibility",
    "background_difficulty"
]

for column in text_columns:
    df[column] = (
        df[column]
        .fillna("")
        .astype(str)
        .str.strip()
    )


# ============================================================
# DEFINE ERROR TYPE
# ============================================================

def classify_error(row):

    actual = row["actual_class"]
    predicted = row["predicted_class"]

    if actual == predicted:
        if actual == "Blight":
            return "Correct_Blight"
        elif actual == "Gray_Leaf_Spot":
            return "Correct_Gray"

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

    return "Other"


df["error_type"] = df.apply(
    classify_error,
    axis=1
)


# ============================================================
# FILTER BOUNDARY DATA
# ============================================================

df = df[
    df["error_type"].isin([
        "Correct_Blight",
        "Correct_Gray",
        "Blight_to_Gray_Error",
        "Gray_to_Blight_Error"
    ])
].copy()

print(
    f"\nBlight / Gray Leaf Spot records analyzed: {len(df)}"
)


# ============================================================
# SUMMARY BY SEVERITY
# ============================================================

print("\n" + "=" * 70)
print("1. SEVERITY VS CLASSIFICATION ERROR")
print("=" * 70)

severity_order = [
    "early",
    "moderate",
    "advanced",
    "unclear"
]

summary_rows = []

for severity in severity_order:

    subset = df[
        df["severity"].str.lower() == severity
    ]

    total = len(subset)

    if total == 0:
        continue

    errors = subset[
        subset["error_type"].isin([
            "Blight_to_Gray_Error",
            "Gray_to_Blight_Error"
        ])
    ]

    correct = subset[
        subset["error_type"].isin([
            "Correct_Blight",
            "Correct_Gray"
        ])
    ]

    row = {
        "severity": severity,
        "total_images": total,
        "correct_predictions": len(correct),
        "errors": len(errors),
        "error_rate_percent": (
            len(errors) / total * 100
        ),
        "blight_to_gray_errors": len(
            subset[
                subset["error_type"]
                == "Blight_to_Gray_Error"
            ]
        ),
        "gray_to_blight_errors": len(
            subset[
                subset["error_type"]
                == "Gray_to_Blight_Error"
            ]
        )
    }

    summary_rows.append(row)

    print(
        f"\n{severity.upper()}"
    )
    print(
        f"  Images          : {total}"
    )
    print(
        f"  Correct         : {len(correct)}"
    )
    print(
        f"  Errors          : {len(errors)}"
    )
    print(
        f"  Error rate      : "
        f"{row['error_rate_percent']:.2f}%"
    )
    print(
        f"  Blight → Gray   : "
        f"{row['blight_to_gray_errors']}"
    )
    print(
        f"  Gray → Blight   : "
        f"{row['gray_to_blight_errors']}"
    )


summary_df = pd.DataFrame(summary_rows)


# ============================================================
# ERROR-ONLY SEVERITY ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("2. SEVERITY DISTRIBUTION OF ERRORS")
print("=" * 70)

errors_df = df[
    df["error_type"].isin([
        "Blight_to_Gray_Error",
        "Gray_to_Blight_Error"
    ])
].copy()

if len(errors_df) > 0:

    error_severity = (
        errors_df["severity"]
        .value_counts()
        .reindex(
            severity_order,
            fill_value=0
        )
    )

    for severity, count in error_severity.items():

        percentage = (
            count / len(errors_df) * 100
        )

        print(
            f"  {severity:<10} : "
            f"{count:>3} "
            f"({percentage:.2f}%)"
        )

else:

    print("\nNo classification errors found.")


# ============================================================
# DIRECTIONAL ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("3. DIRECTIONAL ERROR ANALYSIS")
print("=" * 70)

for error_type, label in [
    (
        "Blight_to_Gray_Error",
        "BLIGHT → GRAY LEAF SPOT"
    ),
    (
        "Gray_to_Blight_Error",
        "GRAY LEAF SPOT → BLIGHT"
    )
]:

    subset = errors_df[
        errors_df["error_type"] == error_type
    ]

    print(f"\n{label}")

    if len(subset) == 0:
        print("  No cases.")
        continue

    counts = (
        subset["severity"]
        .value_counts()
        .reindex(
            severity_order,
            fill_value=0
        )
    )

    for severity, count in counts.items():
        print(
            f"  {severity:<10} : {count}"
        )


# ============================================================
# CONFIDENCE BY SEVERITY
# ============================================================

print("\n" + "=" * 70)
print("4. CONFIDENCE BY SEVERITY")
print("=" * 70)

for severity in severity_order:

    subset = df[
        df["severity"].str.lower() == severity
    ]

    if len(subset) == 0:
        continue

    confidence = subset["confidence"]

    print(
        f"\n{severity.upper()}"
    )
    print(
        f"  Average confidence : "
        f"{confidence.mean() * 100:.2f}%"
    )
    print(
        f"  Minimum confidence : "
        f"{confidence.min() * 100:.2f}%"
    )
    print(
        f"  Maximum confidence : "
        f"{confidence.max() * 100:.2f}%"
    )


# ============================================================
# VISUAL CHARACTERISTICS OF ERRORS
# ============================================================

print("\n" + "=" * 70)
print("5. VISUAL CHARACTERISTICS ASSOCIATED WITH ERRORS")
print("=" * 70)

characteristics = [
    "lesion_shape",
    "lesion_distribution",
    "lesion_boundary_visibility",
    "image_quality",
    "background_difficulty",
    "visual_review",
    "boundary_case"
]

for column in characteristics:

    print(
        f"\n{column}:"
    )

    counts = (
        errors_df[column]
        .replace("", "unrecorded")
        .value_counts()
    )

    if len(counts) == 0:
        print("  No data.")
        continue

    for value, count in counts.items():

        percentage = (
            count / len(errors_df) * 100
        )

        print(
            f"  {value:<20} : "
            f"{count:>3} "
            f"({percentage:.2f}%)"
        )


# ============================================================
# HIGH-CONFIDENCE ERRORS
# ============================================================

print("\n" + "=" * 70)
print("6. HIGH-CONFIDENCE BOUNDARY ERRORS")
print("=" * 70)

high_conf_errors = errors_df[
    errors_df["confidence"] >= 0.70
].copy()

print(
    f"\nErrors ≥70% confidence: "
    f"{len(high_conf_errors)}"
)

if len(high_conf_errors) > 0:

    for _, row in (
        high_conf_errors
        .sort_values(
            "confidence",
            ascending=False
        )
        .iterrows()
    ):

        print(
            f"\n  {row['error_type']}"
        )

        print(
            f"    Severity    : "
            f"{row['severity']}"
        )

        print(
            f"    Confidence  : "
            f"{row['confidence'] * 100:.2f}%"
        )

        print(
            f"    Image       : "
            f"{row.get('image_path', '')}"
        )


# ============================================================
# SAVE CASE-LEVEL ERROR FILE
# ============================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

errors_df.to_csv(
    CASES_FILE,
    index=False
)

print("\n" + "-" * 70)
print("ERROR CASE FILE SAVED")
print("-" * 70)

print(
    f"\n  {CASES_FILE}"
)


# ============================================================
# SAVE SUMMARY CSV
# ============================================================

summary_df.to_csv(
    SUMMARY_FILE,
    index=False
)

print(
    f"\nSummary CSV saved:"
)
print(
    f"  {SUMMARY_FILE}"
)


# ============================================================
# INTERPRETATION
# ============================================================

print("\n" + "=" * 70)
print("7. PRELIMINARY INTERPRETATION")
print("=" * 70)

interpretation = []

if len(summary_df) == 0:

    interpretation.append(
        "No usable severity ratings were recorded."
    )

else:

    highest_row = summary_df.loc[
        summary_df["error_rate_percent"].idxmax()
    ]

    lowest_row = summary_df.loc[
        summary_df["error_rate_percent"].idxmin()
    ]

    interpretation.append(
        f"The highest observed error rate occurs in the "
        f"'{highest_row['severity']}' severity group "
        f"({highest_row['error_rate_percent']:.2f}%)."
    )

    interpretation.append(
        f"The lowest observed error rate occurs in the "
        f"'{lowest_row['severity']}' severity group "
        f"({lowest_row['error_rate_percent']:.2f}%)."
    )

    if len(errors_df) > 0:

        interpretation.append(
            f"There are {len(errors_df)} Blight ↔ Gray Leaf Spot "
            f"errors in the focused review set."
        )

    interpretation.append(
        "Severity association should be treated as evidence "
        "for dataset refinement only if the manually reviewed "
        "sample is sufficiently consistent."
    )

    interpretation.append(
        "This analysis does NOT establish that severity causes "
        "classification errors."
    )


for item in interpretation:
    print(
        f"\n  {item}"
    )


# ============================================================
# WRITE REPORT
# ============================================================

with open(
    REPORT_FILE,
    "w",
    encoding="utf-8"
) as report:

    report.write(
        "BLIGHT ↔ GRAY LEAF SPOT "
        "SEVERITY / ERROR ANALYSIS\n"
    )

    report.write(
        "=" * 70 + "\n\n"
    )

    report.write(
        "Purpose:\n"
    )

    report.write(
        "Determine whether manually recorded disease severity "
        "is associated with Blight ↔ Gray Leaf Spot "
        "classification errors.\n\n"
    )

    report.write(
        "Important:\n"
        "NO DATASET CHANGES WERE MADE.\n"
        "NO LABELS WERE CHANGED.\n"
        "NO MODEL WAS RETRAINED.\n\n"
    )

    report.write(
        f"Focused images analyzed: {len(df)}\n"
    )

    report.write(
        f"Boundary errors analyzed: {len(errors_df)}\n\n"
    )

    report.write(
        "SEVERITY SUMMARY\n"
    )

    report.write(
        "-" * 70 + "\n"
    )

    for _, row in summary_df.iterrows():

        report.write(
            f"{row['severity']}: "
            f"{row['total_images']} images, "
            f"{row['errors']} errors, "
            f"{row['error_rate_percent']:.2f}% error rate\n"
        )

    report.write("\n")

    report.write(
        "PRELIMINARY INTERPRETATION\n"
    )

    report.write(
        "-" * 70 + "\n"
    )

    for item in interpretation:
        report.write(
            f"- {item}\n"
        )

    report.write("\n")

    report.write(
        "NEXT DECISION POINT\n"
    )

    report.write(
        "-" * 70 + "\n"
    )

    report.write(
        "Use the severity results together with the manual "
        "visual observations to determine whether V2 should "
        "include additional early-stage, moderate-stage, "
        "and advanced-stage examples for both Blight and "
        "Gray Leaf Spot.\n"
    )

print(
    f"\nReport saved:"
)
print(
    f"  {REPORT_FILE}"
)


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 70)
print("SEVERITY / ERROR ANALYSIS COMPLETE")
print("=" * 70)

print("""
No dataset modifications were made.

The important outputs are:

  severity_error_summary.csv
  severity_error_cases.csv
  severity_error_report.txt

These results will tell us whether the severity hypothesis
is supported strongly enough to influence the V2 data-refinement plan.
""")