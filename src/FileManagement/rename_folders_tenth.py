import os
import re
import math


# Function to round up the number to the nearest tenth
def round_up_to_nearest_tenth(num):
    return math.ceil(num * 10) / 10


# Function to create the new folder name by rounding numbers to the nearest tenth
def create_new_folder_name(folder_name):
    pattern = re.compile(r"(\d+\.\d+)")

    def replace_with_rounded(matchobj):
        # Extract the number from the match object, round it up to the nearest tenth
        number = float(matchobj.group(0))
        rounded_number = round_up_to_nearest_tenth(number)
        # Format the rounded number with one decimal place
        return f"{rounded_number:.1f}"

    # Replace all occurrences of the pattern in the folder name
    new_folder_name = pattern.sub(replace_with_rounded, folder_name)

    return new_folder_name


# Example usage of the function
directory_path = "/home/Marc_network_sims/data/Data05_Current_Burst"  # Replace with your actual directory path

# Iterate over each folder and rename it
for folder_name in os.listdir(directory_path):
    if os.path.isdir(os.path.join(directory_path, folder_name)):
        new_folder_name = create_new_folder_name(folder_name)
        old_folder_path = os.path.join(directory_path, folder_name)
        new_folder_path = os.path.join(directory_path, new_folder_name)

        # Check if the new folder path already exists
        if not os.path.exists(new_folder_path):
            # Rename the folder
            os.rename(old_folder_path, new_folder_path)
            print(f'Renamed "{folder_name}" to "{new_folder_name}"')
        else:
            print(
                f"Cannot rename '{folder_name}' to '{new_folder_name}' because the target directory already exists."
            )
