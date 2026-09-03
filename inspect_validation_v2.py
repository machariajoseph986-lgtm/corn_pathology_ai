import os
import numpy as np
import tensorflow as tf

from sklearn.metrics import classification_report, confusion_matrix


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
    "v2",
    "best_maize_disease_cnn_v2.keras"
)

CLASS_NAMES = [
    "Blight",
    "Common_Rust",
    "Gray_Leaf_Spot",
    "Healthy"
]

IMG_SIZE = (320, 320)

BATCH_SIZE = 32


# ============================================================
# HEADER
# ============================================================

print("=" * 60)
print("MAIZE DISEASE CNN V2 VALIDATION EVALUATION")
print("=" * 60)

print("\nValidation dataset:")
print(f"  {VALIDATION_DIR}")

print("\nModel:")
print(f"  {MODEL_PATH}")


# ============================================================
# CHECK FILES
# ============================================================

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"\nV2 model not found:\n{MODEL_PATH}"
    )

if not os.path.exists(VALIDATION_DIR):
    raise FileNotFoundError(
        f"\nValidation dataset not found:\n{VALIDATION_DIR}"
    )


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

print("\n" + "-" * 60)
print("LOADING V2 MODEL")
print("-" * 60)

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully.")


# ============================================================
# GENERATE PREDICTIONS
# ============================================================

print("\n" + "-" * 60)
print("GENERATING VALIDATION PREDICTIONS")
print("-" * 60)

y_true = np.concatenate([
    labels.numpy()
    for images, labels in validation_ds
])

predictions = model.predict(validation_ds)

y_pred = np.argmax(predictions, axis=1)


# ============================================================
# CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_true,
    y_pred
)

print("\n" + "=" * 60)
print("V2 VALIDATION CONFUSION MATRIX")
print("=" * 60)

print("\nRows = Actual")
print("Columns = Predicted\n")

header = f"{'':20}"

for name in CLASS_NAMES:
    header += f"{name:18}"

print(header)

for i, row in enumerate(cm):

    line = f"{CLASS_NAMES[i]:20}"

    for value in row:
        line += f"{value:<18}"

    print(line)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print("\n" + "=" * 60)
print("V2 CLASSIFICATION REPORT")
print("=" * 60)

report = classification_report(
    y_true,
    y_pred,
    target_names=CLASS_NAMES,
    digits=4
)

print(report)


# ============================================================
# BLIGHT ↔ GRAY LEAF SPOT ANALYSIS
# ============================================================

blight_index = CLASS_NAMES.index("Blight")
gray_index = CLASS_NAMES.index("Gray_Leaf_Spot")

blight_to_gray = cm[
    blight_index,
    gray_index
]

gray_to_blight = cm[
    gray_index,
    blight_index
]

total_confusion = (
    blight_to_gray +
    gray_to_blight
)

print("=" * 60)
print("BLIGHT ↔ GRAY LEAF SPOT ANALYSIS")
print("=" * 60)

print()

print(
    f"Blight → Gray Leaf Spot : {blight_to_gray}"
)

print(
    f"Gray Leaf Spot → Blight : {gray_to_blight}"
)

print(
    f"Total two-way confusion : {total_confusion}"
)

print()

print("=" * 60)
print("V2 VALIDATION EVALUATION COMPLETE")
print("=" * 60)