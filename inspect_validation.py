import os
import numpy as np
import tensorflow as tf

from sklearn.metrics import confusion_matrix, classification_report


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

CLASS_NAMES = [
    "Blight",
    "Common_Rust",
    "Gray_Leaf_Spot",
    "Healthy"
]

IMG_SIZE = (256, 256)
BATCH_SIZE = 32


# ============================================================
# HEADER
# ============================================================

print("=" * 60)
print("MAIZE DISEASE CNN VALIDATION CONFUSION MATRIX")
print("=" * 60)

print("\nValidation dataset:")
print(f"  {VALIDATION_DIR}")

print("\nModel:")
print(f"  {MODEL_PATH}")


# ============================================================
# LOAD VALIDATION DATASET
# ============================================================

print("\n" + "-" * 60)
print("LOADING VALIDATION DATASET")
print("-" * 60)

validation_ds = tf.keras.utils.image_dataset_from_directory(
    VALIDATION_DIR,
    class_names=CLASS_NAMES,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

normalization = tf.keras.layers.Rescaling(1.0 / 255)

validation_ds = validation_ds.map(
    lambda images, labels: (normalization(images), labels),
    num_parallel_calls=tf.data.AUTOTUNE
)

validation_ds = validation_ds.prefetch(tf.data.AUTOTUNE)


# ============================================================
# LOAD MODEL
# ============================================================

print("\n" + "-" * 60)
print("LOADING BEST CNN MODEL")
print("-" * 60)

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully.")


# ============================================================
# GENERATE PREDICTIONS
# ============================================================

print("\n" + "-" * 60)
print("GENERATING VALIDATION PREDICTIONS")
print("-" * 60)

predictions = model.predict(
    validation_ds,
    verbose=1
)

y_pred = np.argmax(
    predictions,
    axis=1
)

y_true = np.concatenate(
    [labels.numpy() for _, labels in validation_ds],
    axis=0
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_true,
    y_pred,
    labels=range(len(CLASS_NAMES))
)

print("\n" + "=" * 60)
print("VALIDATION CONFUSION MATRIX")
print("=" * 60)

print("\nRows = Actual")
print("Columns = Predicted\n")

print(
    f"{'':20}"
    + "".join(
        f"{name:>18}"
        for name in CLASS_NAMES
    )
)

for i, class_name in enumerate(CLASS_NAMES):

    print(
        f"{class_name:20}"
        + "".join(
            f"{cm[i][j]:18}"
            for j in range(len(CLASS_NAMES))
        )
    )


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print("\n" + "=" * 60)
print("VALIDATION CLASSIFICATION REPORT")
print("=" * 60)

print(
    classification_report(
        y_true,
        y_pred,
        target_names=CLASS_NAMES,
        digits=4
    )
)


# ============================================================
# BLIGHT / GRAY LEAF SPOT FOCUS
# ============================================================

BLIGHT = CLASS_NAMES.index("Blight")
GRAY_LEAF_SPOT = CLASS_NAMES.index("Gray_Leaf_Spot")

blight_to_gray = cm[BLIGHT][GRAY_LEAF_SPOT]
gray_to_blight = cm[GRAY_LEAF_SPOT][BLIGHT]

print("\n" + "=" * 60)
print("BLIGHT ↔ GRAY LEAF SPOT ANALYSIS")
print("=" * 60)

print(
    f"\nBlight → Gray Leaf Spot : {blight_to_gray}"
)

print(
    f"Gray Leaf Spot → Blight : {gray_to_blight}"
)

print(
    f"Total two-way confusion : "
    f"{blight_to_gray + gray_to_blight}"
)

print("\n" + "=" * 60)
print("VALIDATION INSPECTION COMPLETE")
print("=" * 60)