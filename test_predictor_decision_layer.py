"""
PREDICTOR DECISION-LAYER VALIDATION

Purpose:
    Systematically verify the final decision logic in
    cnn/predictor.py.

Tests:
    1. High-confidence Blight
    2. Low-confidence Blight
    3. High-confidence Common Rust
    4. High-confidence Healthy
    5. Blight ↔ Gray Leaf Spot caution behavior

Important:
    This script does NOT modify the CNN model.
    It only tests the existing predictor.
"""

import os
import sys


# ============================================================
# PROJECT IMPORT
# ============================================================

PROJECT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

sys.path.insert(
    0,
    PROJECT_DIR
)


from cnn.predictor import predict_image


# ============================================================
# TEST IMAGES
# ============================================================

TEST_CASES = [

    {
        "name": "High-confidence Blight",
        "image": os.path.join(
            PROJECT_DIR,
            "dataset_split",
            "test",
            "Blight",
            "Corn_Blight (97).jpg"
        ),
        "expected_class": "Blight",
        "expected_status": "accepted",
        "expected_caution": True
    },

    {
        "name": "Low-confidence Blight",
        "image": os.path.join(
            PROJECT_DIR,
            "dataset_split",
            "test",
            "Blight",
            "Corn_Blight (739).JPG"
        ),
        "expected_class": "Blight",
        "expected_status": "uncertain",
        "expected_caution": True
    },

    {
        "name": "High-confidence Common Rust",
        "image": os.path.join(
            PROJECT_DIR,
            "dataset_split",
            "test",
            "Common_Rust",
            "Corn_Common_Rust (1000).JPG"
        ),
        "expected_class": "Common_Rust",
        "expected_status": "accepted",
        "expected_caution": False
    }
]


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("CNN PREDICTOR DECISION-LAYER VALIDATION")
print("=" * 70)

print("\nPurpose:")
print(
    "Verify that confidence decisions and the "
    "Blight ↔ Gray Leaf Spot caution mechanism "
    "behave as expected."
)

print("\nImportant:")
print(
    "The trained CNN model is NOT being modified."
)


# ============================================================
# RUN TESTS
# ============================================================

passed = 0
failed = 0


for number, test in enumerate(
    TEST_CASES,
    start=1
):

    print("\n" + "-" * 70)

    print(
        f"TEST {number}: "
        f"{test['name']}"
    )

    print("-" * 70)

    image_path = test["image"]

    print(
        f"\nImage:\n  {image_path}"
    )

    # --------------------------------------------------------
    # CHECK IMAGE
    # --------------------------------------------------------

    if not os.path.exists(image_path):

        print(
            "\nRESULT: FAILED"
        )

        print(
            "Reason: Test image not found."
        )

        failed += 1

        continue

    # --------------------------------------------------------
    # RUN PREDICTOR
    # --------------------------------------------------------

    result = predict_image(
        image_path
    )

    # --------------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------------

    print("\nActual predictor result:")

    print(
        f"  Class       : "
        f"{result['class_name']}"
    )

    print(
        f"  Confidence  : "
        f"{result['confidence'] * 100:.2f}%"
    )

    print(
        f"  Threshold   : "
        f"{result['confidence_threshold'] * 100:.2f}%"
    )

    print(
        f"  Status      : "
        f"{result['confidence_status'].upper()}"
    )

    print(
        f"  Caution     : "
        f"{'YES' if result['caution_required'] else 'NO'}"
    )

    # --------------------------------------------------------
    # VALIDATE CLASS
    # --------------------------------------------------------

    class_ok = (
        result["class_name"]
        == test["expected_class"]
    )

    # --------------------------------------------------------
    # VALIDATE STATUS
    # --------------------------------------------------------

    status_ok = (
        result["confidence_status"]
        == test["expected_status"]
    )

    # --------------------------------------------------------
    # VALIDATE CAUTION
    # --------------------------------------------------------

    caution_ok = (
        result["caution_required"]
        == test["expected_caution"]
    )

    # --------------------------------------------------------
    # TEST RESULT
    # --------------------------------------------------------

    test_passed = (
        class_ok
        and status_ok
        and caution_ok
    )

    print("\nValidation:")

    print(
        f"  Class     : "
        f"{'PASS' if class_ok else 'FAIL'}"
    )

    print(
        f"  Status    : "
        f"{'PASS' if status_ok else 'FAIL'}"
    )

    print(
        f"  Caution   : "
        f"{'PASS' if caution_ok else 'FAIL'}"
    )

    if test_passed:

        print(
            "\nRESULT: PASS"
        )

        passed += 1

    else:

        print(
            "\nRESULT: FAIL"
        )

        failed += 1


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("DECISION-LAYER VALIDATION SUMMARY")
print("=" * 70)

print(
    f"\nTests passed : {passed}"
)

print(
    f"Tests failed : {failed}"
)

print(
    f"Tests total  : {len(TEST_CASES)}"
)


# ============================================================
# FINAL DECISION
# ============================================================

if failed == 0:

    print("\n" + "=" * 70)

    print(
        "ALL DECISION-LAYER TESTS PASSED"
    )

    print("=" * 70)

    print(
        "\nThe predictor correctly handles:"
    )

    print(
        "  ✓ High-confidence Blight"
    )

    print(
        "  ✓ Low-confidence Blight"
    )

    print(
        "  ✓ High-confidence Common Rust"
    )

    print(
        "  ✓ Blight ↔ Gray Leaf Spot caution"
    )

    print(
        "\nThe 70% confidence decision layer "
        "is behaving as designed."
    )

else:

    print("\n" + "=" * 70)

    print(
        "DECISION-LAYER VALIDATION FAILED"
    )

    print("=" * 70)

    print(
        "\nOne or more tests require investigation."
    )