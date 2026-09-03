"""
Database Integration Decision-Layer Validation

Purpose:
Verify that cnn/database_integration.py preserves the
diagnostic decision information produced by cnn/predictor.py.

The test verifies:

    - confidence_status
    - caution_required
    - caution_reason
    - correct CNN class
    - correct knowledge-base ID
    - disease profile retrieval

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
# IMPORT DATABASE INTEGRATION
# ============================================================

from cnn.database_integration import (
    diagnose_from_image
)


# ============================================================
# TEST IMAGE
# ============================================================

TEST_IMAGE = os.path.join(
    PROJECT_DIR,
    "dataset_split",
    "test",
    "Common_Rust",
    "Corn_Common_Rust (1000).JPG"
)


# ============================================================
# EXPECTED RESULTS
# ============================================================

EXPECTED_CLASS = "Common_Rust"

EXPECTED_KB_ID = (
    "HP_MAIZE_COMMON_RUST"
)

EXPECTED_CONFIDENCE_STATUS = "accepted"

EXPECTED_CAUTION_REQUIRED = False

EXPECTED_CAUTION_REASON = None


# ============================================================
# TEST
# ============================================================

def main():

    print("=" * 70)
    print("DATABASE INTEGRATION DECISION-LAYER VALIDATION")
    print("=" * 70)

    print("\nPurpose:")
    print(
        "Verify that database_integration.py preserves "
        "the CNN decision information."
    )

    print("\nDecision information being tested:")

    print(
        "  - confidence_status"
    )

    print(
        "  - caution_required"
    )

    print(
        "  - caution_reason"
    )

    print("\nThe trained CNN model is NOT being modified.")
    print("The SQLite knowledge base is NOT being modified.")

    # --------------------------------------------------------
    # CHECK IMAGE
    # --------------------------------------------------------

    print("\n" + "-" * 70)
    print("TEST IMAGE")
    print("-" * 70)

    print(f"\n{TEST_IMAGE}")

    if not os.path.exists(TEST_IMAGE):

        print("\nRESULT: FAIL")
        print("Test image was not found.")

        sys.exit(1)

    # --------------------------------------------------------
    # RUN INTEGRATION
    # --------------------------------------------------------

    print("\nRunning CNN → database integration...")

    try:

        result = diagnose_from_image(
            TEST_IMAGE
        )

    except Exception as error:

        print("\n" + "-" * 70)
        print("INTEGRATION ERROR")
        print("-" * 70)

        print(f"\n{error}")

        print("\nRESULT: FAIL")

        sys.exit(1)

    # --------------------------------------------------------
    # DISPLAY ACTUAL RESULT
    # --------------------------------------------------------

    print("\n" + "-" * 70)
    print("ACTUAL INTEGRATION RESULT")
    print("-" * 70)

    print(
        f"\nClass              : "
        f"{result['class_name']}"
    )

    print(
        f"Confidence         : "
        f"{result['confidence']:.2%}"
    )

    print(
        f"Confidence status   : "
        f"{result['confidence_status']}"
    )

    print(
        f"Caution required   : "
        f"{result['caution_required']}"
    )

    print(
        f"Caution reason     : "
        f"{result['caution_reason']}"
    )

    print(
        f"Knowledge Base ID  : "
        f"{result['health_problem_id']}"
    )

    print(
        f"Disease profile    : "
        f"{'FOUND' if result['disease_profile'] else 'NOT FOUND'}"
    )

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    print("\n" + "-" * 70)
    print("VALIDATION")
    print("-" * 70)

    tests_passed = 0
    tests_failed = 0

    # --------------------------------------------------------
    # TEST 1: CLASS
    # --------------------------------------------------------

    if result["class_name"] == EXPECTED_CLASS:

        print("\nClass mapping       : PASS")

        tests_passed += 1

    else:

        print(
            "\nClass mapping       : FAIL"
        )

        print(
            f"  Expected: {EXPECTED_CLASS}"
        )

        print(
            f"  Actual  : {result['class_name']}"
        )

        tests_failed += 1

    # --------------------------------------------------------
    # TEST 2: CONFIDENCE STATUS
    # --------------------------------------------------------

    if (
        result["confidence_status"]
        == EXPECTED_CONFIDENCE_STATUS
    ):

        print(
            "Confidence status   : PASS"
        )

        tests_passed += 1

    else:

        print(
            "Confidence status   : FAIL"
        )

        print(
            f"  Expected: "
            f"{EXPECTED_CONFIDENCE_STATUS}"
        )

        print(
            f"  Actual  : "
            f"{result['confidence_status']}"
        )

        tests_failed += 1

    # --------------------------------------------------------
    # TEST 3: CAUTION REQUIRED
    # --------------------------------------------------------

    if (
        result["caution_required"]
        == EXPECTED_CAUTION_REQUIRED
    ):

        print(
            "Caution required    : PASS"
        )

        tests_passed += 1

    else:

        print(
            "Caution required    : FAIL"
        )

        print(
            f"  Expected: "
            f"{EXPECTED_CAUTION_REQUIRED}"
        )

        print(
            f"  Actual  : "
            f"{result['caution_required']}"
        )

        tests_failed += 1

    # --------------------------------------------------------
    # TEST 4: CAUTION REASON
    # --------------------------------------------------------

    if (
        result["caution_reason"]
        == EXPECTED_CAUTION_REASON
    ):

        print(
            "Caution reason      : PASS"
        )

        tests_passed += 1

    else:

        print(
            "Caution reason      : FAIL"
        )

        print(
            f"  Expected: "
            f"{EXPECTED_CAUTION_REASON}"
        )

        print(
            f"  Actual  : "
            f"{result['caution_reason']}"
        )

        tests_failed += 1

    # --------------------------------------------------------
    # TEST 5: KNOWLEDGE BASE MAPPING
    # --------------------------------------------------------

    if (
        result["health_problem_id"]
        == EXPECTED_KB_ID
    ):

        print(
            "Knowledge-base ID   : PASS"
        )

        tests_passed += 1

    else:

        print(
            "Knowledge-base ID   : FAIL"
        )

        print(
            f"  Expected: "
            f"{EXPECTED_KB_ID}"
        )

        print(
            f"  Actual  : "
            f"{result['health_problem_id']}"
        )

        tests_failed += 1

    # --------------------------------------------------------
    # TEST 6: DISEASE PROFILE
    # --------------------------------------------------------

    profile = result[
        "disease_profile"
    ]

    if profile is not None:

        print(
            "Disease profile     : PASS"
        )

        tests_passed += 1

    else:

        print(
            "Disease profile     : FAIL"
        )

        tests_failed += 1

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    total_tests = (
        tests_passed
        + tests_failed
    )

    print("\n" + "=" * 70)
    print("INTEGRATION DECISION-LAYER SUMMARY")
    print("=" * 70)

    print(
        f"\nTests passed : "
        f"{tests_passed}"
    )

    print(
        f"Tests failed : "
        f"{tests_failed}"
    )

    print(
        f"Tests total  : "
        f"{total_tests}"
    )

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    if tests_failed == 0:

        print("\n" + "=" * 70)
        print(
            "ALL DATABASE INTEGRATION "
            "DECISION TESTS PASSED"
        )
        print("=" * 70)

        print(
            "\nThe integration layer correctly preserves:"
        )

        print(
            "  ✓ Confidence status"
        )

        print(
            "  ✓ Caution required"
        )

        print(
            "  ✓ Caution reason"
        )

        print(
            "\nIt also correctly preserves:"
        )

        print(
            "  ✓ CNN class"
        )

        print(
            "  ✓ Knowledge-base mapping"
        )

        print(
            "  ✓ Disease profile"
        )

    else:

        print("\n" + "=" * 70)
        print(
            "DATABASE INTEGRATION "
            "DECISION TESTS FAILED"
        )
        print("=" * 70)

        sys.exit(1)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()