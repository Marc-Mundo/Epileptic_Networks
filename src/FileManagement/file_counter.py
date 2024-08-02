import os


def count_folders_and_pkls(directory_path):
    folder_count = 0
    pkl_count = 0

    # Iterate over all items in the given directory
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)

        # Check if the item is a directory (folder)
        if os.path.isdir(item_path):
            folder_count += 1  # Increment the folder count

            # Count .pkl files in this directory
            for file in os.listdir(item_path):
                if file.endswith(".pkl"):
                    pkl_count += 1  # Increment the .pkl file count

    return folder_count, pkl_count


# Replace '/path/to/your/directory' with the actual path to your data directory
# directory_path = "/home/Marc/Marc_network_sims/data/Data05_External_noise"
directory_path = "/mnt/internserver1_1tb/Data/MarcData/Data14_Current_Burst"
folder_count, pkl_count = count_folders_and_pkls(directory_path)

print(f"Total folders: {folder_count}")  # Should be 1331 directories
print(f"Total .pkl files: {pkl_count}")  # Should be 19965 .pkl files (15 each dir.)
