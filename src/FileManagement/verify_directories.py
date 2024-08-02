import os
import numpy as np


def verify_directories_and_pkls(base_directory):
    missing_directories = []
    directories_with_missing_pkls = []
    total_missing_pkls = 0  # Counter for total missing .pkl files

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
                    pkl_files = [f for f in os.listdir(dir_path) if f.endswith(".pkl")]
                    num_pkls = len(pkl_files)
                    if num_pkls != expected_pkl_files:
                        missing_pkls_in_dir = expected_pkl_files - num_pkls
                        total_missing_pkls += (
                            missing_pkls_in_dir  # Update total missing count
                        )
                        directories_with_missing_pkls.append((variant, num_pkls))

    return missing_directories, directories_with_missing_pkls, total_missing_pkls


# base_directory = "/home/Marc/Marc_network_sims/data/Data05_External_noise"
base_directory = "/mnt/internserver1_1tb/Data/MarcData/Data14_Current_Burst"

missing_directories, directories_with_missing_pkls, total_missing_pkls = (
    verify_directories_and_pkls(base_directory)
)

if missing_directories:
    print("Missing directories:")
    for directory in missing_directories:
        print(directory)

if directories_with_missing_pkls:
    print("\nDirectories with incorrect number of .pkl files:")
    for directory, count in directories_with_missing_pkls:
        print(f"{directory}: {count} .pkl files")

print(f"\nTotal missing .pkl files: {total_missing_pkls}")

if not missing_directories and not directories_with_missing_pkls:
    print(
        "All expected directories exist and contain the correct number of .pkl files."
    )
