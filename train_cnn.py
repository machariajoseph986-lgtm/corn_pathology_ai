import os
import json
import tensorflow as tf

from cnn_model import build_cnn_model


# ============================================================
# MAIZE DISEASE CNN TRAINING
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------
# DATA DIRECTORIES
# ------------------------------------------------------------

TRAIN_DIR = os.path.join(
    BASE_DIR,
    "dataset_split",
    "train"
)

VALIDATION_DIR = os.path.join(
    BASE_DIR,
    "dataset_split",
    "validation"
)

# ------------------------------------------------------------
# CLASS WEIGHTS
# ------------------------------------------------------------

CLASS_WEIGHTS_FILE = os.path.join(
    BASE_DIR,
    "class_weights.json"
)

# ------------------------------------------------------------
# OUTPUT DIRECTORY
# ------------------------------------------------------------

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "training_output"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# CONFIGURATION
# ============================================================

IMAGE_SIZE = (256, 256)

BATCH_SIZE = 32

EPOCHS = 30

SEED = 42


# ============================================================
# HEADER
# ============================================================

print("=" * 60)
print("MAIZE DISEASE CNN TRAINING")
print("=" * 60)


# ============================================================
# LOAD TRAINING DATASET
# ============================================================

print("\nLoading training dataset...")

train_dataset = tf.keras.utils.image_dataset_from_directory(

    TRAIN_DIR,

    labels="inferred",

    label_mode="int",

    image_size=IMAGE_SIZE,

    batch_size=BATCH_SIZE,

    shuffle=True,

    seed=SEED
)


# ============================================================
# LOAD VALIDATION DATASET
# ============================================================

print("Loading validation dataset...")

validation_dataset = tf.keras.utils.image_dataset_from_directory(

    VALIDATION_DIR,

    labels="inferred",

    label_mode="int",

    image_size=IMAGE_SIZE,

    batch_size=BATCH_SIZE,

    shuffle=False
)


# ============================================================
# DISPLAY CLASS INFORMATION
# ============================================================

class_names = train_dataset.class_names

print("\nClasses:")

for index, class_name in enumerate(class_names):

    print(
        f"  {index}: {class_name}"
    )


# ============================================================
# DATA AUGMENTATION
#
# IMPORTANT:
# Augmentation is applied ONLY to training data.
# Validation data remains untouched.
# ============================================================

data_augmentation = tf.keras.Sequential([

    tf.keras.layers.RandomFlip(
        "horizontal"
    ),

    tf.keras.layers.RandomRotation(
        0.10
    ),

    tf.keras.layers.RandomZoom(
        0.10
    ),

    tf.keras.layers.RandomContrast(
        0.10
    )

], name="data_augmentation")


# ============================================================
# PREPROCESSING
#
# Convert pixel values:
#
# 0-255  →  0-1
#
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
            data_augmentation(images, training=True)
        ),
        labels
    ),

    num_parallel_calls=tf.data.AUTOTUNE
)


# ============================================================
# APPLY VALIDATION PREPROCESSING
#
# NO AUGMENTATION
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

print("\nLoading class weights...")

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
        f"{class_names[class_index]:<20}"
        f"{weight:.6f}"
    )


# ============================================================
# BUILD CNN MODEL
# ============================================================

print("\nBuilding CNN model...")

model = build_cnn_model()


# ============================================================
# COMPILE MODEL
# ============================================================

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

print("\nCNN architecture:")

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

model_checkpoint = tf.keras.callbacks.ModelCheckpoint(

    filepath=os.path.join(
        OUTPUT_DIR,
        "best_maize_disease_cnn.keras"
    ),

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
print("STARTING TRAINING")
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

    "final_maize_disease_cnn.keras"
)

model.save(
    final_model_path
)


# ============================================================
# SAVE TRAINING HISTORY
# ============================================================

history_path = os.path.join(

    OUTPUT_DIR,

    "training_history.json"
)


history_data = {
    key: [
        float(value)
        for value in values
    ]
    for key, values
    in history.history.items()
}


with open(
    history_path,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        history_data,
        file,
        indent=4
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("TRAINING COMPLETE")
print("=" * 60)

print("\nBest model:")
print(
    os.path.join(
        OUTPUT_DIR,
        "best_maize_disease_cnn.keras"
    )
)

print("\nFinal model:")
print(final_model_path)

print("\nTraining history:")
print(history_path)

print("\nThe TEST dataset has NOT been used.")

print("\n" + "=" * 60)