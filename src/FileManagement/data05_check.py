import os
import numpy as np


def verify_directories_and_pkls(base_directory):
    missing_directories = []
    directories_with_missing_pkls = []
    total_missing_pkls = 0  # Counter for total missing .pkl files
    total_directories = 0  # Counter for total directories
    total_pkls = 0  # Counter for total .pkl files
    pkls_smaller_than_20mb = []  # List to keep track of .pkl files smaller than 20 MB

    pyr_noise_factors = [
        0.65,
        0.70,
        0.75,
        0.80,
        0.85,
        0.90,
        0.95,
        1.00,
        1.10,
        1.20,
        1.30,
    ]
    expected_pkl_files = 15

    for gk in np.arange(0.50, 1.60, 0.1):
        for gna in np.arange(0.50, 1.60, 0.1):
            for noise_factor in pyr_noise_factors:
                variant = f"gna_{gna:.2f}_gk_{gk:.2f}_noise_{noise_factor:.2f}"
                dir_path = os.path.join(base_directory, variant)

                if not os.path.exists(dir_path):
                    missing_directories.append(variant)
                else:
                    total_directories += 1  # Increment total directories count
                    pkl_files = [f for f in os.listdir(dir_path) if f.endswith(".pkl")]
                    num_pkls = len(pkl_files)
                    total_pkls += num_pkls  # Increment total .pkl files count

                    if num_pkls != expected_pkl_files:
                        missing_pkls_in_dir = expected_pkl_files - num_pkls
                        total_missing_pkls += missing_pkls_in_dir
                        directories_with_missing_pkls.append((variant, num_pkls))

                    for pkl_file in pkl_files:
                        file_path = os.path.join(dir_path, pkl_file)
                        file_size = os.path.getsize(file_path)
                        if (
                            file_size < 20 * 1024 * 1024
                        ):  # Check if file size is less than 20 MB
                            pkls_smaller_than_20mb.append(file_path)

    # Verify if the total directories and .pkl files match the expected numbers
    correct_directory_count = total_directories == 1331
    correct_pkl_count = total_pkls == 19965 and not pkls_smaller_than_20mb

    return {
        "missing_directories": missing_directories,
        "directories_with_missing_pkls": directories_with_missing_pkls,
        "total_missing_pkls": total_missing_pkls,
        "pkls_smaller_than_20mb": pkls_smaller_than_20mb,
        "correct_directory_count": correct_directory_count,
        "correct_pkl_count": correct_pkl_count,
        "total_directories": total_directories,
        "total_pkls": total_pkls,
    }


# base_directory = "/mnt/internserver1_1tb/Data/MarcData/Data14_Current_Burst"
base_directory = "/home/Marc/Marc_network_sims/data/Data05_External_noise"

results = verify_directories_and_pkls(base_directory)

if results["missing_directories"]:
    print("Missing directories:")
    for directory in results["missing_directories"]:
        print(directory)
else:
    print("No missing directories.")

if results["directories_with_missing_pkls"]:
    print("\nDirectories with incorrect number of .pkl files:")
    for directory, count in results["directories_with_missing_pkls"]:
        print(f"{directory}: {count} .pkl files")
else:
    print("\nAll directories have the correct number of .pkl files.")

if results["pkls_smaller_than_20mb"]:
    print("\n.pkl files smaller than 20 MB:")
    for filepath in results["pkls_smaller_than_20mb"]:
        print(filepath)
else:
    print("\nAll .pkl files are at least 20 MB.")

print(f"\nTotal missing .pkl files: {results['total_missing_pkls']}")
print(f"Total directories counted: {results['total_directories']}")
print(f"Total .pkl files counted: {results['total_pkls']}")

if results["correct_directory_count"]:
    print("Directory count check: Passed")
else:
    print(
        "Directory count check: Failed (expected 1331, found {results['total_directories']})"
    )

if results["correct_pkl_count"]:
    print("File count and size check: Passed")
else:
    print("File count and size check: Failed")
    if not results["correct_pkl_count"]:
        print("Expected 19965 .pkl files of at least 20 MB, discrepancies found.")

# Enhanced clarity on what check failed
if (
    results["correct_directory_count"]
    and results["correct_pkl_count"]
    and not results["pkls_smaller_than_20mb"]
):
    print(
        "All checks passed: Correct number of directories and .pkl files of appropriate size."
    )
else:
    print("Verification details provided above.")
