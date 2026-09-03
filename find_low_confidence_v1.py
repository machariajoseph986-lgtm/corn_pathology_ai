"""
V1 CNN — LOW CONFIDENCE IMAGE FINDER

Finds test images where the V1 CNN prediction confidence
is below the selected 70% diagnostic threshold.

Purpose:
    Identify a real image that can be used to validate
    the UNCERTAIN decision state in cnn/predictor.py.
"""

import os
import numpy as np
import tensorflow as tf


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "training_output",
    "best_maize_disease_cnn.keras"
)

TEST_DIR = os.path.join(
    PROJECT_DIR,
    "dataset_split",
    "test"
)

IMAGE_SIZE = (256, 256)

CONFIDENCE_THRESHOLD = 0.70

CLASS_NAMES = [
    "Blight",
    "Common_Rust",
    "Gray_Leaf_Spot",
    "Healthy"
]


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("V1 CNN LOW-CONFIDENCE IMAGE FINDER")
print("=" * 70)

print("\nModel:")
print(f"  {MODEL_PATH}")

print("\nTest dataset:")
print(f"  {TEST_DIR}")

print(
    f"\nTarget confidence threshold: "
    f"{CONFIDENCE_THRESHOLD * 100:.0f}%"
)


# ============================================================
# CHECK PATHS
# ============================================================

if not os.path.exists(MODEL_PATH):

    raise FileNotFoundError(
        f"\nV1 model not found:\n{MODEL_PATH}"
    )

if not os.path.exists(TEST_DIR):

    raise FileNotFoundError(
        f"\nTest dataset not found:\n{TEST_DIR}"
    )


# ============================================================
# LOAD MODEL
# ============================================================

print("\n" + "-" * 70)
print("LOADING V1 CNN MODEL")
print("-" * 70)

model = tf.keras.models.load_model(
    MODEL_PATH
)

print("V1 model loaded successfully.")


# ============================================================
# FIND TEST IMAGES
# ============================================================

print("\n" + "-" * 70)
print("FINDING TEST IMAGES")
print("-" * 70)

image_extensions = (
    ".jpg",
    ".jpeg",
    ".png",
    ".JPG",
    ".JPEG",
    ".PNG"
)

image_paths = []

for class_name in CLASS_NAMES:

    class_dir = os.path.join(
        TEST_DIR,
        class_name
    )

    if not os.path.exists(class_dir):
        continue

    for filename in os.listdir(class_dir):

        if filename.endswith(image_extensions):

            image_paths.append(
                os.path.join(
                    class_dir,
                    filename
                )
            )


print(
    f"Images found: {len(image_paths)}"
)


# ============================================================
# ANALYZE IMAGES
# ============================================================

print("\n" + "-" * 70)
print("ANALYZING PREDICTIONS")
print("-" * 70)

low_confidence_results = []

correct_low_confidence = []
incorrect_low_confidence = []


for image_path in image_paths:

    # --------------------------------------------------------
    # LOAD IMAGE
    # --------------------------------------------------------

    image = tf.keras.utils.load_img(
        image_path,
        target_size=IMAGE_SIZE
    )

    image_array = tf.keras.utils.img_to_array(
        image
    )

    image_array = image_array / 255.0

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    # --------------------------------------------------------
    # PREDICT
    # --------------------------------------------------------

    predictions = model.predict(
        image_array,
        verbose=0
    )

    probabilities = predictions[0]

    predicted_index = int(
        np.argmax(probabilities)
    )

    confidence = float(
        probabilities[predicted_index]
    )

    predicted_class = CLASS_NAMES[
        predicted_index
    ]

    # --------------------------------------------------------
    # ACTUAL CLASS
    # --------------------------------------------------------

    actual_class = os.path.basename(
        os.path.dirname(image_path)
    )

    # --------------------------------------------------------
    # KEEP ONLY LOW-CONFIDENCE RESULTS
    # --------------------------------------------------------

    if confidence < CONFIDENCE_THRESHOLD:

        result = {

            "image_path": image_path,

            "actual_class": actual_class,

            "predicted_class": predicted_class,

            "confidence": confidence,

            "correct": (
                actual_class == predicted_class
            )
        }

        low_confidence_results.append(
            result
        )

        if result["correct"]:

            correct_low_confidence.append(
                result
            )

        else:

            incorrect_low_confidence.append(
                result
            )


# ============================================================
# SORT RESULTS
# ============================================================

low_confidence_results.sort(
    key=lambda x: x["confidence"]
)

correct_low_confidence.sort(
    key=lambda x: x["confidence"]
)

incorrect_low_confidence.sort(
    key=lambda x: x["confidence"]
)


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("LOW-CONFIDENCE SUMMARY")
print("=" * 70)

print(
    f"\nImages below "
    f"{CONFIDENCE_THRESHOLD * 100:.0f}% confidence:"
    f" {len(low_confidence_results)}"
)

print(
    f"Correct low-confidence predictions:"
    f" {len(correct_low_confidence)}"
)

print(
    f"Incorrect low-confidence predictions:"
    f" {len(incorrect_low_confidence)}"
)


# ============================================================
# SHOW LOW-CONFIDENCE RESULTS
# ============================================================

print("\n" + "-" * 70)
print("LOW-CONFIDENCE IMAGES")
print("-" * 70)

for result in low_confidence_results[:20]:

    status = (
        "CORRECT"
        if result["correct"]
        else "INCORRECT"
    )

    print("\n" + status)

    print(
        f"  Actual     : "
        f"{result['actual_class']}"
    )

    print(
        f"  Predicted  : "
        f"{result['predicted_class']}"
    )

    print(
        f"  Confidence : "
        f"{result['confidence'] * 100:.2f}%"
    )

    print(
        f"  Image      : "
        f"{result['image_path']}"
    )


# ============================================================
# BEST IMAGE FOR VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("RECOMMENDED VALIDATION IMAGE")
print("=" * 70)

if low_confidence_results:

    recommended = low_confidence_results[0]

    print(
        "\nUse this image to test the "
        "UNCERTAIN state:"
    )

    print(
        f"\nActual class:"
        f" {recommended['actual_class']}"
    )

    print(
        f"Predicted class:"
        f" {recommended['predicted_class']}"
    )

    print(
        f"Confidence:"
        f" {recommended['confidence'] * 100:.2f}%"
    )

    print(
        "\nImage:"
    )

    print(
        f"  {recommended['image_path']}"
    )

    print(
        "\nExpected predictor status:"
        " UNCERTAIN"
    )

else:

    print(
        "\nNo images below the 70% threshold "
        "were found."
    )


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 70)
print("LOW-CONFIDENCE ANALYSIS COMPLETE")
print("=" * 70)