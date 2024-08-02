import os

# The directory containing the folders
directory_path = "/home/Marc_network_sims/data/Data05_Current_Burst"  # Replace with your actual directory path

# Iterate over each folder in the directory
for folder_name in os.listdir(directory_path):
    folder_path = os.path.join(directory_path, folder_name)

    # Check if it is indeed a folder
    if os.path.isdir(folder_path):
        # List all files in the directory
        files = os.listdir(folder_path)

        # Check if there are any .pkl files in the directory
        pkl_files = [f for f in files if f.endswith(".pkl")]

        if not pkl_files:
            # If there are no .pkl files, delete the folder
            os.rmdir(folder_path)
            print(f'Deleted "{folder_name}" because it contains no .pkl files.')
        else:
            # If there are .pkl files, do nothing
            print(f'Kept "{folder_name}" because it contains .pkl files.')
