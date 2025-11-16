import os

for file_number in range(1, 55):
    filename = f"resized_{file_number}.bmp"
    try:
        os.remove(filename)
        print(f"Deleted {filename}")
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"An error occurred while trying to delete {filename}: {e}")

print("\nDeletion process finished.")