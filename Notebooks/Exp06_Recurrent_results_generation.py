import sys
import pickle
import numpy as np
import os
import gc

# Update the sys.path.append as needed if the location of the code has changed
sys.path.append("/home/Marc/Marc_network_sims")  # path to the code with the functions

from src.SanjayCode import (
    get_spike_times_for_basket_cells,
    get_convolved_signal_per_neuron,
    detect_depolarization_blocks,
)

# Updated base directory for data
base_data_path = "../data/Data06_Recurrent_connections"

# Basket cell recurrent connection strength
Bwb_Bwb_weights = np.array([1.00, 1.05, 1.10, 1.15, 1.20])

# gNa and gK values, adjusted for tighter range
gna_values = np.arange(0.75, 1.50, 0.25)
gk_values = np.arange(0.75, 1.50, 0.25)

# Directory to save results
results_save_dir = "../Results/Recurrent_results"

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
            return "No depolarization events"  # added this string result as otherwise there would be no results dictionary made.

    except Exception as e:
        print(f"Error loading the file {file_path}: {e}")
        return None


# Process and save results for each noise level
for bwb_bwb_weight in Bwb_Bwb_weights:
    results_file_path = os.path.join(
        results_save_dir, f"bwb_bwb_weight_{bwb_bwb_weight:.2f}.pkl"
    )

    # Check if results already exist for this basket cell weight
    if os.path.exists(results_file_path):
        print(f"Results for bwb {bwb_bwb_weight:.2f} already exist. Skipping.")
        continue

    weight_level_results = {}

    for gna in gna_values:
        for gk in gk_values:
            # New variant naming to include bwb_bwb_weight
            variant = f"gna_{gna:.2f}_gk_{gk:.2f}_bwb_bwb_weight_{bwb_bwb_weight:.2f}"
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

            if variant_results:  # Only add to weight_level_results if there are results
                weight_level_results[variant] = variant_results

    # Proceed to save the weight-level results into a specific file only if we have new data
    if weight_level_results:  # Check if we collected any results
        try:
            with open(results_file_path, "wb") as pkl_file:
                pickle.dump(weight_level_results, pkl_file)
            print(f"Results for bwb {bwb_bwb_weight:.2f} saved successfully.")
        except Exception as e:
            print(f"Error saving the results file for bwb {bwb_bwb_weight:.2f}: {e}")
    else:
        print(f"No new results to save for bwb {bwb_bwb_weight:.2f}.")
