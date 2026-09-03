"""
CNN 9-Image Validation Test

Tests three randomly selected images from each CNN-supported
maize disease class using a fixed random seed.

The test validates:

    Test image
        ↓
    CNN predictor
        ↓
    CNN class
        ↓
    CNN → Knowledge Base mapping
        ↓
    Knowledge Base ID

Classes tested:

    Blight
    Common_Rust
    Gray_Leaf_Spot
"""

import os
import random

from predictor import predict_image


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

TEST_DIR = os.path.join(
    PROJECT_DIR,
    "dataset_split",
    "test"
)

CLASSES = [
    "Blight",
    "Common_Rust",
    "Gray_Leaf_Spot"
]

IMAGES_PER_CLASS = 3

RANDOM_SEED = 42

SUPPORTED_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
)


# ============================================================
# SELECT TEST IMAGES
# ============================================================

def select_test_images():

    random.seed(RANDOM_SEED)

    selected_images = []

    for class_name in CLASSES:

        class_dir = os.path.join(
            TEST_DIR,
            class_name
        )

        if not os.path.isdir(class_dir):
            raise FileNotFoundError(
                f"Test class directory not found:\n{class_dir}"
            )

        images = [
            os.path.join(class_dir, filename)
            for filename in os.listdir(class_dir)
            if filename.lower().endswith(
                SUPPORTED_EXTENSIONS
            )
        ]

        images.sort()

        if len(images) < IMAGES_PER_CLASS:
            raise ValueError(
                f"Not enough images in {class_name}. "
                f"Found {len(images)}, "
                f"need {IMAGES_PER_CLASS}."
            )

        selected = random.sample(
            images,
            IMAGES_PER_CLASS
        )

        selected_images.extend(
            (class_name, image_path)
            for image_path in selected
        )

    return selected_images


# ============================================================
# RUN VALIDATION
# ============================================================

def run_validation():

    print("=" * 80)
    print("CNN 9-IMAGE VALIDATION TEST")
    print("=" * 80)

    print("\nTest dataset:")
    print(f"  {TEST_DIR}")

    print("\nSelection:")
    print(f"  Images per class : {IMAGES_PER_CLASS}")
    print(f"  Random seed      : {RANDOM_SEED}")

    selected_images = select_test_images()

    results = []

    print("\n" + "-" * 80)
    print(
        f"{'Actual':<20}"
        f"{'Predicted':<20}"
        f"{'Confidence':<14}"
        f"{'Knowledge Base ID':<30}"
        f"{'Result':<8}"
    )
    print("-" * 80)

    for actual_class, image_path in selected_images:

        result = predict_image(
            image_path
        )

        predicted_class = result[
            "class_name"
        ]

        confidence = result[
            "confidence"
        ]

        health_problem_id = result[
            "health_problem_id"
        ]

        passed = (
            predicted_class == actual_class
        )

        status = (
            "PASS"
            if passed
            else "FAIL"
        )

        print(
            f"{actual_class:<20}"
            f"{predicted_class:<20}"
            f"{confidence * 100:>8.2f}%     "
            f"{str(health_problem_id):<30}"
            f"{status:<8}"
        )

        results.append({
            "actual": actual_class,
            "predicted": predicted_class,
            "confidence": confidence,
            "health_problem_id": health_problem_id,
            "passed": passed,
            "image_path": image_path
        })

    # ========================================================
    # SUMMARY
    # ========================================================

    total = len(results)

    correct = sum(
        result["passed"]
        for result in results
    )

    incorrect = total - correct

    accuracy = (
        correct / total * 100
        if total > 0
        else 0
    )

    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)

    print(f"\nImages tested : {total}")
    print(f"Correct       : {correct}")
    print(f"Incorrect     : {incorrect}")
    print(f"Accuracy      : {accuracy:.2f}%")

    print("\n" + "-" * 80)
    print("SELECTED IMAGES")
    print("-" * 80)

    for result in results:

        print(
            f"\nActual class : {result['actual']}"
        )

        print(
            f"Image        : {result['image_path']}"
        )

        print(
            f"Prediction   : {result['predicted']}"
        )

        print(
            f"Confidence   : "
            f"{result['confidence'] * 100:.2f}%"
        )

        print(
            f"KB ID        : "
            f"{result['health_problem_id']}"
        )

    print("\n" + "=" * 80)

    if incorrect == 0:
        print(
            "ALL 9 PREDICTIONS MATCHED THEIR ACTUAL CLASSES."
        )
    else:
        print(
            f"{incorrect} PREDICTION(S) DID NOT MATCH "
            "THEIR ACTUAL CLASS."
        )

    print("=" * 80)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    run_validation()

