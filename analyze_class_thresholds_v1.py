import os
import pandas as pd


# ============================================================
# V1 CLASS-SPECIFIC THRESHOLD ANALYSIS
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


CLASSES = [
    "Blight",
    "Common_Rust",
    "Gray_Leaf_Spot",
    "Healthy"
]


THRESHOLDS = [
    0.50,
    0.55,
    0.60,
    0.65,
    0.70,
    0.75,
    0.80,
    0.85,
    0.90,
    0.95
]


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 75)
print("V1 CNN CLASS-SPECIFIC THRESHOLD ANALYSIS")
print("=" * 75)

print("\nReading:")
print(f"  {CSV_PATH}")

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(
        f"\nCSV file not found:\n{CSV_PATH}"
    )

df = pd.read_csv(CSV_PATH)

print("\nCSV loaded successfully.")

print(f"Total predictions : {len(df)}")


# ============================================================
# NORMALIZE DATA
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
# ANALYZE EACH DISEASE
# ============================================================

for class_name in CLASSES:

    print("\n")
    print("=" * 75)
    print(f"{class_name.upper()}")
    print("=" * 75)

    class_df = df[
        df["actual_class"] == class_name
    ]

    correct = class_df[
        class_df["correct"] == True
    ]

    incorrect = class_df[
        class_df["correct"] == False
    ]

    print(
        f"\nActual {class_name} images : "
        f"{len(class_df)}"
    )

    print(
        f"Correctly diagnosed       : "
        f"{len(correct)}"
    )

    print(
        f"Incorrectly diagnosed     : "
        f"{len(incorrect)}"
    )

    if len(class_df) > 0:

        baseline_accuracy = (
            len(correct)
            /
            len(class_df)
            *
            100
        )

        print(
            f"Baseline recall           : "
            f"{baseline_accuracy:.2f}%"
        )

    print("\nConfidence of correct predictions:")

    if len(correct) > 0:

        print(
            f"  Minimum : "
            f"{correct['confidence'].min() * 100:.2f}%"
        )

        print(
            f"  Average : "
            f"{correct['confidence'].mean() * 100:.2f}%"
        )

        print(
            f"  Maximum : "
            f"{correct['confidence'].max() * 100:.2f}%"
        )

    print("\nConfidence of incorrect predictions:")

    if len(incorrect) > 0:

        print(
            f"  Minimum : "
            f"{incorrect['confidence'].min() * 100:.2f}%"
        )

        print(
            f"  Average : "
            f"{incorrect['confidence'].mean() * 100:.2f}%"
        )

        print(
            f"  Maximum : "
            f"{incorrect['confidence'].max() * 100:.2f}%"
        )

    # --------------------------------------------------------
    # THRESHOLD TABLE
    # --------------------------------------------------------

    print("\n")
    print(
        "Threshold | Accepted | Rejected | "
        "Accepted Correct | Accepted Wrong | Accuracy"
    )

    print("-" * 85)

    for threshold in THRESHOLDS:

        accepted = class_df[
            class_df["confidence"] >= threshold
        ]

        rejected = class_df[
            class_df["confidence"] < threshold
        ]

        accepted_correct = accepted[
            accepted["correct"] == True
        ]

        accepted_wrong = accepted[
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
            f"{len(accepted_wrong):14d} | "
            f"{accepted_accuracy:8.2f}%"
        )


# ============================================================
# COMPARISON OF 70% ACROSS CLASSES
# ============================================================

print("\n")
print("=" * 75)
print("70% THRESHOLD — CLASS-BY-CLASS COMPARISON")
print("=" * 75)

print(
    "\nClass              Actual   Accepted   Rejected   "
    "Accepted Correct   Accepted Wrong   Accuracy"
)

print("-" * 95)


for class_name in CLASSES:

    class_df = df[
        df["actual_class"] == class_name
    ]

    accepted = class_df[
        class_df["confidence"] >= 0.70
    ]

    rejected = class_df[
        class_df["confidence"] < 0.70
    ]

    accepted_correct = accepted[
        accepted["correct"] == True
    ]

    accepted_wrong = accepted[
        accepted["correct"] == False
    ]

    if len(accepted) > 0:

        accuracy = (
            len(accepted_correct)
            /
            len(accepted)
            *
            100
        )

    else:

        accuracy = 0

    print(
        f"{class_name:<18} "
        f"{len(class_df):6d} "
        f"{len(accepted):10d} "
        f"{len(rejected):10d} "
        f"{len(accepted_correct):18d} "
        f"{len(accepted_wrong):16d} "
        f"{accuracy:9.2f}%"
    )


# ============================================================
# HOW MANY CORRECT PREDICTIONS WOULD BE REJECTED?
# ============================================================

print("\n")
print("=" * 75)
print("CORRECT DIAGNOSES REJECTED AT 70%")
print("=" * 75)


for class_name in CLASSES:

    class_df = df[
        df["actual_class"] == class_name
    ]

    correct = class_df[
        class_df["correct"] == True
    ]

    rejected_correct = correct[
        correct["confidence"] < 0.70
    ]

    if len(correct) > 0:

        percentage = (
            len(rejected_correct)
            /
            len(correct)
            *
            100
        )

    else:

        percentage = 0

    print(
        f"\n{class_name}:"
    )

    print(
        f"  Correct predictions : "
        f"{len(correct)}"
    )

    print(
        f"  Rejected at 70%     : "
        f"{len(rejected_correct)}"
    )

    print(
        f"  Percentage rejected : "
        f"{percentage:.2f}%"
    )


# ============================================================
# LOW-CONFIDENCE CORRECT DIAGNOSES
# ============================================================

print("\n")
print("=" * 75)
print("LOW-CONFIDENCE CORRECT DIAGNOSES")
print("=" * 75)


for class_name in CLASSES:

    class_df = df[
        (df["actual_class"] == class_name)
        &
        (df["correct"] == True)
        &
        (df["confidence"] < 0.70)
    ].sort_values(
        "confidence"
    )

    print(
        f"\n{class_name}: "
        f"{len(class_df)} correct predictions below 70%"
    )

    if len(class_df) > 0:

        print(
            class_df[
                [
                    "actual_class",
                    "predicted_class",
                    "confidence"
                ]
            ].to_string(index=False)
        )


# ============================================================
# SUMMARY
# ============================================================

print("\n")
print("=" * 75)
print("CLASS-SPECIFIC THRESHOLD ANALYSIS COMPLETE")
print("=" * 75)

print(
    "\nNo threshold has been selected."
)

print(
    "The purpose of this analysis is to determine whether "
    "a global threshold or class-specific thresholds are "
    "better supported by V1 validation behavior."
)

print("=" * 75)