import sys
import os


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)


# ============================================================
# IMPORT EXISTING PROJECT COMPONENTS
# ============================================================

from cnn.database_integration import diagnose_from_image


# ============================================================
# DISPLAY DIAGNOSIS
# ============================================================

def display_diagnosis(result):
    """
    Convert the structured CNN + knowledge-base result
    into a user-friendly diagnosis.
    """

    print("\n" + "=" * 70)
    print("PLANT HEALTH RESULT")
    print("=" * 70)

    # --------------------------------------------------------
    # DIAGNOSIS
    # --------------------------------------------------------

    print("\nDiagnosis")
    print("-" * 70)

    class_name = result["class_name"]
    confidence = result["confidence"]
    confidence_status = result["confidence_status"]

    readable_class = class_name.replace(
        "_", " "
    ).lower()

    # --------------------------------------------------------
    # HEALTHY CASE
    # --------------------------------------------------------

    if result["is_healthy"]:

        print(
            "The image appears to show a healthy maize plant."
        )

        print(
            f"\nConfidence: {confidence:.2%}"
        )

        print(
            "\nNo disease was identified from the image."
        )

        print("\nNote")
        print("-" * 70)

        print(
            "This result is based on the image provided. "
            "Continue normal field monitoring for any changes "
            "in plant health."
        )

        print("\n" + "=" * 70)
        print("DIAGNOSIS COMPLETE")
        print("=" * 70)

        return

    # --------------------------------------------------------
    # ACCEPTED DIAGNOSIS
    # --------------------------------------------------------

    if confidence_status == "accepted":

        print(
            f"The image is most consistent with "
            f"maize {readable_class}."
        )

        print(
            f"\nConfidence: {confidence:.2%}"
        )

        print(
            "\nThe system is reasonably confident in this result."
        )

    # --------------------------------------------------------
    # UNCERTAIN DIAGNOSIS
    # --------------------------------------------------------

    else:

        print(
            f"The image may show "
            f"maize {readable_class}, "
            "but the system is uncertain."
        )

        print(
            f"\nConfidence: {confidence:.2%}"
        )

        print(
            "\nPlease treat this result as an indication "
            "rather than a confirmed diagnosis."
        )

    # --------------------------------------------------------
    # DIAGNOSTIC CAUTION
    # --------------------------------------------------------

    if result["caution_required"]:

        print("\nImportant note")
        print("-" * 70)

        print(
            "Blight and Gray Leaf Spot can have similar "
            "visual symptoms."
        )

        print(
            "For an important farming or treatment decision, "
            "consider additional field observations or "
            "confirmation from an agricultural expert."
        )

    # --------------------------------------------------------
    # DATABASE PROFILE
    # --------------------------------------------------------

    profile = result["disease_profile"]

    if profile is None:

        print("\nImportant note")
        print("-" * 70)

        print(
            "The system identified a possible disease, but "
            "additional disease information is currently "
            "unavailable."
        )

        print("\n" + "=" * 70)
        print("DIAGNOSIS COMPLETE")
        print("=" * 70)

        return

    # --------------------------------------------------------
    # DISEASE INFORMATION
    # --------------------------------------------------------

    print("\nDisease information")
    print("-" * 70)

    print(
        f"Disease : {profile['disease']}"
    )

    print(
        f"Crop    : {profile['crop']}"
    )

    print(
        f"Type    : {profile['type'].capitalize()}"
    )

    # --------------------------------------------------------
    # PATHOGENS
    # --------------------------------------------------------

    if profile["pathogens"]:

        print("\nCause / Pathogen")
        print("-" * 70)

        for pathogen in profile["pathogens"]:

            scientific_name = pathogen.get(
                "scientific_name",
                ""
            )

            pathogen_type = pathogen.get(
                "type",
                ""
            )

            role = pathogen.get(
                "role",
                ""
            )

            text = scientific_name

            if pathogen_type:
                text += f" ({pathogen_type})"

            if role:
                text += f": {role}"

            print(f"- {text}")

    # --------------------------------------------------------
    # SYMPTOMS
    # --------------------------------------------------------

    if profile["symptoms"]:

        print("\nSymptoms")
        print("-" * 70)

        for symptom in profile["symptoms"]:

            category = symptom.get(
                "category",
                ""
            )

            description = symptom.get(
                "description",
                ""
            )

            if category:
                print(
                    f"- [{category}] {description}"
                )

            else:
                print(
                    f"- {description}"
                )

    # --------------------------------------------------------
    # TRANSMISSION
    # --------------------------------------------------------

    if profile["transmission"]:

        print("\nTransmission")
        print("-" * 70)

        for item in profile["transmission"]:

            method = item.get(
                "method",
                ""
            )

            description = item.get(
                "description",
                ""
            )

            print(
                f"- {method}: {description}"
            )

    # --------------------------------------------------------
    # FAVOURABLE CONDITIONS
    # --------------------------------------------------------

    if profile["conditions"]:

        print("\nFavourable conditions")
        print("-" * 70)

        for condition in profile["conditions"]:

            factor = condition.get(
                "factor",
                ""
            )

            value = condition.get(
                "value",
                ""
            )

            description = condition.get(
                "description",
                ""
            )

            text = factor

            if value:
                text += f" ({value})"

            if description:
                text += f": {description}"

            print(
                f"- {text}"
            )

    # --------------------------------------------------------
    # MANAGEMENT
    # --------------------------------------------------------

    if profile["management"]:

        print("\nManagement")
        print("-" * 70)

        for item in profile["management"]:

            category = item.get(
                "category",
                ""
            )

            action = item.get(
                "action",
                ""
            )

            if category:
                print(
                    f"- [{category}] {action}"
                )

            else:
                print(
                    f"- {action}"
                )

    # --------------------------------------------------------
    # SOURCES
    # --------------------------------------------------------

    if profile["sources"]:

        print("\nSources")
        print("-" * 70)

        for source in profile["sources"]:

            organization = source.get(
                "organization",
                ""
            )

            title = source.get(
                "title",
                ""
            )

            url = source.get(
                "url",
                ""
            )

            text = ""

            if organization:
                text += organization

            if title:
                text += f": {title}"

            if text:
                print(f"- {text}")

            if url:
                print(f"  {url}")

    # --------------------------------------------------------
    # END
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("DIAGNOSIS COMPLETE")
    print("=" * 70)


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("=" * 70)
    print("PLANT HEALTH AI")
    print("=" * 70)

    print("\nCNN + Knowledge Base Diagnosis System")

    # --------------------------------------------------------
    # CHECK IMAGE ARGUMENT
    # --------------------------------------------------------

    if len(sys.argv) != 2:

        print("\nUsage:")

        print(
            'python diagnose.py "path/to/image.jpg"'
        )

        sys.exit(1)

    image_path = sys.argv[1]

    # --------------------------------------------------------
    # CHECK IMAGE EXISTS
    # --------------------------------------------------------

    if not os.path.exists(image_path):

        print("\nERROR: Image not found:")

        print(image_path)

        sys.exit(1)

    # --------------------------------------------------------
    # RUN COMPLETE PIPELINE
    # --------------------------------------------------------

    print("\nImage:")

    print(
        f"  {image_path}"
    )

    print(
        "\nRunning CNN diagnosis..."
    )

    try:

        result = diagnose_from_image(
            image_path
        )

        display_diagnosis(
            result
        )

    except Exception as error:

        print(
            "\n" + "=" * 70
        )

        print(
            "DIAGNOSIS FAILED"
        )

        print(
            "=" * 70
        )

        print("\nError:")

        print(error)

        sys.exit(1)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()