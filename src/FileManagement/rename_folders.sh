#!/bin/bash

# Loop through all subdirectories
for dir in gna_*_gk_*_noise_*; do
    # Replace commas with periods in the folder name
    dir_replaced=$(echo "$dir" | tr ',' '.')

    # Extract values of gna, gka, and noise from the folder name
    gna=$(echo "$dir_replaced" | grep -o 'gna_[0-9.]*' | cut -d'_' -f2)
    gka=$(echo "$dir_replaced" | grep -o 'gk_[0-9.]*' | cut -d'_' -f2)
    noise=$(echo "$dir_replaced" | grep -o 'noise_[0-9.]*' | cut -d'_' -f2)

    # Round the values to one decimal place
    gna_rounded=$(printf "%.1f" "$gna")
    gka_rounded=$(printf "%.1f" "$gka")
    noise_rounded=$(printf "%.1f" "$noise")

    # Check if the values are within the specified range
    if (( $(echo "$gna_rounded >= 0.5 && $gna_rounded <= 1.5" | bc -l) )) && \
       (( $(echo "$gka_rounded >= 0.5 && $gka_rounded <= 1.5" | bc -l) )) && \
       (( $(echo "$noise_rounded >= 0.7 && $noise_rounded <= 1.3" | bc -l) )); then
        # Create the new folder name
        new_dir="gna_${gna_rounded}_gk_${gka_rounded}_noise_${noise_rounded}"

        # Rename the folder
        mv "$dir" "$new_dir"
        echo "Renamed: $dir -> $new_dir"
    else
        echo "Skipped: $dir (outside the range)"
    fi
done
