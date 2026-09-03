"""
End-to-End Plant Health Diagnosis Validation

Purpose:
Validate the complete diagnosis pipeline across all four
CNN classes:

    1. Blight
    2. Common_Rust
    3. Gray_Leaf_Spot
    4. Healthy

Pipeline being tested:

    Image
      ↓
    CNN prediction
      ↓
    Decision layer
      ↓
    CNN → Knowledge Base mapping
      ↓
    SQLite profile retrieval
      ↓
    Complete diagnosis result

The trained CNN model is NOT modified.
The SQLite knowledge base is NOT modified.
"""


import os
import sys


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)


# ============================================================
# IMPORT COMPLETE PIPELINE
# ============================================================

from cnn.database_integration import (
    diagnose_from_image
)


# ============================================================
# TEST CASES
# ============================================================

TEST_CASES = [

    {
        "name": "Blight",
        "image": os.path.join(
            PROJECT_DIR,
            "dataset_split",
            "test",
            "Blight",
            "Corn_Blight (1004).JPG"
        ),
        "expected_class": "Blight",
        "expected_kb_id": "HP_MAIZE_BLIGHT",
        "expected_healthy": False
    },

    {
        "name": "Common Rust",
        "image": os.path.join(
            PROJECT_DIR,
            "dataset_split",
            "test",
            "Common_Rust",
            "Corn_Common_Rust (1000).JPG"
        ),
        "expected_class": "Common_Rust",
        "expected_kb_id": "HP_MAIZE_COMMON_RUST",
        "expected_healthy": False
    },

    {
        "name": "Gray Leaf Spot",
        "image": os.path.join(
            PROJECT_DIR,
            "dataset_split",
            "test",
            "Gray_Leaf_Spot",
            "Corn_Gray_Spot (100).JPG"
        ),
        "expected_class": "Gray_Leaf_Spot",
        "expected_kb_id": "HP_MAIZE_GRAY_LEAF_SPOT",
        "expected_healthy": False
    },

    {
        "name": "Healthy",
        "image": os.path.join(
            PROJECT_DIR,
            "dataset_split",
            "test",
            "Healthy",
            "Corn_Health (1).jpg"
        ),
        "expected_class": "Healthy",
        "expected_kb_id": None,
        "expected_healthy": True
    }

]


# ============================================================
# VALIDATION
# ============================================================

def main():

    print("=" * 70)
    print("END-TO-END PLANT HEALTH DIAGNOSIS VALIDATION")
    print("=" * 70)

    print("\nPurpose:")
    print(
        "Validate the complete CNN → decision → "
        "mapping → database diagnosis pipeline."
    )

    print("\nThe trained CNN model is NOT being modified.")
    print("The SQLite knowledge base is NOT being modified.")

    total_tests = 0
    passed_tests = 0
    failed_tests = 0

    # ========================================================
    # RUN ALL TEST CASES
    # ========================================================

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

        print("\nImage:")
        print(test["image"])

        # ----------------------------------------------------
        # IMAGE CHECK
        # ----------------------------------------------------

        if not os.path.exists(
            test["image"]
        ):

            print("\nRESULT: FAIL")
            print("Image not found.")

            failed_tests += 1
            total_tests += 1

            continue

        # ----------------------------------------------------
        # RUN PIPELINE
        # ----------------------------------------------------

        print("\nRunning complete pipeline...")

        try:

            result = diagnose_from_image(
                test["image"]
            )

        except Exception as error:

            print("\nRESULT: FAIL")

            print(
                f"Pipeline error: {error}"
            )

            failed_tests += 1
            total_tests += 1

            continue

        # ----------------------------------------------------
        # DISPLAY RESULT
        # ----------------------------------------------------

        print("\nActual result:")

        print(
            f"  Class              : "
            f"{result['class_name']}"
        )

        print(
            f"  Confidence         : "
            f"{result['confidence']:.2%}"
        )

        print(
            f"  Confidence status  : "
            f"{result['confidence_status']}"
        )

        print(
            f"  Caution required   : "
            f"{result['caution_required']}"
        )

        print(
            f"  Knowledge Base ID  : "
            f"{result['health_problem_id']}"
        )

        print(
            f"  Healthy            : "
            f"{result['is_healthy']}"
        )

        print(
            f"  Disease profile    : "
            f"{'FOUND' if result['disease_profile'] else 'NONE'}"
        )

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        print("\nValidation:")

        test_passed = True

        # ----------------------------------------------------
        # CLASS
        # ----------------------------------------------------

        if (
            result["class_name"]
            == test["expected_class"]
        ):

            print(
                "  Class mapping       : PASS"
            )

        else:

            print(
                "  Class mapping       : FAIL"
            )

            print(
                f"    Expected: "
                f"{test['expected_class']}"
            )

            print(
                f"    Actual: "
                f"{result['class_name']}"
            )

            test_passed = False

        # ----------------------------------------------------
        # KNOWLEDGE BASE ID
        # ----------------------------------------------------

        if (
            result["health_problem_id"]
            == test["expected_kb_id"]
        ):

            print(
                "  Knowledge-base ID   : PASS"
            )

        else:

            print(
                "  Knowledge-base ID   : FAIL"
            )

            print(
                f"    Expected: "
                f"{test['expected_kb_id']}"
            )

            print(
                f"    Actual: "
                f"{result['health_problem_id']}"
            )

            test_passed = False

        # ----------------------------------------------------
        # HEALTHY FLAG
        # ----------------------------------------------------

        if (
            result["is_healthy"]
            == test["expected_healthy"]
        ):

            print(
                "  Healthy classification: PASS"
            )

        else:

            print(
                "  Healthy classification: FAIL"
            )

            print(
                f"    Expected: "
                f"{test['expected_healthy']}"
            )

            print(
                f"    Actual: "
                f"{result['is_healthy']}"
            )

            test_passed = False

        # ----------------------------------------------------
        # PROFILE LOGIC
        # ----------------------------------------------------

        if test["expected_healthy"]:

            profile_valid = (
                result["disease_profile"]
                is None
            )

        else:

            profile_valid = (
                result["disease_profile"]
                is not None
            )

        if profile_valid:

            print(
                "  Database profile    : PASS"
            )

        else:

            print(
                "  Database profile    : FAIL"
            )

            test_passed = False

        # ----------------------------------------------------
        # DECISION INFORMATION
        # ----------------------------------------------------

        decision_fields_present = all(
            field in result
            for field in [
                "confidence_status",
                "caution_required",
                "caution_reason"
            ]
        )

        if decision_fields_present:

            print(
                "  Decision information: PASS"
            )

        else:

            print(
                "  Decision information: FAIL"
            )

            test_passed = False

        # ----------------------------------------------------
        # TEST RESULT
        # ----------------------------------------------------

        total_tests += 1

        if test_passed:

            print("\nRESULT: PASS")

            passed_tests += 1

        else:

            print("\nRESULT: FAIL")

            failed_tests += 1

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print("\n" + "=" * 70)
    print("END-TO-END VALIDATION SUMMARY")
    print("=" * 70)

    print(
        f"\nTests passed : "
        f"{passed_tests}"
    )

    print(
        f"Tests failed : "
        f"{failed_tests}"
    )

    print(
        f"Tests total  : "
        f"{total_tests}"
    )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    if failed_tests == 0:

        print("\n" + "=" * 70)
        print(
            "ALL END-TO-END DIAGNOSIS TESTS PASSED"
        )
        print("=" * 70)

        print(
            "\nThe complete pipeline successfully handles:"
        )

        print(
            "  ✓ Blight"
        )

        print(
            "  ✓ Common Rust"
        )

        print(
            "  ✓ Gray Leaf Spot"
        )

        print(
            "  ✓ Healthy"
        )

        print(
            "\nThe pipeline correctly connects:"
        )

        print(
            "  ✓ CNN prediction"
        )

        print(
            "  ✓ Decision layer"
        )

        print(
            "  ✓ Knowledge-base mapping"
        )

        print(
            "  ✓ SQLite disease profile"
        )

        print(
            "  ✓ User-facing diagnosis data"
        )

    else:

        print("\n" + "=" * 70)
        print(
            "END-TO-END DIAGNOSIS VALIDATION FAILED"
        )
        print("=" * 70)

        sys.exit(1)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()