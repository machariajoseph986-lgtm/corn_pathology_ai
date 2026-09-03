import os
import shutil
from sklearn.model_selection import train_test_split

# ============================================================
# STRATIFIED TRAIN / VALIDATION / TEST SPLIT
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SOURCE_DIR = os.path.join(BASE_DIR, "data")

OUTPUT_DIR = os.path.join(BASE_DIR, "dataset_split")

TRAIN_DIR = os.path.join(OUTPUT_DIR, "train")
VAL_DIR = os.path.join(OUTPUT_DIR, "validation")
TEST_DIR = os.path.join(OUTPUT_DIR, "test")

RANDOM_STATE = 42

# 70% train, 15% validation, 15% test
TRAIN_SIZE = 0.70
VALIDATION_SIZE = 0.15
TEST_SIZE = 0.15

VALID_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".JPG",
    ".JPEG",
    ".PNG"
)


# ============================================================
# COLLECT ALL IMAGES
# ============================================================

images = []
labels = []

classes = sorted([
    directory
    for directory in os.listdir(SOURCE_DIR)
    if os.path.isdir(os.path.join(SOURCE_DIR, directory))
])


print("=" * 60)
print("STRATIFIED DATASET SPLITTING")
print("=" * 60)

print("\nClasses:")
for class_name in classes:
    print(f"  - {class_name}")


for class_name in classes:

    class_path = os.path.join(
        SOURCE_DIR,
        class_name
    )

    for filename in os.listdir(class_path):

        if filename.endswith(VALID_EXTENSIONS):

            image_path = os.path.join(
                class_path,
                filename
            )

            images.append(image_path)
            labels.append(class_name)


print(f"\nTotal images found: {len(images)}")


# ============================================================
# FIRST SPLIT
# 70% TRAIN
# 30% TEMPORARY
# ============================================================

train_images, temp_images, train_labels, temp_labels = train_test_split(
    images,
    labels,
    test_size=(VALIDATION_SIZE + TEST_SIZE),
    stratify=labels,
    random_state=RANDOM_STATE
)


# ============================================================
# SECOND SPLIT
# HALF OF TEMPORARY → VALIDATION
# HALF OF TEMPORARY → TEST
# ============================================================

val_images, test_images, val_labels, test_labels = train_test_split(
    temp_images,
    temp_labels,
    test_size=0.50,
    stratify=temp_labels,
    random_state=RANDOM_STATE
)


print("\n" + "-" * 60)

print("SPLIT RESULTS")
print("-" * 60)

print(f"Training   : {len(train_images)}")
print(f"Validation : {len(val_images)}")
print(f"Test       : {len(test_images)}")

print(f"Total      : {len(train_images) + len(val_images) + len(test_images)}")


# ============================================================
# CREATE OUTPUT DIRECTORIES
# ============================================================

for split_dir in [TRAIN_DIR, VAL_DIR, TEST_DIR]:

    for class_name in classes:

        os.makedirs(
            os.path.join(split_dir, class_name),
            exist_ok=True
        )


# ============================================================
# COPY IMAGES
# ============================================================

def copy_images(image_paths, labels, destination):

    for image_path, label in zip(image_paths, labels):

        filename = os.path.basename(image_path)

        destination_path = os.path.join(
            destination,
            label,
            filename
        )

        shutil.copy2(
            image_path,
            destination_path
        )


print("\nCopying training images...")
copy_images(
    train_images,
    train_labels,
    TRAIN_DIR
)

print("Copying validation images...")
copy_images(
    val_images,
    val_labels,
    VAL_DIR
)

print("Copying test images...")
copy_images(
    test_images,
    test_labels,
    TEST_DIR
)


# ============================================================
# VERIFY CLASS DISTRIBUTION
# ============================================================

def count_classes(split_dir):

    results = {}

    for class_name in classes:

        class_path = os.path.join(
            split_dir,
            class_name
        )

        count = sum(
            1
            for filename in os.listdir(class_path)
            if filename.endswith(VALID_EXTENSIONS)
        )

        results[class_name] = count

    return results


print("\n" + "=" * 60)
print("CLASS DISTRIBUTION")
print("=" * 60)

for split_name, split_dir in [
    ("TRAIN", TRAIN_DIR),
    ("VALIDATION", VAL_DIR),
    ("TEST", TEST_DIR)
]:

    counts = count_classes(split_dir)

    print(f"\n{split_name}")

    for class_name, count in counts.items():

        print(
            f"  {class_name:<20} {count:>5}"
        )


print("\n" + "=" * 60)
print("DATASET SPLITTING COMPLETE")
print("=" * 60)