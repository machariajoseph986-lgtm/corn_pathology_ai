import os
from PIL import Image
from collections import Counter
import hashlib

# ============================================================
# CORN PATHOLOGY DATASET INSPECTION
# ============================================================

# Dataset location
DATASET_PATH = "data"

# Supported image formats
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}


# ------------------------------------------------------------
# 1. Find all images
# ------------------------------------------------------------

image_files = []

for root, dirs, files in os.walk(DATASET_PATH):
    for file in files:
        extension = os.path.splitext(file)[1]

        if extension.lower() in {".jpg", ".jpeg", ".png"}:
            image_files.append(os.path.join(root, file))


print("=" * 60)
print("CORN PATHOLOGY DATASET INSPECTION")
print("=" * 60)

print(f"\nTotal images found: {len(image_files)}")


# ------------------------------------------------------------
# 2. Count images by class
# ------------------------------------------------------------

class_counts = Counter()

for file_path in image_files:
    # Get the folder containing the image
    class_name = os.path.basename(os.path.dirname(file_path))
    class_counts[class_name] += 1


print("\n" + "-" * 60)
print("IMAGES PER CLASS")
print("-" * 60)

for class_name, count in sorted(class_counts.items()):
    percentage = (count / len(image_files)) * 100
    print(f"{class_name:20} {count:5} images ({percentage:.2f}%)")


# ------------------------------------------------------------
# 3. Check image integrity
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("CHECKING IMAGE INTEGRITY")
print("-" * 60)

corrupted_images = []

for i, file_path in enumerate(image_files, start=1):

    try:
        with Image.open(file_path) as img:
            img.verify()

    except Exception as e:
        corrupted_images.append((file_path, str(e)))

    # Progress indicator
    if i % 500 == 0:
        print(f"Checked {i}/{len(image_files)} images...")


print(f"\nCorrupted images: {len(corrupted_images)}")

if corrupted_images:
    print("\nCorrupted files:")

    for file_path, error in corrupted_images:
        print(f"  {file_path}")
        print(f"  Error: {error}")


# ------------------------------------------------------------
# 4. Inspect image dimensions
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("IMAGE DIMENSIONS")
print("-" * 60)

dimensions = Counter()
failed_dimensions = []

for file_path in image_files:

    try:
        with Image.open(file_path) as img:
            dimensions[img.size] += 1

    except Exception:
        failed_dimensions.append(file_path)


print(f"\nDifferent image dimensions found: {len(dimensions)}")

print("\nMost common dimensions:")

for dimension, count in dimensions.most_common(15):
    print(f"  {dimension[0]} x {dimension[1]} : {count} images")


# ------------------------------------------------------------
# 5. Check image formats
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("IMAGE FORMATS")
print("-" * 60)

format_counts = Counter()

for file_path in image_files:

    try:
        with Image.open(file_path) as img:
            format_counts[img.format] += 1

    except Exception:
        pass


for image_format, count in format_counts.items():
    print(f"{image_format:10} {count:5} images")


# ------------------------------------------------------------
# 6. Check for duplicate images
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("CHECKING FOR DUPLICATES")
print("-" * 60)

hashes = {}
duplicates = []

for i, file_path in enumerate(image_files, start=1):

    try:
        with open(file_path, "rb") as f:
            file_hash = hashlib.md5(f.read()).hexdigest()

        if file_hash in hashes:
            duplicates.append(
                (file_path, hashes[file_hash])
            )
        else:
            hashes[file_hash] = file_path

    except Exception:
        pass

    if i % 500 == 0:
        print(f"Processed {i}/{len(image_files)} images...")


print(f"\nDuplicate images found: {len(duplicates)}")

if duplicates:

    print("\nDuplicate pairs:")

    for duplicate, original in duplicates[:20]:
        print(f"\nDuplicate: {duplicate}")
        print(f"Original : {original}")

    if len(duplicates) > 20:
        print(
            f"\nShowing first 20 only. "
            f"Total duplicates: {len(duplicates)}"
        )


# ------------------------------------------------------------
# 7. Final summary
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FINAL SUMMARY")
print("=" * 60)

print(f"Total images       : {len(image_files)}")
print(f"Number of classes  : {len(class_counts)}")
print(f"Corrupted images   : {len(corrupted_images)}")
print(f"Duplicate images   : {len(duplicates)}")
print(f"Different sizes    : {len(dimensions)}")

print("\nClasses:")

for class_name, count in sorted(class_counts.items()):
    print(f"  {class_name}: {count}")

print("\nInspection complete.")
print("=" * 60)