import sys

sys.path.append(
    "../",
)  # path to the src with the functions

import os
import pickle

# import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d


#################################################################
# Calculating the bursts in pyr and basket cells around the DPB #
#################################################################


def find_depolarization_block(simData, cell_range, window=100, timestep=0.1):
    """
    Find the onset time of the depolarization block across the Basket cell population.

    Parameters:
    simData (dict): Dictionary containing spike times data for each cell.
    cell_range (range): The range of GIDs for the Basket cell type to analyze.
    window (int): The window size (in ms) to consider for depolarization block detection.
    timestep (float): The timestep of the simulation in ms.

    Returns:
    float: The onset time of the depolarization block, if found. None otherwise.
    """

    # Create a timeline with all possible time points given the timestep
    timeline = np.arange(0, 5000, timestep)

    # Initialize an array to track the spiking activity at each time point
    spike_activity = np.zeros_like(timeline, dtype=int)

    # Fill the spike activity array with 1 where spikes occur
    for gid in cell_range:
        spike_times = simData[gid].spike_times
        indices = np.searchsorted(timeline, spike_times)
        spike_activity[indices] = 1

    # Search for a window of size 'window' with no spikes
    window_size = int(window / timestep)  # Convert window size to number of indices
    for i in range(len(spike_activity) - window_size):
        if np.all(spike_activity[i : i + window_size] == 0):
            # Found a window with no spikes, return the onset time
            depolarization_onset = i * timestep
            return depolarization_onset

    # No depolarization block detected
    return None


def detect_bursts(activity, threshold):
    """
    Detects bursts in the convolved activity based on a fixed threshold.
    Returns the indices of the start and end of bursts.
    """
    above_threshold = activity > threshold
    diff = np.diff(above_threshold.astype(int))
    start_indices = np.where(diff == 1)[0] + 1  # Start of burst
    end_indices = np.where(diff == -1)[
        0
    ]  # End of burst if activity ends exactly at threshold

    # Adding handling for bursts that might start at the beginning or end at the end of the activity array
    if above_threshold[0]:
        start_indices = np.insert(start_indices, 0, 0)  # If starts with a burst
    if above_threshold[-1]:
        end_indices = np.append(end_indices, len(activity) - 1)  # If ends with a burst

    valid_bursts = [
        (start, end)
        for start, end in zip(start_indices, end_indices)
        if end - start
        >= 3  # Ensuring the burst lasts for at least the duration of 3 bins
    ]
    return valid_bursts


def convolve_spike_activity_DPB_with_bursts(
    simData, depolarization_onset, window=200, resolution=1, sigma=1, fixed_threshold=1
):
    gids = {"Pyr": range(800), "Bwb": range(800, 1000)}
    time_bins = np.arange(
        depolarization_onset - window,
        depolarization_onset + window + resolution,
        resolution,
    )

    convolved_activities = {}
    burst_info = {}

    for cell_type, gid_range in gids.items():
        spike_times = np.concatenate(
            [simData[gid].spike_times for gid in gid_range if gid in simData]
        )
        spike_counts, _ = np.histogram(spike_times, bins=time_bins)
        convolved_activity = gaussian_filter1d(spike_counts, sigma=sigma / resolution)

        bursts = detect_bursts(convolved_activity, fixed_threshold)

        last_burst_before_dpb = None
        second_last_burst_before_dpb = None
        first_burst_after_dpb = None
        for start, end in bursts:
            if time_bins[start] < depolarization_onset:
                second_last_burst_before_dpb = last_burst_before_dpb
                last_burst_before_dpb = (start, end, max(convolved_activity[start:end]))
            elif (
                time_bins[start] > depolarization_onset
                and first_burst_after_dpb is None
            ):
                first_burst_after_dpb = (start, end, max(convolved_activity[start:end]))
                break  # Stop after finding the first burst after DPB

        # Adjusting the tuple values to time bins for consistency
        if last_burst_before_dpb is not None:
            last_burst_before_dpb = (
                time_bins[last_burst_before_dpb[0]],
                time_bins[last_burst_before_dpb[1]],
                last_burst_before_dpb[2],
            )
        if second_last_burst_before_dpb is not None:
            second_last_burst_before_dpb = (
                time_bins[second_last_burst_before_dpb[0]],
                time_bins[second_last_burst_before_dpb[1]],
                second_last_burst_before_dpb[2],
            )
        if first_burst_after_dpb is not None:
            first_burst_after_dpb = (
                time_bins[first_burst_after_dpb[0]],
                time_bins[first_burst_after_dpb[1]],
                first_burst_after_dpb[2],
            )

        convolved_activities[cell_type] = (time_bins[:-1], convolved_activity)
        burst_info[cell_type] = {
            "last_burst_before_dpb": last_burst_before_dpb,
            "second_last_burst_before_dpb": second_last_burst_before_dpb,
            "first_burst_after_dpb": first_burst_after_dpb,
        }

    # Return the convolved activities, burst information
    return convolved_activities, burst_info


###################################################
# Loop over all the trials in selected conditions #
###################################################


# Function to process a single trial
def process_trial(pkl_path):
    try:
        with open(pkl_path, "rb") as file:
            data = pickle.load(file)
        print(f"Data loaded successfully from {pkl_path}.")
    except Exception as e:
        print(f"Error loading the file {pkl_path}:", e)
        return None

    simData = data["simData"]
    cell_range = range(800, 1000)  # Basket Cell range

    depolarization_onset = find_depolarization_block(
        simData, cell_range, window=100, timestep=0.1
    )
    convolved_activities, burst_info = convolve_spike_activity_DPB_with_bursts(
        simData,
        depolarization_onset,
        window=200,
        resolution=0.5,
        sigma=2,
        fixed_threshold=1,
    )

    return {
        "depolarization_onset": depolarization_onset,
        "convolved_activities": convolved_activities,
        "burst_info": burst_info,
    }


# # Single condition
# # Initialize a dictionary to store the results of each trial
# results = {}

# # Define the base path for your condition
# base_path = "../data/Data05_External_noise/gna_1.00_gk_1.00_noise_1.00"

# # Loop over all trials
# for i in range(15):
#     # Generate the file path for the current trial
#     trial_file = f"{base_path}/{str(i).zfill(2)}.pkl"

#     # Process the trial and store the results
#     trial_results = process_trial(trial_file)
#     if trial_results is not None:
#         results[str(i).zfill(2)] = trial_results

# # Specify the path where you want to save the results
# output_path = "../Results/burst_analysis_results.pkl"

# if not os.path.exists(os.path.dirname(output_path)):
#     os.makedirs(os.path.dirname(output_path))

# # Dump the results dictionary into a pickle file
# with open(output_path, "wb") as output_file:
#     pickle.dump(results, output_file)

# print("Analysis completed and results saved.")

###################################################

# Multiple conditions
# List of conditions to process
conditions = [
    ("1.00", "1.00"),  # Baseline
    ("0.80", "1.20"),
    ("1.20", "0.80"),
    ("0.80", "0.80"),
    ("1.20", "1.20"),
]

# Base path for the data directory
data_base_path = "../data/Data05_External_noise"

# Initialize a dictionary to store the results of each trial for each condition
all_conditions_results = {}

for gna, gk in conditions:
    condition_name = f"gna_{gna}_gk_{gk}_noise_1.00"
    base_path = os.path.join(data_base_path, condition_name)

    # Initialize a dictionary to store the results of each trial for the current condition
    results = {}

    # Loop over all trials for the current condition
    for i in range(15):
        trial_file = f"{base_path}/{str(i).zfill(2)}.pkl"
        trial_results = process_trial(trial_file)
        if trial_results is not None:
            results[str(i).zfill(2)] = trial_results

    # Store the results for the current condition
    all_conditions_results[condition_name] = results

    print(f"Completed analysis for condition: {condition_name}.")

# Specify the path where you want to save the results for all conditions
output_path = "../Results/all_conditions_burst_analysis_results.pkl"

if not os.path.exists(os.path.dirname(output_path)):
    os.makedirs(os.path.dirname(output_path))

# Dump the results dictionary into a pickle file
with open(output_path, "wb") as output_file:
    pickle.dump(all_conditions_results, output_file)

print("Analysis for all conditions completed and results saved.")
