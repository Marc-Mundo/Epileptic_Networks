#!/bin/bash

# This script runs the Python scripts for experiments 5 to 10.
# Assuming this script is always run from within the 'Marc_network_sims' directory
# and the Python scripts are located in the 'Experiments' directory, or backups directory.

# The target directory relative to 'backups'
target_directory="Marc_network_sims/Backups/Experiments"

# Check if the current directory is the target directory
if [ "$(basename "$PWD")" != "Experiments" ]; then
    # Navigate to the target directory if not already there
    cd "$target_directory" || exit
fi

# Run Python scripts for experiments 5 to 10
python Exp04_Pyr_NA_Variants.py
python Exp04_Pyr_K_Variants.py
python Exp04_OLM_NA_Variants.py
python Exp04_OLM_K_Variants.py
python Exp04_Bwb_NA_Variants.py
python Exp04_Bwb_K_Variants.py

# If the scripts are located in different directories, use full paths or cd into each directory before running the script.
