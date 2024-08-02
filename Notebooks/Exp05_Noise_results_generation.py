import sys

sys.path.append("/home/Marc/Marc_network_sims")  # path to the code with the functions

import pickle
import numpy as np
import os
import gc
from src.SanjayCode import (
    get_spike_times_for_basket_cells,
    get_convolved_signal_per_neuron,
    detect_depolarization_blocks,
)

# Base directory for data
base_data_path = "../data/Data05_External_noise"

# Noise factors, adjusted to match new double decimal format
pyr_noise_factors = [0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00, 1.10, 1.20, 1.30]

# gNa and gK values, adjusted for two decimal places in naming
gna_values = [0.50 + 0.10 * i for i in range(11)]
gk_values = [0.50 + 0.10 * i for i in range(11)]

# Directory to save results
results_save_dir = "../Results/Noise_results"

if not os.path.exists(results_save_dir):
    os.makedirs(results_save_dir)


# Function to process files, unchanged from your script
def process_noise_file(file_path):
    try:
        with open(file_path, "rb") as file:
            data = pickle.load(file)

            # Process data
            basket_spike_times = get_spike_times_for_basket_cells(data, 800, 999)
            total_duration = int(5000)  # Assuming each time step is 1ms
            convolved_signal = get_convolved_signal_per_neuron(
                basket_spike_times, total_duration
            )
            (
                depolarization_starts,
                depolarization_ends,
                threshold,
                total_depolarization_duration,
            ) = detect_depolarization_blocks(convolved_signal, total_duration)

        if (
            len(depolarization_starts) > 0
        ):  # Check if any depolarization events were detected
            # Convert numpy arrays to lists for serialization
            return (
                depolarization_starts.tolist(),
                depolarization_ends.tolist(),
                float(threshold),
                total_depolarization_duration,
            )
        else:
            return None

    except Exception as e:
        print(f"Error loading the file {file_path}: {e}")
        return None


# Process and save results for each noise level
for noise_factor in pyr_noise_factors:
    results_file_path = os.path.join(results_save_dir, f"noise_{noise_factor:.2f}.pkl")

    # Check if results already exist for this noise level
    if os.path.exists(results_file_path):
        print(f"Results for noise {noise_factor:.2f} already exist. Skipping.")
        continue

    noise_level_results = {}

    for gna in gna_values:
        for gk in gk_values:
            # Adjusted to format numbers to two decimal places in the variant
            variant = f"gna_{gna:.2f}_gk_{gk:.2f}_noise_{noise_factor:.2f}"
            data_path = os.path.join(base_data_path, variant)

            if not os.path.exists(data_path):
                continue  # Skip if the directory does not exist

            variant_results = {}  # Initialize the variant results
            for i in range(15):  # Process 15 trials for each variant
                file_name = f"{i:02}.pkl"
                file_path = os.path.join(data_path, file_name)
                file_results = process_noise_file(file_path)
                if file_results:
                    variant_results[file_name] = file_results

                gc.collect()  # Suggest manual garbage collection

            if variant_results:  # Only add to noise_level_results if there are results
                noise_level_results[variant] = variant_results

    # Proceed to save the noise-level results into a specific file only if we have new data
    if noise_level_results:  # Check if we collected any results
        try:
            with open(results_file_path, "wb") as pkl_file:
                pickle.dump(noise_level_results, pkl_file)
            print(f"Results for noise {noise_factor:.2f} saved successfully.")
        except Exception as e:
            print(f"Error saving the results file for noise {noise_factor:.2f}: {e}")
    else:
        print(f"No new results to save for noise {noise_factor:.2f}.")
