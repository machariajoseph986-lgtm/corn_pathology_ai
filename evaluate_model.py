import os
import json
import numpy as np
import tensorflow as tf

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

import matplotlib.pyplot as plt


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

TEST_DIR = os.path.join(
    PROJECT_DIR,
    "dataset_split",
    "test"
)

MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "training_output",
    "best_maize_disease_cnn.keras"
)

RESULTS_DIR = os.path.join(
    PROJECT_DIR,
    "results"
)

os.makedirs(RESULTS_DIR, exist_ok=True)


# Class order must match the order used during training
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
print("MAIZE DISEASE CNN MODEL EVALUATION")
print("=" * 60)

print("\nModel:")
print(f"  {MODEL_PATH}")

print("\nTest dataset:")
print(f"  {TEST_DIR}")


# ============================================================
# CHECK REQUIRED FILES
# ============================================================

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"\nERROR: Best model not found:\n{MODEL_PATH}"
    )

if not os.path.exists(TEST_DIR):
    raise FileNotFoundError(
        f"\nERROR: Test dataset not found:\n{TEST_DIR}"
    )


# ============================================================
# LOAD TEST DATASET
# ============================================================

print("\n" + "-" * 60)
print("LOADING TEST DATASET")
print("-" * 60)

test_ds = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    class_names=CLASS_NAMES,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)
normalization = tf.keras.layers.Rescaling(1.0 / 255)

test_ds = test_ds.map(
    lambda images, labels: (normalization(images), labels),
    num_parallel_calls=tf.data.AUTOTUNE
)

test_ds = test_ds.prefetch(tf.data.AUTOTUNE)

print("\nClasses:")
for index, class_name in enumerate(CLASS_NAMES):
    print(f"  {index}: {class_name}")


# ============================================================
# LOAD TRAINED MODEL
# ============================================================

print("\n" + "-" * 60)
print("LOADING BEST CNN MODEL")
print("-" * 60)

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully.")


# ============================================================
# MODEL EVALUATION
# ============================================================

print("\n" + "-" * 60)
print("EVALUATING ON TEST SET")
print("-" * 60)

test_loss, test_accuracy = model.evaluate(
    test_ds,
    verbose=1
)

print("\nTest Results:")
print(f"  Test Loss     : {test_loss:.4f}")
print(f"  Test Accuracy : {test_accuracy:.4f}")
print(f"  Test Accuracy : {test_accuracy * 100:.2f}%")


# ============================================================
# GET TRUE LABELS
# ============================================================

print("\n" + "-" * 60)
print("GENERATING PREDICTIONS")
print("-" * 60)

y_true = np.concatenate(
    [labels.numpy() for _, labels in test_ds],
    axis=0
)

predictions = model.predict(
    test_ds,
    verbose=1
)

y_pred = np.argmax(
    predictions,
    axis=1
)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print("\n" + "-" * 60)
print("CLASSIFICATION REPORT")
print("-" * 60)

report = classification_report(
    y_true,
    y_pred,
    target_names=CLASS_NAMES,
    digits=4
)

print(report)


report_path = os.path.join(
    RESULTS_DIR,
    "classification_report.txt"
)

with open(report_path, "w") as file:
    file.write(report)

print(f"Classification report saved to:")
print(f"  {report_path}")


# ============================================================
# CONFUSION MATRIX
# ============================================================

print("\n" + "-" * 60)
print("CONFUSION MATRIX")
print("-" * 60)

cm = confusion_matrix(
    y_true,
    y_pred
)

print("\nConfusion Matrix:")
print(cm)


plt.figure(figsize=(8, 7))

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=CLASS_NAMES
)

display.plot(
    cmap="Blues",
    xticks_rotation=45,
    values_format="d"
)

plt.title(
    "Maize Disease CNN - Test Confusion Matrix"
)

plt.tight_layout()

confusion_matrix_path = os.path.join(
    RESULTS_DIR,
    "confusion_matrix.png"
)

plt.savefig(
    confusion_matrix_path,
    dpi=200,
    bbox_inches="tight"
)

plt.show()

print(f"Confusion matrix saved to:")
print(f"  {confusion_matrix_path}")


# ============================================================
# SAVE EVALUATION SUMMARY
# ============================================================

summary = {
    "model": "best_maize_disease_cnn.keras",
    "test_images": int(len(y_true)),
    "test_loss": float(test_loss),
    "test_accuracy": float(test_accuracy),
    "test_accuracy_percentage": float(test_accuracy * 100),
    "classes": CLASS_NAMES,
    "confusion_matrix": cm.tolist()
}

summary_path = os.path.join(
    RESULTS_DIR,
    "evaluation_summary.json"
)

with open(summary_path, "w") as file:
    json.dump(
        summary,
        file,
        indent=4
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("MODEL EVALUATION COMPLETE")
print("=" * 60)

print(f"""
Test images       : {len(y_true)}
Test accuracy     : {test_accuracy * 100:.2f}%
Test loss         : {test_loss:.4f}

Results saved in:
  {RESULTS_DIR}

Files created:
  - classification_report.txt
  - confusion_matrix.png
  - evaluation_summary.json
""")

print("=" * 60)