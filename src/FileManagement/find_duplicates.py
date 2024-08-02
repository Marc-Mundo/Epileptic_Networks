import os


def find_duplicate_folders(directory_path_1, directory_path_2):
    # Get the list of folder names in each directory
    folders_1 = set(os.listdir(directory_path_1))
    folders_2 = set(os.listdir(directory_path_2))

    # Find intersection of the two sets to get the list of duplicates
    duplicates = folders_1.intersection(folders_2)

    # Print the duplicate folder names
    if duplicates:
        print("Duplicate folders found:")
        for folder in duplicates:
            print(folder)
    else:
        print("No duplicate folders found.")


# Replace with the actual paths to your directories
directory_path_1 = (
    "/home/Marc/Marc_network_sims/data"  # "/path/to/your/first/directory"
)
directory_path_2 = "/home/Marc_network_sims/data/Data05_Current_Burst"  # "/path/to/your/second/directory"

find_duplicate_folders(directory_path_1, directory_path_2)
