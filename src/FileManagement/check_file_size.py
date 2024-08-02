import os


def check_pkl_file_sizes_less_than(base_directory, max_size_mb=20):
    # Convert max size from MB to bytes
    max_size_bytes = max_size_mb * 1024 * 1024
    incorrect_files = []

    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith(".pkl"):
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                # Check if file size is less than 25 MB
                if file_size < max_size_bytes:
                    incorrect_files.append((file_path, file_size / (1024 * 1024)))

    return incorrect_files


# base_directory = "../../data/Data05_Current_Burst"
base_directory = "/home/Marc/Marc_network_sims/data/Data05_External_noise"
incorrect_files = check_pkl_file_sizes_less_than(base_directory)

if incorrect_files:
    print("Files smaller than 25 MB:")
    for file_path, size in incorrect_files:
        print(f"{file_path}: {size:.2f} MB")
else:
    print("All .pkl files are 25 MB or larger.")


# Function to delete files smaller than 20 MB
def delete_pkl_files_smaller_than(base_directory, min_size_mb=20):
    # Convert min size from MB to bytes
    min_size_bytes = min_size_mb * 1024 * 1024
    deleted_files = []

    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith(".pkl"):
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                # Check if file size is less than 20 MB and delete it
                if file_size < min_size_bytes:
                    os.remove(file_path)  # Delete the file
                    deleted_files.append(file_path)
                    print(f"Deleted {file_path}: {file_size / (1024 * 1024):.2f} MB")

    return deleted_files


# base_directory = "../../data/Data05_Current_Burst"
base_directory = "/home/Marc/Marc_network_sims/data/Data05_External_noise"
deleted_files = delete_pkl_files_smaller_than(base_directory)

if deleted_files:
    print(f"Deleted {len(deleted_files)} files smaller than 20 MB.")
else:
    print("No files smaller than 20 MB found.")
