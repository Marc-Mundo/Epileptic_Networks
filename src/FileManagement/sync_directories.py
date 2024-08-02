import os
import shutil
import numpy as np


def sync_directories(primary_dir, secondary_dir):
    expected_pkl_files = 15
    pyr_noise_factors = [0.7 + 0.1 * i for i in range(7)]

    # Generate expected directory names
    expected_dirs = [
        f"gna_{gna:.1f}_gk_{gk:.1f}_noise_{noise:.1f}"
        for gk in np.arange(0.5, 1.6, 0.1)
        for gna in np.arange(0.5, 1.6, 0.1)
        for noise in pyr_noise_factors
    ]

    for dir_name in expected_dirs:
        primary_path = os.path.join(primary_dir, dir_name)
        secondary_path = os.path.join(secondary_dir, dir_name)

        # Ensure the directory exists in the primary directory
        if not os.path.exists(primary_path):
            if os.path.exists(secondary_path):
                # Copy the entire directory from secondary to primary if it doesn't exist in primary
                shutil.copytree(secondary_path, primary_path)
                print(f"Copied missing directory {dir_name} from secondary to primary.")
            continue

        # If the directory exists in both primary and secondary
        if os.path.exists(secondary_path):
            primary_files = set(os.listdir(primary_path))
            secondary_files = set(os.listdir(secondary_path))

            missing_files = secondary_files - primary_files
            for file in missing_files:
                if file.endswith(".pkl") and len(primary_files) < expected_pkl_files:
                    # Copy missing .pkl files to primary directory
                    shutil.copy(
                        os.path.join(secondary_path, file),
                        os.path.join(primary_path, file),
                    )
                    print(
                        f"Copied missing file {file} to {dir_name} in primary directory."
                    )

            # Check if the secondary directory has less than expected .pkl files
            if len(secondary_files) < expected_pkl_files:
                print(
                    f"Warning: {dir_name} in secondary directory has less than {expected_pkl_files} .pkl files."
                )

    print("Directory synchronization complete.")


# Example usage
primary_dir = "/path/to/primary/directory"
secondary_dir = "/path/to/secondary/directory"
sync_directories(primary_dir, secondary_dir)
