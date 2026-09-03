import os
import json
from collections import Counter

# ============================================================
# MAIZE DISEASE CLASS WEIGHTS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TRAIN_DIR = os.path.join(
    BASE_DIR,
    "dataset_split",
    "train"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "class_weights.json"
)

VALID_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".JPG",
    ".JPEG",
    ".PNG"
)


# ============================================================
# HEADER
# ============================================================

print("=" * 60)
print("MAIZE DISEASE CLASS WEIGHT CALCULATION")
print("=" * 60)


# ============================================================
# FIND CLASSES
# ============================================================

classes = sorted([
    directory
    for directory in os.listdir(TRAIN_DIR)
    if os.path.isdir(
        os.path.join(TRAIN_DIR, directory)
    )
])


print("\nClasses:")
for index, class_name in enumerate(classes):
    print(f"  {index}: {class_name}")


# ============================================================
# COUNT TRAINING IMAGES
# ============================================================

class_counts = Counter()

for class_name in classes:

    class_path = os.path.join(
        TRAIN_DIR,
        class_name
    )

    for filename in os.listdir(class_path):

        if filename.endswith(VALID_EXTENSIONS):

            class_counts[class_name] += 1


total_images = sum(class_counts.values())

number_of_classes = len(classes)


# ============================================================
# DISPLAY CLASS COUNTS
# ============================================================

print("\n" + "-" * 60)
print("TRAINING CLASS COUNTS")
print("-" * 60)

for class_name in classes:

    count = class_counts[class_name]

    percentage = (
        count / total_images
    ) * 100

    print(
        f"{class_name:<20}"
        f"{count:>6} images"
        f" ({percentage:>6.2f}%)"
    )


print(f"\nTotal training images: {total_images}")


# ============================================================
# CALCULATE CLASS WEIGHTS
#
# Formula:
#
# weight = total_images /
#          (number_of_classes × class_images)
#
# ============================================================

class_weights = {}

for index, class_name in enumerate(classes):

    count = class_counts[class_name]

    weight = (
        total_images /
        (number_of_classes * count)
    )

    class_weights[str(index)] = round(
        weight,
        6
    )


# ============================================================
# DISPLAY CLASS WEIGHTS
# ============================================================

print("\n" + "-" * 60)
print("CALCULATED CLASS WEIGHTS")
print("-" * 60)

for index, class_name in enumerate(classes):

    weight = class_weights[str(index)]

    print(
        f"{index}: "
        f"{class_name:<20}"
        f"weight = {weight:.6f}"
    )


# ============================================================
# SAVE CLASS WEIGHTS TO JSON
# ============================================================

output_data = {
    "classes": classes,
    "class_counts": dict(class_counts),
    "total_training_images": total_images,
    "number_of_classes": number_of_classes,
    "class_weights": class_weights
}


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        output_data,
        file,
        indent=4
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("CLASS WEIGHTS SAVED")
print("=" * 60)

print(f"\nFile:")
print(f"  {OUTPUT_FILE}")

print("\nClass weights:")
for index, class_name in enumerate(classes):

    print(
        f"  {index} - "
        f"{class_name}: "
        f"{class_weights[str(index)]}"
    )

print("\nClass weight calculation complete.")
print("=" * 60)