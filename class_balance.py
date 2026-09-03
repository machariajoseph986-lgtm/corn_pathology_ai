import os
from collections import Counter
import matplotlib.pyplot as plt

# ============================================================
# CLASS BALANCE ANALYSIS
# ============================================================

DATASET_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data"
)

VALID_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".JPG",
    ".JPEG",
    ".PNG"
)

class_counts = Counter()

for class_name in os.listdir(DATASET_PATH):

    class_path = os.path.join(
        DATASET_PATH,
        class_name
    )

    if not os.path.isdir(class_path):
        continue

    count = 0

    for filename in os.listdir(class_path):

        if filename.endswith(VALID_EXTENSIONS):
            count += 1

    class_counts[class_name] = count


# ============================================================
# PRINT RESULTS
# ============================================================

total = sum(class_counts.values())

print("=" * 60)
print("CORN PATHOLOGY CLASS BALANCE ANALYSIS")
print("=" * 60)

print(f"\nTotal images: {total}\n")

for class_name, count in sorted(class_counts.items()):

    percentage = (count / total) * 100

    print(
        f"{class_name:<20} "
        f"{count:>5} images "
        f"({percentage:>6.2f}%)"
    )


# ============================================================
# IMBALANCE RATIO
# ============================================================

largest_class = max(class_counts, key=class_counts.get)
smallest_class = min(class_counts, key=class_counts.get)

largest_count = class_counts[largest_class]
smallest_count = class_counts[smallest_class]

imbalance_ratio = largest_count / smallest_count

print("\n" + "-" * 60)

print(f"Largest class : {largest_class} ({largest_count})")
print(f"Smallest class: {smallest_class} ({smallest_count})")
print(f"Imbalance ratio: {imbalance_ratio:.2f}x")


# ============================================================
# BAR CHART
# ============================================================

plt.figure(figsize=(9, 6))

plt.bar(
    class_counts.keys(),
    class_counts.values()
)

plt.title("Corn Pathology Dataset - Class Distribution")
plt.xlabel("Class")
plt.ylabel("Number of Images")

plt.xticks(rotation=20)

plt.tight_layout()

plt.savefig(
    "class_distribution.png",
    dpi=300
)

plt.show()

print("\nChart saved as: class_distribution.png")
print("=" * 60)