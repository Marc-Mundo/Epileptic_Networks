import os
import re

# The directory containing the folders
directory_path = "/home/Marc_network_sims/data/Data05_Current_Burst"  # Replace with your actual directory path


# Function to determine if the file name represents a number 15 or higher
def should_delete(file_name):
    match = re.match(r"(\d+)\.pkl$", file_name)
    if match:
        # Extract the number from the filename and check if it is 15 or higher
        number = int(match.group(1))
        return number >= 15
    return False


# Iterate over each folder in the directory
for folder_name in os.listdir(directory_path):
    folder_path = os.path.join(directory_path, folder_name)

    # Check if it is indeed a folder
    if os.path.isdir(folder_path):
        # List all files in the directory
        files = os.listdir(folder_path)

        # Iterate over files and remove those numbered 15 or higher
        for file_name in files:
            if should_delete(file_name):
                file_path = os.path.join(folder_path, file_name)
                os.remove(file_path)  # Remove the file
                print(f'Deleted "{file_name}" from "{folder_name}".')

print("File deletion process completed.")
