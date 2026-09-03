import os
import pandas as pd


# ============================================================
# V1 THRESHOLD ANALYSIS
# ============================================================

PROJECT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CSV_PATH = os.path.join(
    PROJECT_DIR,
    "results",
    "confidence_analysis",
    "v1_confidence_predictions.csv"
)


CLASS_NAMES = [
    "Blight",
    "Common_Rust",
    "Gray_Leaf_Spot",
    "Healthy"
]


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("V1 CNN THRESHOLD ANALYSIS")
print("=" * 70)

print("\nReading:")
print(f"  {CSV_PATH}")

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(
        f"\nCSV file not found:\n{CSV_PATH}"
    )

df = pd.read_csv(CSV_PATH)

print("\nCSV loaded successfully.")

print(f"Images analyzed : {len(df)}")


# ============================================================
# NORMALIZE COLUMN TYPES
# ============================================================

df["confidence"] = pd.to_numeric(
    df["confidence"]
)

df["correct"] = (
    df["correct"]
    .astype(str)
    .str.lower()
    .map({
        "true": True,
        "false": False
    })
)


# ============================================================
# OVERALL CONFIDENCE
# ============================================================

print("\n" + "-" * 70)
print("1. OVERALL CONFIDENCE")
print("-" * 70)

correct_df = df[df["correct"] == True]
incorrect_df = df[df["correct"] == False]

print(
    f"\nCorrect predictions   : {len(correct_df)}"
)

print(
    f"Incorrect predictions : {len(incorrect_df)}"
)

print(
    f"\nCorrect confidence:"
)

print(
    f"  Minimum : {correct_df['confidence'].min() * 100:.2f}%"
)

print(
    f"  Maximum : {correct_df['confidence'].max() * 100:.2f}%"
)

print(
    f"  Average : {correct_df['confidence'].mean() * 100:.2f}%"
)

print(
    f"\nIncorrect confidence:"
)

print(
    f"  Minimum : {incorrect_df['confidence'].min() * 100:.2f}%"
)

print(
    f"  Maximum : {incorrect_df['confidence'].max() * 100:.2f}%"
)

print(
    f"  Average : {incorrect_df['confidence'].mean() * 100:.2f}%"
)


# ============================================================
# CANDIDATE THRESHOLDS
# ============================================================

print("\n" + "-" * 70)
print("2. CANDIDATE THRESHOLD ANALYSIS")
print("-" * 70)

thresholds = [
    0.50,
    0.60,
    0.65,
    0.70,
    0.75,
    0.80,
    0.85,
    0.90,
    0.95
]


print(
    "\nThreshold | Accepted | Rejected | "
    "Accepted Correct | Accepted Incorrect | Accuracy"
)

print("-" * 95)


for threshold in thresholds:

    accepted = df[
        df["confidence"] >= threshold
    ]

    rejected = df[
        df["confidence"] < threshold
    ]

    accepted_correct = accepted[
        accepted["correct"] == True
    ]

    accepted_incorrect = accepted[
        accepted["correct"] == False
    ]

    if len(accepted) > 0:
        accepted_accuracy = (
            len(accepted_correct)
            /
            len(accepted)
            *
            100
        )
    else:
        accepted_accuracy = 0

    print(
        f"{threshold * 100:8.0f}% | "
        f"{len(accepted):8d} | "
        f"{len(rejected):8d} | "
        f"{len(accepted_correct):16d} | "
        f"{len(accepted_incorrect):18d} | "
        f"{accepted_accuracy:7.2f}%"
    )


# ============================================================
# REJECTED CORRECT PREDICTIONS
# ============================================================

print("\n" + "-" * 70)
print("3. CORRECT PREDICTIONS THAT WOULD BE REJECTED")
print("-" * 70)


for threshold in thresholds:

    rejected_correct = df[
        (df["confidence"] < threshold)
        &
        (df["correct"] == True)
    ]

    percentage = (
        len(rejected_correct)
        /
        len(correct_df)
        *
        100
    )

    print(
        f"\nThreshold {threshold * 100:.0f}%:"
    )

    print(
        f"  Correct predictions rejected : "
        f"{len(rejected_correct)}"
    )

    print(
        f"  Percentage of all correct predictions : "
        f"{percentage:.2f}%"
    )


# ============================================================
# INCORRECT PREDICTIONS CAUGHT
# ============================================================

print("\n" + "-" * 70)
print("4. INCORRECT PREDICTIONS CAUGHT BY THRESHOLD")
print("-" * 70)


for threshold in thresholds:

    rejected_incorrect = df[
        (df["confidence"] < threshold)
        &
        (df["correct"] == False)
    ]

    percentage = (
        len(rejected_incorrect)
        /
        len(incorrect_df)
        *
        100
    )

    print(
        f"\nThreshold {threshold * 100:.0f}%:"
    )

    print(
        f"  Incorrect predictions rejected : "
        f"{len(rejected_incorrect)}"
    )

    print(
        f"  Percentage of all errors caught : "
        f"{percentage:.2f}%"
    )


# ============================================================
# BLIGHT ↔ GRAY LEAF SPOT
# ============================================================

print("\n" + "-" * 70)
print("5. BLIGHT ↔ GRAY LEAF SPOT")
print("-" * 70)


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

confused = pd.concat([
    blight_to_gray,
    gray_to_blight
])


print(
    f"\nBlight → Gray Leaf Spot : "
    f"{len(blight_to_gray)}"
)

print(
    f"Gray Leaf Spot → Blight : "
    f"{len(gray_to_blight)}"
)

print(
    f"Total confusion         : "
    f"{len(confused)}"
)


print(
    "\nConfidence:"
)

print(
    f"  Minimum : "
    f"{confused['confidence'].min() * 100:.2f}%"
)

print(
    f"  Maximum : "
    f"{confused['confidence'].max() * 100:.2f}%"
)

print(
    f"  Average : "
    f"{confused['confidence'].mean() * 100:.2f}%"
)


# ============================================================
# BLIGHT ↔ GRAY LEAF SPOT BY THRESHOLD
# ============================================================

print("\n" + "-" * 70)
print("6. BLIGHT ↔ GRAY LEAF SPOT ERRORS CAUGHT")
print("-" * 70)

print(
    "\nThreshold | Confusion Caught | "
    "Confusion Remaining"
)

print("-" * 55)


for threshold in thresholds:

    caught = confused[
        confused["confidence"] < threshold
    ]

    remaining = confused[
        confused["confidence"] >= threshold
    ]

    print(
        f"{threshold * 100:8.0f}% | "
        f"{len(caught):16d} | "
        f"{len(remaining):18d}"
    )


# ============================================================
# HIGH-CONFIDENCE ERRORS
# ============================================================

print("\n" + "-" * 70)
print("7. HIGH-CONFIDENCE ERRORS")
print("-" * 70)


high_conf_errors = incorrect_df[
    incorrect_df["confidence"] >= 0.90
].sort_values(
    "confidence",
    ascending=False
)


print(
    f"\nIncorrect predictions with ≥90% confidence:"
    f" {len(high_conf_errors)}"
)


if len(high_conf_errors) > 0:

    print(
        "\nTop high-confidence errors:"
    )

    print(
        high_conf_errors[
            [
                "actual_class",
                "predicted_class",
                "confidence"
            ]
        ]
        .head(20)
        .to_string(index=False)
    )


# ============================================================
# BLIGHT / GRAY HIGH-CONFIDENCE ERRORS
# ============================================================

print("\n" + "-" * 70)
print("8. HIGH-CONFIDENCE BLIGHT ↔ GRAY ERRORS")
print("-" * 70)


high_confused = confused[
    confused["confidence"] >= 0.70
].sort_values(
    "confidence",
    ascending=False
)


print(
    f"\nBlight ↔ Gray errors with ≥70% confidence:"
    f" {len(high_confused)}"
)


if len(high_confused) > 0:

    print(
        "\nThese are particularly important because "
        "the model was confident but wrong:"
    )

    print(
        high_confused[
            [
                "actual_class",
                "predicted_class",
                "confidence"
            ]
        ]
        .to_string(index=False)
    )


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("V1 THRESHOLD ANALYSIS COMPLETE")
print("=" * 70)

print(
    "\nNo threshold has been selected."
)

print(
    "This analysis is for evidence-based threshold selection."
)

print(
    "\nNext:"
)

print(
    "Compare the candidate thresholds and determine "
    "which threshold gives the best balance between "
    "diagnostic safety and useful coverage."
)

print("=" * 70)