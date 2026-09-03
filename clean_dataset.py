import os
import shutil

# ============================================================
# ALWAYS USE THE FOLDER WHERE THIS SCRIPT IS LOCATED
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(
    BASE_DIR,
    "data"
)

QUARANTINE_PATH = os.path.join(
    BASE_DIR,
    "quarantine",
    "conflicting_duplicates"
)

# ============================================================
# FILES TO QUARANTINE
# ============================================================

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
    )
]

# ============================================================
# CREATE CORRECT QUARANTINE FOLDER
# ============================================================

os.makedirs(QUARANTINE_PATH, exist_ok=True)

print("=" * 60)
print("CORN PATHOLOGY DATASET CLEANING")
print("=" * 60)

found = 0
moved = 0

for file_path in FILES_TO_QUARANTINE:

    if os.path.isfile(file_path):

        found += 1

        filename = os.path.basename(file_path)

        destination = os.path.join(
            QUARANTINE_PATH,
            filename
        )

        if os.path.exists(destination):

            print(f"Already quarantined: {filename}")

        else:

            shutil.move(file_path, destination)

            moved += 1

            print(f"MOVED: {filename}")

    else:

        print(f"NOT FOUND: {file_path}")

print("\n" + "=" * 60)
print("CLEANING SUMMARY")
print("=" * 60)

print(f"Files identified : {len(FILES_TO_QUARANTINE)}")
print(f"Files found      : {found}")
print(f"Files moved      : {moved}")

print("\nCleaning complete.")
print("=" * 60)