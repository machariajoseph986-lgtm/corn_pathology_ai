import os
import json
import tensorflow as tf


# ============================================================
# MAIZE DISEASE CNN — VERSION 2
# ============================================================
#
# Purpose:
# Controlled improvement experiment over train_cnn.py
#
# Main change:
#   256 x 256  →  320 x 320
#
# The CNN architecture, class weights, optimizer and training
# strategy remain consistent with the baseline.
#
# IMPORTANT:
#   This file does NOT modify train_cnn.py or cnn_model.py.
# ============================================================


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


TRAIN_DIR = os.path.join(
    PROJECT_DIR,
    "dataset_split",
    "train"
)


VALIDATION_DIR = os.path.join(
    PROJECT_DIR,
    "dataset_split",
    "validation"
)


CLASS_WEIGHTS_FILE = os.path.join(
    PROJECT_DIR,
    "class_weights.json"
)


# V2 gets its own output directory.
OUTPUT_DIR = os.path.join(
    PROJECT_DIR,
    "training_output",
    "v2"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# MODEL CONFIGURATION
# ============================================================

IMAGE_SIZE = (320, 320)

NUM_CHANNELS = 3

NUM_CLASSES = 4

BATCH_SIZE = 32

EPOCHS = 30

SEED = 42


CLASS_NAMES = [
    "Blight",
    "Common_Rust",
    "Gray_Leaf_Spot",
    "Healthy"
]


# ============================================================
# HEADER
# ============================================================

print("=" * 60)
print("MAIZE DISEASE CNN — VERSION 2")
print("=" * 60)

print("\nExperiment:")
print("  Input resolution : 320 x 320")
print("  CNN architecture : 32 → 64 → 128 → 256")
print("  Classes          : 4")
print("  Batch size       :", BATCH_SIZE)
print("  Maximum epochs   :", EPOCHS)

print("\nOutput directory:")
print(f"  {OUTPUT_DIR}")


# ============================================================
# LOAD TRAINING DATASET
# ============================================================

print("\n" + "-" * 60)
print("LOADING TRAINING DATASET")
print("-" * 60)

train_dataset = tf.keras.utils.image_dataset_from_directory(

    TRAIN_DIR,

    labels="inferred",

    label_mode="int",

    class_names=CLASS_NAMES,

    image_size=IMAGE_SIZE,

    batch_size=BATCH_SIZE,

    shuffle=True,

    seed=SEED
)


# ============================================================
# LOAD VALIDATION DATASET
# ============================================================

print("\nLoading validation dataset...")

validation_dataset = tf.keras.utils.image_dataset_from_directory(

    VALIDATION_DIR,

    labels="inferred",

    label_mode="int",

    class_names=CLASS_NAMES,

    image_size=IMAGE_SIZE,

    batch_size=BATCH_SIZE,

    shuffle=False
)


# ============================================================
# DISPLAY CLASS INFORMATION
# ============================================================

print("\nClasses:")

for index, class_name in enumerate(
    train_dataset.class_names
):

    print(
        f"  {index}: {class_name}"
    )


# ============================================================
# DATA AUGMENTATION
# ============================================================
#
# Controlled augmentation.
#
# We retain the baseline augmentation strategy but keep
# transformations moderate so that disease characteristics
# are not distorted excessively.
# ============================================================

data_augmentation = tf.keras.Sequential([

    tf.keras.layers.RandomFlip(
        "horizontal"
    ),

    tf.keras.layers.RandomRotation(
        0.08
    ),

    tf.keras.layers.RandomZoom(
        0.08
    ),

    tf.keras.layers.RandomContrast(
        0.08
    )

], name="data_augmentation_v2")


# ============================================================
# NORMALIZATION
# ============================================================

normalization = tf.keras.layers.Rescaling(
    1.0 / 255
)


# ============================================================
# APPLY TRAINING PREPROCESSING
# ============================================================

train_dataset = train_dataset.map(

    lambda images, labels: (
        normalization(
            data_augmentation(
                images,
                training=True
            )
        ),
        labels
    ),

    num_parallel_calls=tf.data.AUTOTUNE
)


# ============================================================
# APPLY VALIDATION PREPROCESSING
#
# IMPORTANT:
# No augmentation is applied to validation data.
# ============================================================

validation_dataset = validation_dataset.map(

    lambda images, labels: (
        normalization(images),
        labels
    ),

    num_parallel_calls=tf.data.AUTOTUNE
)


# ============================================================
# PERFORMANCE OPTIMIZATION
# ============================================================

train_dataset = train_dataset.prefetch(
    tf.data.AUTOTUNE
)

validation_dataset = validation_dataset.prefetch(
    tf.data.AUTOTUNE
)


# ============================================================
# LOAD CLASS WEIGHTS
# ============================================================

print("\n" + "-" * 60)
print("LOADING CLASS WEIGHTS")
print("-" * 60)

if not os.path.exists(CLASS_WEIGHTS_FILE):

    raise FileNotFoundError(
        f"\nClass weights file not found:\n"
        f"{CLASS_WEIGHTS_FILE}"
    )


with open(
    CLASS_WEIGHTS_FILE,
    "r",
    encoding="utf-8"
) as file:

    weights_data = json.load(file)


class_weights = {

    int(class_index): float(weight)

    for class_index, weight
    in weights_data["class_weights"].items()

}


print("\nClass weights:")

for class_index, weight in class_weights.items():

    print(
        f"  {class_index}: "
        f"{CLASS_NAMES[class_index]:<20}"
        f"{weight:.6f}"
    )


# ============================================================
# BUILD V2 CNN MODEL
# ============================================================
#
# Same architecture as the baseline.
#
# Only the input resolution is increased to 320 x 320.
# ============================================================

print("\n" + "-" * 60)
print("BUILDING V2 CNN MODEL")
print("-" * 60)


model = tf.keras.Sequential([

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    tf.keras.layers.Input(
        shape=(
            IMAGE_SIZE[0],
            IMAGE_SIZE[1],
            NUM_CHANNELS
        )
    ),


    # --------------------------------------------------------
    # CONVOLUTIONAL BLOCK 1
    # --------------------------------------------------------

    tf.keras.layers.Conv2D(
        filters=32,
        kernel_size=(3, 3),
        activation="relu",
        padding="same"
    ),

    tf.keras.layers.BatchNormalization(),

    tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2)
    ),


    # --------------------------------------------------------
    # CONVOLUTIONAL BLOCK 2
    # --------------------------------------------------------

    tf.keras.layers.Conv2D(
        filters=64,
        kernel_size=(3, 3),
        activation="relu",
        padding="same"
    ),

    tf.keras.layers.BatchNormalization(),

    tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2)
    ),


    # --------------------------------------------------------
    # CONVOLUTIONAL BLOCK 3
    # --------------------------------------------------------

    tf.keras.layers.Conv2D(
        filters=128,
        kernel_size=(3, 3),
        activation="relu",
        padding="same"
    ),

    tf.keras.layers.BatchNormalization(),

    tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2)
    ),


    # --------------------------------------------------------
    # CONVOLUTIONAL BLOCK 4
    # --------------------------------------------------------

    tf.keras.layers.Conv2D(
        filters=256,
        kernel_size=(3, 3),
        activation="relu",
        padding="same"
    ),

    tf.keras.layers.BatchNormalization(),

    tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2)
    ),


    # --------------------------------------------------------
    # FEATURE AGGREGATION
    # --------------------------------------------------------

    tf.keras.layers.GlobalAveragePooling2D(),


    # --------------------------------------------------------
    # CLASSIFICATION HEAD
    # --------------------------------------------------------

    tf.keras.layers.Dense(
        128,
        activation="relu"
    ),

    tf.keras.layers.Dropout(
        0.4
    ),


    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    tf.keras.layers.Dense(
        NUM_CLASSES,
        activation="softmax"
    )

], name="maize_disease_cnn_v2")


# ============================================================
# COMPILE MODEL
# ============================================================

print("\nCompiling model...")

model.compile(

    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.001
    ),

    loss=tf.keras.losses.SparseCategoricalCrossentropy(),

    metrics=[
        "accuracy"
    ]
)


# ============================================================
# DISPLAY MODEL
# ============================================================

print("\nCNN V2 architecture:")

model.summary()


# ============================================================
# CALLBACKS
# ============================================================

# ------------------------------------------------------------
# EARLY STOPPING
# ------------------------------------------------------------

early_stopping = tf.keras.callbacks.EarlyStopping(

    monitor="val_loss",

    patience=5,

    restore_best_weights=True,

    verbose=1
)


# ------------------------------------------------------------
# MODEL CHECKPOINT
# ------------------------------------------------------------

best_model_path = os.path.join(

    OUTPUT_DIR,

    "best_maize_disease_cnn_v2.keras"

)


model_checkpoint = tf.keras.callbacks.ModelCheckpoint(

    filepath=best_model_path,

    monitor="val_loss",

    save_best_only=True,

    verbose=1
)


# ------------------------------------------------------------
# LEARNING RATE REDUCTION
# ------------------------------------------------------------

reduce_learning_rate = tf.keras.callbacks.ReduceLROnPlateau(

    monitor="val_loss",

    factor=0.5,

    patience=2,

    min_lr=1e-6,

    verbose=1
)


# ============================================================
# TRAIN MODEL
# ============================================================

print("\n" + "=" * 60)
print("STARTING V2 TRAINING")
print("=" * 60)

history = model.fit(

    train_dataset,

    validation_data=validation_dataset,

    epochs=EPOCHS,

    class_weight=class_weights,

    callbacks=[
        early_stopping,
        model_checkpoint,
        reduce_learning_rate
    ]
)


# ============================================================
# SAVE FINAL MODEL
# ============================================================

final_model_path = os.path.join(

    OUTPUT_DIR,

    "final_maize_disease_cnn_v2.keras"

)


model.save(
    final_model_path
)


# ============================================================
# SAVE TRAINING HISTORY
# ============================================================

history_path = os.path.join(

    OUTPUT_DIR,

    "training_history_v2.json"

)


with open(
    history_path,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        history.history,
        file,
        indent=4
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("V2 TRAINING COMPLETE")
print("=" * 60)

print("\nSaved models:")

print(
    f"  Best model : {best_model_path}"
)

print(
    f"  Final model: {final_model_path}"
)

print(
    f"  History    : {history_path}"
)

print("\nFinal training metrics:")

print(
    f"  Train accuracy      : "
    f"{history.history['accuracy'][-1]:.4f}"
)

print(
    f"  Validation accuracy : "
    f"{history.history['val_accuracy'][-1]:.4f}"
)

print(
    f"  Train loss          : "
    f"{history.history['loss'][-1]:.4f}"
)

print(
    f"  Validation loss     : "
    f"{history.history['val_loss'][-1]:.4f}"
)

print("\n" + "=" * 60)
print("BASELINE REMAINS UNTOUCHED")
print("=" * 60)