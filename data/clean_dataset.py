import os
import shutil

DATASET_PATH = "data"

QUARANTINE_PATH = os.path.join(
    "quarantine",
    "conflicting_duplicates"
)

FILES_TO_QUARANTINE = [
    os.path.join(
        DATASET_PATH,
        "Blight",
        "Corn_Blight (77).jpg"
    ),
    os.path.join(
        DATASET_PATH,
        "Blight",
        "Corn_Blight (1104).jpg"
    ),
    os.path.join(
        DATASET_PATH,
        "Gray_Leaf_Spot",
        "Corn_Gray_Spot (19).jpg"
    ),
    os.path.join(
        DATASET_PATH,
        "Gray_Leaf_Spot",
        "Corn_Gray_Spot (564).jpg"
    ),
]

# Create the correct quarantine folder
os.makedirs(QUARANTINE_PATH, exist_ok=True)

print("=" * 60)
print("CORN PATHOLOGY DATASET CLEANING")
print("=" * 60)

print("\nChecking files...")

found = 0
moved = 0

for file_path in FILES_TO_QUARANTINE:

    if not os.path.isfile(file_path):
        print(f"NOT FOUND: {file_path}")
        continue

    found += 1

    filename = os.path.basename(file_path)
    destination = os.path.join(
        QUARANTINE_PATH,
        filename
    )

    shutil.move(file_path, destination)

    moved += 1

    print(f"\nMOVED:")
    print(f"  FROM: {file_path}")
    print(f"  TO:   {destination}")

print("\n" + "=" * 60)
print("CLEANING SUMMARY")
print("=" * 60)

print(f"Files identified: {len(FILES_TO_QUARANTINE)}")
print(f"Files found:     {found}")
print(f"Files moved:     {moved}")

print("\nCleaning complete.")