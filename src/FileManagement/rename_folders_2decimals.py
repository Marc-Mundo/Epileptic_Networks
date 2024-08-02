import os
import re


# Function to ensure the number has two decimal places
def ensure_two_decimals(num):
    return f"{num:.2f}"


# Function to create the new folder name with numbers formatted to two decimal places
def create_new_folder_name(folder_name):
    pattern = re.compile(r"(\d+\.\d+|\d+)")

    def replace_with_two_decimals(matchobj):
        # Extract the number from the match object
        number = float(matchobj.group(0))
        # Format the number with two decimal places
        return ensure_two_decimals(number)

    # Replace all occurrences of the pattern in the folder name
    new_folder_name = pattern.sub(replace_with_two_decimals, folder_name)

    return new_folder_name


# Example usage of the function
# directory_path = "/home/Marc_network_sims/data/Data05_Current_Burst"  # Replace with your actual directory path
directory_path = "/mnt/internserver1_1tb/Data/MarcData/Data14_Current_Burst"  # 1tb server on internserver1, run experiments on 2

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
