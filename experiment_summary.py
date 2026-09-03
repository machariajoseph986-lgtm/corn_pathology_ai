import json
import os
from datetime import datetime


# ============================================================
# CORN PATHOLOGY AI - EXPERIMENT SUMMARY
# ============================================================

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
TRAINING_DIR = os.path.join(PROJECT_ROOT, "training_output")

CLASS_WEIGHTS_FILE = os.path.join(
    PROJECT_ROOT,
    "class_weights.json"
)

TRAINING_HISTORY_FILE = os.path.join(
    TRAINING_DIR,
    "training_history.json"
)

SUMMARY_JSON = os.path.join(
    RESULTS_DIR,
    "experiment_summary.json"
)

SUMMARY_TXT = os.path.join(
    RESULTS_DIR,
    "experiment_summary.txt"
)


# ============================================================
# PROJECT INFORMATION
# ============================================================

classes = [
    "Blight",
    "Common_Rust",
    "Gray_Leaf_Spot",
    "Healthy"
]

dataset_information = {
    "original_images": 4188,
    "removed_conflicting_duplicates": 4,
    "clean_images": 4184,
    "number_of_classes": 4,
    "classes": classes
}


# ============================================================
# CLASS DISTRIBUTION
# ============================================================

class_distribution = {
    "Blight": {
        "total": 1144,
        "train": 801,
        "validation": 171,
        "test": 172
    },
    "Common_Rust": {
        "total": 1306,
        "train": 914,
        "validation": 196,
        "test": 196
    },
    "Gray_Leaf_Spot": {
        "total": 572,
        "train": 400,
        "validation": 86,
        "test": 86
    },
    "Healthy": {
        "total": 1162,
        "train": 813,
        "validation": 175,
        "test": 174
    }
}


split_information = {
    "training": 2928,
    "validation": 628,
    "test": 628,
    "total": 4184,
    "strategy": "Stratified split"
}


# ============================================================
# PREPROCESSING
# ============================================================

preprocessing = {
    "image_size": "256x256",
    "channels": 3,
    "normalization": "Rescaling 1/255",
    "pixel_range_after_normalization": "0-1",
    "augmentation": {
        "applied_to": "Training set only",
        "validation_augmented": False,
        "test_augmented": False
    }
}


# ============================================================
# CLASS WEIGHTS
# ============================================================

class_weights = {}

if os.path.exists(CLASS_WEIGHTS_FILE):

    with open(CLASS_WEIGHTS_FILE, "r") as f:
        weights_data = json.load(f)

    class_weights = weights_data["class_weights"]

else:

    class_weights = {
        "0": 0.913858,
        "1": 0.800875,
        "2": 1.83,
        "3": 0.900369
    }


# ============================================================
# MODEL INFORMATION
# ============================================================

model_information = {
    "model_type": "Custom CNN",
    "input_size": "256x256x3",
    "number_of_classes": 4,
    "output_activation": "Softmax",
    "loss_function": "Sparse Categorical Crossentropy",
    "optimizer": "Adam",
    "class_weights_used": True
}


# ============================================================
# TRAINING RESULTS
# ============================================================

training_results = {}

if os.path.exists(TRAINING_HISTORY_FILE):

    with open(TRAINING_HISTORY_FILE, "r") as f:
        history = json.load(f)

    epochs = len(history["loss"])

    best_train_accuracy = max(history["accuracy"])
    best_validation_accuracy = max(history["val_accuracy"])

    best_validation_epoch = (
        history["val_accuracy"].index(best_validation_accuracy) + 1
    )

    training_results = {
        "epochs_completed": epochs,
        "best_training_accuracy": best_train_accuracy,
        "best_validation_accuracy": best_validation_accuracy,
        "best_validation_epoch": best_validation_epoch,
        "final_training_accuracy": history["accuracy"][-1],
        "final_validation_accuracy": history["val_accuracy"][-1],
        "final_training_loss": history["loss"][-1],
        "final_validation_loss": history["val_loss"][-1]
    }


# ============================================================
# TEST RESULTS
# ============================================================

test_results = {
    "test_images": 628,
    "test_accuracy": 0.9363,
    "test_loss": 0.1805,
    "macro_f1": 0.9232,
    "weighted_f1": 0.9369
}


per_class_results = {
    "Blight": {
        "precision": 0.9187,
        "recall": 0.8547,
        "f1_score": 0.8855
    },
    "Common_Rust": {
        "precision": 0.9844,
        "recall": 0.9643,
        "f1_score": 0.9742
    },
    "Gray_Leaf_Spot": {
        "precision": 0.7800,
        "recall": 0.9070,
        "f1_score": 0.8387
    },
    "Healthy": {
        "precision": 0.9886,
        "recall": 1.0000,
        "f1_score": 0.9943
    }
}


# ============================================================
# CONFUSION MATRIX
# ============================================================

confusion_matrix = [
    [147, 3, 20, 2],
    [5, 189, 2, 0],
    [8, 0, 78, 0],
    [0, 0, 0, 174]
]


# ============================================================
# IMPORTANT FINDINGS
# ============================================================

findings = [
    "The CNN achieved 93.63% accuracy on the independent test set.",
    "Validation accuracy reached approximately 93.95%.",
    "The best training accuracy was approximately 94.91%.",
    "Healthy achieved 100% recall on the test set.",
    "Common_Rust achieved 96.43% recall on the test set.",
    "Gray_Leaf_Spot achieved 90.70% recall on the test set.",
    "The main confusion was between Blight and Gray_Leaf_Spot.",
    "20 Blight images were classified as Gray_Leaf_Spot.",
    "Class weighting gave Gray_Leaf_Spot the highest weight because it was the minority class.",
    "Test evaluation was performed using the same 256x256 and 1/255 normalization pipeline used during training."
]


# ============================================================
# COMPLETE SUMMARY
# ============================================================

summary = {
    "project": "Corn Pathology AI",
    "generated_at": datetime.now().isoformat(),

    "dataset": dataset_information,

    "class_distribution": class_distribution,

    "split": split_information,

    "preprocessing": preprocessing,

    "class_weights": class_weights,

    "model": model_information,

    "training": training_results,

    "test_results": test_results,

    "per_class_results": per_class_results,

    "confusion_matrix": {
        "class_order": classes,
        "matrix": confusion_matrix
    },

    "findings": findings
}


# ============================================================
# CREATE RESULTS DIRECTORY
# ============================================================

os.makedirs(RESULTS_DIR, exist_ok=True)


# ============================================================
# SAVE JSON
# ============================================================

with open(SUMMARY_JSON, "w") as f:

    json.dump(
        summary,
        f,
        indent=4
    )


# ============================================================
# CREATE READABLE TEXT REPORT
# ============================================================

with open(SUMMARY_TXT, "w") as f:

    f.write("=" * 70 + "\n")
    f.write("CORN PATHOLOGY AI - EXPERIMENT SUMMARY\n")
    f.write("=" * 70 + "\n\n")

    f.write("PROJECT\n")
    f.write("-" * 70 + "\n")
    f.write("Corn Pathology AI\n\n")

    f.write("DATASET\n")
    f.write("-" * 70 + "\n")
    f.write(f"Original images: {dataset_information['original_images']}\n")
    f.write(
        f"Removed conflicting duplicates: "
        f"{dataset_information['removed_conflicting_duplicates']}\n"
    )
    f.write(f"Clean images: {dataset_information['clean_images']}\n")
    f.write(f"Classes: {', '.join(classes)}\n\n")

    f.write("DATASET SPLIT\n")
    f.write("-" * 70 + "\n")
    f.write(f"Training: {split_information['training']}\n")
    f.write(f"Validation: {split_information['validation']}\n")
    f.write(f"Test: {split_information['test']}\n")
    f.write(f"Strategy: {split_information['strategy']}\n\n")

    f.write("PREPROCESSING\n")
    f.write("-" * 70 + "\n")
    f.write("Image size: 256 x 256\n")
    f.write("Channels: 3\n")
    f.write("Normalization: 1/255\n")
    f.write("Augmentation: Training set only\n")
    f.write("Validation augmentation: No\n")
    f.write("Test augmentation: No\n\n")

    f.write("CLASS WEIGHTS\n")
    f.write("-" * 70 + "\n")

    for index, class_name in enumerate(classes):
        weight = class_weights.get(
            str(index),
            class_weights.get(index, "N/A")
        )
        f.write(
            f"{index}: {class_name:<20} {weight}\n"
        )

    f.write("\n")

    f.write("MODEL\n")
    f.write("-" * 70 + "\n")
    f.write("Model: Custom CNN\n")
    f.write("Input: 256 x 256 x 3\n")
    f.write("Output classes: 4\n")
    f.write("Optimizer: Adam\n")
    f.write("Loss: Sparse Categorical Crossentropy\n")
    f.write("Class weights used: Yes\n\n")

    f.write("TRAINING RESULTS\n")
    f.write("-" * 70 + "\n")

    if training_results:

        f.write(
            f"Epochs completed: "
            f"{training_results['epochs_completed']}\n"
        )

        f.write(
            f"Best training accuracy: "
            f"{training_results['best_training_accuracy']:.4f}\n"
        )

        f.write(
            f"Best validation accuracy: "
            f"{training_results['best_validation_accuracy']:.4f}\n"
        )

        f.write(
            f"Best validation epoch: "
            f"{training_results['best_validation_epoch']}\n"
        )

    f.write("\n")

    f.write("TEST RESULTS\n")
    f.write("-" * 70 + "\n")
    f.write(
        f"Test accuracy: "
        f"{test_results['test_accuracy']:.4f} "
        f"({test_results['test_accuracy'] * 100:.2f}%)\n"
    )

    f.write(
        f"Test loss: "
        f"{test_results['test_loss']:.4f}\n"
    )

    f.write(
        f"Macro F1: "
        f"{test_results['macro_f1']:.4f}\n"
    )

    f.write(
        f"Weighted F1: "
        f"{test_results['weighted_f1']:.4f}\n\n"
    )

    f.write("PER-CLASS PERFORMANCE\n")
    f.write("-" * 70 + "\n")

    for class_name, metrics in per_class_results.items():

        f.write(
            f"{class_name:<20} "
            f"Precision: {metrics['precision']:.4f} | "
            f"Recall: {metrics['recall']:.4f} | "
            f"F1: {metrics['f1_score']:.4f}\n"
        )

    f.write("\n")

    f.write("CONFUSION MATRIX\n")
    f.write("-" * 70 + "\n")

    f.write(
        "Class order: "
        + ", ".join(classes)
        + "\n\n"
    )

    for row in confusion_matrix:
        f.write(" ".join(f"{value:4d}" for value in row) + "\n")

    f.write("\n")

    f.write("KEY FINDINGS\n")
    f.write("-" * 70 + "\n")

    for finding in findings:
        f.write(f"- {finding}\n")

    f.write("\n")
    f.write("=" * 70 + "\n")
    f.write("EXPERIMENT SUMMARY COMPLETE\n")
    f.write("=" * 70 + "\n")


# ============================================================
# CONSOLE OUTPUT
# ============================================================

print("=" * 60)
print("CORN PATHOLOGY AI - EXPERIMENT SUMMARY")
print("=" * 60)

print()
print("Dataset:")
print(f"  Original images : 4188")
print(f"  Clean images    : 4184")
print(f"  Classes         : 4")

print()
print("Dataset split:")
print(f"  Training        : 2928")
print(f"  Validation      : 628")
print(f"  Test            : 628")

print()
print("Training:")
print(
    f"  Best training accuracy   : "
    f"{training_results.get('best_training_accuracy', 0) * 100:.2f}%"
)

print(
    f"  Best validation accuracy : "
    f"{training_results.get('best_validation_accuracy', 0) * 100:.2f}%"
)

print()
print("Final test performance:")
print(f"  Test accuracy : 93.63%")
print(f"  Test loss     : 0.1805")
print(f"  Macro F1      : 92.32%")
print(f"  Weighted F1   : 93.69%")

print()
print("Files created:")
print(f"  {SUMMARY_JSON}")
print(f"  {SUMMARY_TXT}")

print()
print("=" * 60)
print("EXPERIMENT SUMMARY COMPLETE")
print("=" * 60)