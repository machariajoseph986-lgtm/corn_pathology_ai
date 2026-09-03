import os
import tensorflow as tf
import matplotlib.pyplot as plt

# ============================================================
# MAIZE DISEASE IMAGE PREPROCESSING PIPELINE
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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

TEST_DIR = os.path.join(
    BASE_DIR,
    "dataset_split",
    "test"
)

# ============================================================
# CONFIGURATION
# ============================================================

IMAGE_SIZE = (256, 256)
BATCH_SIZE = 32
SEED = 42


# ============================================================
# LOAD DATASETS
# ============================================================

print("=" * 60)
print("MAIZE DISEASE PREPROCESSING PIPELINE")
print("=" * 60)

print("\nLoading training dataset...")

train_dataset = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
    color_mode="rgb",
    shuffle=True,
    seed=SEED
)

print("Loading validation dataset...")

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    VALIDATION_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
    color_mode="rgb",
    shuffle=False
)

print("Loading test dataset...")

test_dataset = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
    color_mode="rgb",
    shuffle=False
)


# ============================================================
# CLASS NAMES
# ============================================================

class_names = train_dataset.class_names

print("\nClasses:")
for index, class_name in enumerate(class_names):
    print(f"  {index}: {class_name}")


# ============================================================
# DATA AUGMENTATION
# TRAINING ONLY
# ============================================================

data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip(
        "horizontal"
    ),

    tf.keras.layers.RandomRotation(
        0.04
    ),

    tf.keras.layers.RandomZoom(
        0.10
    ),

    tf.keras.layers.RandomTranslation(
        height_factor=0.05,
        width_factor=0.05
    )
], name="data_augmentation")


# ============================================================
# NORMALIZATION
# ============================================================

normalization = tf.keras.layers.Rescaling(
    1.0 / 255
)


# ============================================================
# PREPROCESS TRAINING DATA
# ============================================================

def preprocess_training(images, labels):

    images = normalization(images)

    images = data_augmentation(images)

    return images, labels


# ============================================================
# PREPROCESS VALIDATION / TEST DATA
# ============================================================

def preprocess_evaluation(images, labels):

    images = normalization(images)

    return images, labels


train_dataset = train_dataset.map(
    preprocess_training,
    num_parallel_calls=tf.data.AUTOTUNE
)

validation_dataset = validation_dataset.map(
    preprocess_evaluation,
    num_parallel_calls=tf.data.AUTOTUNE
)

test_dataset = test_dataset.map(
    preprocess_evaluation,
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

test_dataset = test_dataset.prefetch(
    tf.data.AUTOTUNE
)


# ============================================================
# VERIFY IMAGE SHAPES AND PIXEL VALUES
# ============================================================

images, labels = next(iter(train_dataset))

print("\n" + "-" * 60)
print("PIPELINE VERIFICATION")
print("-" * 60)

print(f"Batch shape: {images.shape}")
print(f"Label shape: {labels.shape}")

print(
    f"Pixel range: "
    f"{tf.reduce_min(images).numpy():.3f} "
    f"to "
    f"{tf.reduce_max(images).numpy():.3f}"
)

print(f"Expected image shape: (256, 256, 3)")
print("Expected normalized pixel range: 0.0 to 1.0")


# ============================================================
# DISPLAY SAMPLE AUGMENTED IMAGES
# ============================================================

plt.figure(figsize=(10, 10))

for i in range(min(9, len(images))):

    ax = plt.subplot(3, 3, i + 1)

    plt.imshow(images[i].numpy())

    label_index = labels[i].numpy()

    plt.title(
        class_names[label_index]
    )

    plt.axis("off")

plt.suptitle(
    "Sample Training Images After Preprocessing + Augmentation"
)

plt.tight_layout()

plt.savefig(
    "preprocessing_samples.png",
    dpi=300
)

plt.show()


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("PREPROCESSING PIPELINE READY")
print("=" * 60)

print("Image size       : 256 x 256")
print("Color channels   : RGB (3)")
print("Normalization    : 0-1")
print("Batch size       : 32")
print("Training augment : YES")
print("Validation augment: NO")
print("Test augment     : NO")

print("\nPipeline verification complete.")
print("=" * 60)