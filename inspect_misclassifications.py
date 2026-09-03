import os
import shutil
import csv
import numpy as np
import tensorflow as tf


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

VALIDATION_DIR = os.path.join(
    PROJECT_DIR,
    "dataset_split",
    "validation"
)

MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "training_output",
    "best_maize_disease_cnn.keras"
)

OUTPUT_DIR = os.path.join(
    PROJECT_DIR,
    "results",
    "misclassifications"
)

BLIGHT_TO_GLS_DIR = os.path.join(
    OUTPUT_DIR,
    "Blight_to_Gray_Leaf_Spot"
)

GLS_TO_BLIGHT_DIR = os.path.join(
    OUTPUT_DIR,
    "Gray_Leaf_Spot_to_Blight"
)

CLASS_NAMES = [
    "Blight",
    "Common_Rust",
    "Gray_Leaf_Spot",
    "Healthy"
]

IMG_SIZE = (256, 256)
BATCH_SIZE = 32


# ============================================================
# CREATE OUTPUT DIRECTORIES
# ============================================================

os.makedirs(BLIGHT_TO_GLS_DIR, exist_ok=True)
os.makedirs(GLS_TO_BLIGHT_DIR, exist_ok=True)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("CNN MISCLASSIFICATION DIAGNOSTIC")
print("=" * 70)

print("\nTarget confusion:")
print("  Blight → Gray Leaf Spot")
print("  Gray Leaf Spot → Blight")

print("\nValidation dataset:")
print(f"  {VALIDATION_DIR}")

print("\nOutput directory:")
print(f"  {OUTPUT_DIR}")


# ============================================================
# LOAD VALIDATION DATASET
# ============================================================

print("\n" + "-" * 70)
print("LOADING VALIDATION DATASET")
print("-" * 70)

validation_ds = tf.keras.utils.image_dataset_from_directory(
    VALIDATION_DIR,
    class_names=CLASS_NAMES,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

normalization = tf.keras.layers.Rescaling(1.0 / 255)

validation_ds = validation_ds.map(
    lambda images, labels: (
        normalization(images),
        labels
    ),
    num_parallel_calls=tf.data.AUTOTUNE
)

validation_ds = validation_ds.prefetch(tf.data.AUTOTUNE)


# ============================================================
# LOAD MODEL
# ============================================================

print("\n" + "-" * 70)
print("LOADING BEST CNN MODEL")
print("-" * 70)

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully.")


# ============================================================
# GENERATE PREDICTIONS
# ============================================================

print("\n" + "-" * 70)
print("GENERATING VALIDATION PREDICTIONS")
print("-" * 70)

predictions = model.predict(
    validation_ds,
    verbose=1
)

y_pred = np.argmax(
    predictions,
    axis=1
)

y_true = np.concatenate(
    [
        labels.numpy()
        for _, labels in validation_ds
    ],
    axis=0
)


# ============================================================
# GET IMAGE PATHS IN THE SAME ORDER
# ============================================================

image_paths = []

for class_name in CLASS_NAMES:

    class_dir = os.path.join(
        VALIDATION_DIR,
        class_name
    )

    for filename in sorted(os.listdir(class_dir)):

        file_path = os.path.join(
            class_dir,
            filename
        )

        if os.path.isfile(file_path):
            image_paths.append(file_path)


if len(image_paths) != len(y_true):

    raise RuntimeError(
        "\nERROR: Number of image paths does not match "
        "number of validation labels."
    )


# ============================================================
# IDENTIFY TARGET MISCLASSIFICATIONS
# ============================================================

BLIGHT = CLASS_NAMES.index("Blight")
GLS = CLASS_NAMES.index("Gray_Leaf_Spot")

blight_to_gls = []
gls_to_blight = []


for index in range(len(y_true)):

    actual = y_true[index]
    predicted = y_pred[index]

    confidence = float(
        predictions[index][predicted]
    )

    record = {
        "index": index,
        "image_path": image_paths[index],
        "actual_class": CLASS_NAMES[actual],
        "predicted_class": CLASS_NAMES[predicted],
        "confidence": confidence
    }

    if actual == BLIGHT and predicted == GLS:

        blight_to_gls.append(record)

    elif actual == GLS and predicted == BLIGHT:

        gls_to_blight.append(record)


# ============================================================
# SAVE MISCLASSIFIED IMAGES
# ============================================================

def save_misclassifications(records, output_dir):

    for number, record in enumerate(records, start=1):

        source_path = record["image_path"]

        original_name = os.path.basename(
            source_path
        )

        destination_name = (
            f"{number:02d}_"
            f"{record['confidence'] * 100:.2f}pct_"
            f"{original_name}"
        )

        destination_path = os.path.join(
            output_dir,
            destination_name
        )

        shutil.copy2(
            source_path,
            destination_path
        )


save_misclassifications(
    blight_to_gls,
    BLIGHT_TO_GLS_DIR
)

save_misclassifications(
    gls_to_blight,
    GLS_TO_BLIGHT_DIR
)


# ============================================================
# SAVE CSV REPORT
# ============================================================

csv_path = os.path.join(
    OUTPUT_DIR,
    "misclassification_report.csv"
)

all_records = (
    [
        dict(
            record,
            confusion="Blight_to_Gray_Leaf_Spot"
        )
        for record in blight_to_gls
    ]
    +
    [
        dict(
            record,
            confusion="Gray_Leaf_Spot_to_Blight"
        )
        for record in gls_to_blight
    ]
)


with open(
    csv_path,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "confusion",
            "actual_class",
            "predicted_class",
            "confidence",
            "image_path"
        ]
    )

    writer.writeheader()

    for record in all_records:

        writer.writerow({
            "confusion": record["confusion"],
            "actual_class": record["actual_class"],
            "predicted_class": record["predicted_class"],
            "confidence": f"{record['confidence']:.6f}",
            "image_path": record["image_path"]
        })


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("MISCLASSIFICATION SUMMARY")
print("=" * 70)

print(
    f"\nBlight → Gray Leaf Spot : "
    f"{len(blight_to_gls)}"
)

print(
    f"Gray Leaf Spot → Blight : "
    f"{len(gls_to_blight)}"
)

print(
    f"Total target errors     : "
    f"{len(all_records)}"
)


# ============================================================
# CONFIDENCE SUMMARY
# ============================================================

if blight_to_gls:

    confidences = [
        r["confidence"]
        for r in blight_to_gls
    ]

    print("\nBlight → Gray Leaf Spot confidence:")

    print(
        f"  Minimum : {min(confidences) * 100:.2f}%"
    )

    print(
        f"  Maximum : {max(confidences) * 100:.2f}%"
    )

    print(
        f"  Average : {np.mean(confidences) * 100:.2f}%"
    )


if gls_to_blight:

    confidences = [
        r["confidence"]
        for r in gls_to_blight
    ]

    print("\nGray Leaf Spot → Blight confidence:")

    print(
        f"  Minimum : {min(confidences) * 100:.2f}%"
    )

    print(
        f"  Maximum : {max(confidences) * 100:.2f}%"
    )

    print(
        f"  Average : {np.mean(confidences) * 100:.2f}%"
    )


# ============================================================
# OUTPUT LOCATIONS
# ============================================================

print("\n" + "-" * 70)
print("SAVED DIAGNOSTIC FILES")
print("-" * 70)

print(
    f"\nBlight → Gray Leaf Spot images:"
    f"\n  {BLIGHT_TO_GLS_DIR}"
)

print(
    f"\nGray Leaf Spot → Blight images:"
    f"\n  {GLS_TO_BLIGHT_DIR}"
)

print(
    f"\nCSV report:"
    f"\n  {csv_path}"
)

print("\n" + "=" * 70)
print("MISCLASSIFICATION DIAGNOSTIC COMPLETE")
print("=" * 70)