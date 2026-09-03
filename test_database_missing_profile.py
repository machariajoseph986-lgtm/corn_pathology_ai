from knowledge_base.database import get_disease_profile


print("=" * 70)
print("KNOWLEDGE BASE MISSING-PROFILE VALIDATION")
print("=" * 70)


# ============================================================
# TEST NONEXISTENT HEALTH-PROBLEM ID
# ============================================================

missing_id = "HP_DOES_NOT_EXIST"


print("\nTesting nonexistent health-problem ID:")
print(f"  {missing_id}")


print("\nRunning database lookup...")


try:

    result = get_disease_profile(
        missing_id
    )


    # --------------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------------

    print("\nActual result:")
    print(f"  Returned value : {result}")


    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    print("\nValidation:")


    if result is None:

        print(
            "  Missing profile handling : PASS"
        )

        print(
            "\n" + "=" * 70
        )

        print(
            "MISSING-PROFILE VALIDATION PASSED"
        )

        print(
            "=" * 70
        )


    else:

        print(
            "  Missing profile handling : FAIL"
        )

        print(
            "\nERROR: A nonexistent disease ID "
            "returned a profile."
        )

        print(
            "=" * 70
        )

        raise SystemExit(1)


except Exception as error:

    print(
        "\n" + "=" * 70
    )

    print(
        "MISSING-PROFILE VALIDATION FAILED"
    )

    print(
        "=" * 70
    )

    print("\nError:")
    print(error)

    raise SystemExit(1)