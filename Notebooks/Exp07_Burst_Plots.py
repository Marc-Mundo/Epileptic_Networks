import numpy as np
import matplotlib.pyplot as plt
import pickle

pkl_path = (
    "/home/Marc/Marc_network_sims/Results/all_conditions_burst_analysis_results.pkl"
)

try:
    with open(pkl_path, "rb") as file:
        results_all_conditions = pickle.load(file)
    print(f"Data loaded successfully from {pkl_path}.")
except Exception as e:
    print(f"Error loading the file {pkl_path}:", e)

print(results_all_conditions.keys())
results = results_all_conditions["gna_1.00_gk_1.00_noise_1.00"]

try:
    with open(pkl_path, "rb") as file:
        results_all_conditions = pickle.load(file)
    print(f"Data loaded successfully from {pkl_path}.")
except Exception as e:
    print(f"Error loading the file {pkl_path}:", e)


def calculate_mean_and_std_activities(aligned_activities):
    """
    Calculates the mean and standard deviation of aligned activities across trials.
    Assumes that all activities are aligned to the same relative start time.
    """
    # Determine the longest time range to standardize activity lengths
    max_length = max(len(times) for times, _ in aligned_activities)
    standardized_activities = np.full((len(aligned_activities), max_length), np.nan)

    for i, (times, activities) in enumerate(aligned_activities):
        standardized_activities[i, : len(activities)] = activities

    # Calculate mean and standard deviation, ignoring NaNs
    mean_activities = np.nanmean(standardized_activities, axis=0)
    std_activities = np.nanstd(standardized_activities, axis=0)

    # Use the longest time array for x-axis
    longest_times = aligned_activities[
        np.argmax([len(times) for times, _ in aligned_activities])
    ][0]

    return longest_times, mean_activities, std_activities


def align_ictal_burst(results, cell_type, pre_post_margin=10):
    """
    Aligns the first burst after the depolarization onset for each trial for a specified cell type to their start time.
    Adds a margin around the burst for context.
    """
    aligned_activities = []

    for trial in results.values():
        burst_info = trial["burst_info"][cell_type]
        first_after = burst_info["first_burst_after_dpb"]
        conv_times, conv_activities = trial["convolved_activities"][cell_type]

        if first_after is not None:
            # Extract the relevant segment with a margin
            start_time = max(0, first_after[0] - pre_post_margin)
            end_time = first_after[1] + pre_post_margin

            segment_mask = (conv_times >= start_time) & (conv_times <= end_time)
            times_segment = (
                conv_times[segment_mask] - first_after[0]
            )  # Aligning to first burst start
            activities_segment = conv_activities[segment_mask]

            aligned_activities.append((times_segment, activities_segment))

    return aligned_activities


# Assuming 'results' is your data structure containing trial data
aligned_activities_ictal_burst = align_ictal_burst(results, "Pyr")

# Assuming 'aligned_activities_pyr_first_burst' contains your aligned activities for Pyr cells
longest_times, mean_activities, std_activities = calculate_mean_and_std_activities(
    aligned_activities_ictal_burst
)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(longest_times, mean_activities, label="Average Pyr First Burst Post-DPB")
plt.fill_between(
    longest_times,
    mean_activities - std_activities,
    mean_activities + std_activities,
    color="blue",
    alpha=0.2,
    label="Std Dev",
)

plt.title("Ictal network Bursting Activity in Pyr Population")
plt.xlabel("Time relative to first burst start (ms)")
plt.ylabel("Convolved Spike Rate (Hz)")
plt.legend()
plt.tight_layout()
plt.show()


def align_inter_ictal_bursts(results, pre_post_margin=10):
    """
    Aligns the second to last burst before depolarization for both Pyr and Bwb cells
    to the start time of the second to last Pyr burst, with a specified margin for context.
    """
    aligned_activities = {"Pyr": [], "Bwb": []}

    for trial in results.values():
        burst_info_pyr = trial["burst_info"]["Pyr"]
        second_last_before_pyr = burst_info_pyr.get("second_last_burst_before_dpb")

        # Proceed only if there's a second to last burst for Pyr cells
        if second_last_before_pyr:
            start_time_pyr = second_last_before_pyr[0]

            for cell_type in ["Pyr", "Bwb"]:
                burst_info = trial["burst_info"][cell_type]
                second_last_before = burst_info.get("second_last_burst_before_dpb")

                # Ensure alignment for both cell types, even if Bwb doesn't have a second to last burst
                conv_times, conv_activities = trial["convolved_activities"][cell_type]
                if second_last_before:
                    # For cells with a second to last burst, align precisely
                    align_start_time = second_last_before[0]
                else:
                    # For cells without a specific event, align to Pyr start time
                    align_start_time = start_time_pyr

                start_time = max(0, align_start_time - pre_post_margin)
                end_time = align_start_time + pre_post_margin

                segment_mask = (conv_times >= start_time) & (conv_times <= end_time)
                times_segment = (
                    conv_times[segment_mask] - start_time_pyr
                )  # Aligning to second last Pyr burst start
                activities_segment = conv_activities[segment_mask]

                aligned_activities[cell_type].append(
                    (times_segment, activities_segment)
                )

    return aligned_activities


# Align activities based on the second to last Pyr burst start times
aligned_activities_2nd_to_last = align_inter_ictal_bursts(results)

# Calculate mean and std for both cell types
mean_std_activities_2nd_to_last = {}
for cell_type in ["Pyr", "Bwb"]:
    mean_std_activities_2nd_to_last[cell_type] = calculate_mean_and_std_activities(
        aligned_activities_2nd_to_last[cell_type]
    )

# Plotting
plt.figure(figsize=(10, 6))

# Define colors for each cell type
colors = {"Pyr": "blue", "Bwb": "green"}

# Loop through each cell type to plot
for cell_type, color in colors.items():
    times, mean_activities, std_activities = mean_std_activities_2nd_to_last[cell_type]

    plt.plot(
        times, mean_activities, label=f"{cell_type} Mean Activity with STD", color=color
    )
    plt.fill_between(
        times,
        mean_activities - std_activities,
        mean_activities + std_activities,
        color=color,
        alpha=0.2,
    )

plt.title("inter-ictal Network Burst Activity for Pyr and Bwb populations")
plt.xlabel("Time relative Pyr burst start (ms)")
plt.ylabel("Convolved Spike Rate (Hz)")
plt.legend()
plt.tight_layout()
plt.show()


def align_pre_ictal_bursts(results, cell_types, pre_post_margin=10):
    """
    Aligns the last burst before the depolarization onset for each trial for specified cell types to the depolarization onset.
    Adds a margin around the burst for context.
    """
    aligned_activities = {cell_type: [] for cell_type in cell_types}

    for trial in results.values():
        depo_onset = trial["depolarization_onset"]

        for cell_type in cell_types:
            burst_info = trial["burst_info"][cell_type]
            last_before = burst_info["last_burst_before_dpb"]
            conv_times, conv_activities = trial["convolved_activities"][cell_type]

            if last_before is not None:
                # Extract the relevant segment with a margin
                start_time = max(0, last_before[0] - pre_post_margin)
                end_time = min(last_before[1] + pre_post_margin, depo_onset)

                segment_mask = (conv_times >= start_time) & (conv_times <= end_time)
                times_segment = (
                    conv_times[segment_mask] - depo_onset
                )  # Aligning to depolarization onset
                activities_segment = conv_activities[segment_mask]

                aligned_activities[cell_type].append(
                    (times_segment, activities_segment)
                )

    return aligned_activities


# Cell types to consider
cell_types = ["Pyr", "Bwb"]

# Assuming 'results' is your data structure containing trial data
aligned_activities_pre_dpb = align_pre_ictal_bursts(results, cell_types)

# Calculate mean and std for both cell types directly without needing to adjust them post-hoc
mean_std_activities_pre_dpb = {}
for cell_type in ["Pyr", "Bwb"]:
    mean_std_activities_pre_dpb[cell_type] = calculate_mean_and_std_activities(
        aligned_activities_pre_dpb[cell_type]
    )

# Plotting
plt.figure(figsize=(10, 6))

# Define colors for each cell type for consistency
colors = {"Pyr": "blue", "Bwb": "green"}

# Loop through each cell type to plot
for cell_type, color in colors.items():
    times, mean_activities, std_activities = mean_std_activities_pre_dpb[cell_type]

    # Plot mean activities
    plt.plot(times, mean_activities, label=f"{cell_type} Mean Activity", color=color)

    # Plotting the standard deviation area
    plt.fill_between(
        times,
        mean_activities - std_activities,
        mean_activities + std_activities,
        color=color,
        alpha=0.2,
    )

plt.title("Pre-ictal Network Burst Activity for Pyr and Bwb populations")
plt.xlabel("Time relative to depolarization onset (ms)")
plt.ylabel("Convolved Spike Rate (Hz)")
plt.legend()
plt.tight_layout()
plt.show()


# Plot all together
# Set up a figure for subplots
fig, axes = plt.subplots(
    1, 3, figsize=(24, 6)
)  # 1 row, 3 columns, and custom figure size

# Define colors for each cell type for consistency across plots
colors = {"Pyr": "blue", "Bwb": "green"}

# Inter-ictal Plot
# Assuming mean_std_activities for inter-ictal are prepared similarly to your last plot's preparation
for cell_type, color in colors.items():
    times, mean_activities, std_activities = mean_std_activities_2nd_to_last[
        cell_type
    ]  # For inter-ictal
    axes[0].plot(
        times, mean_activities, label=f"{cell_type} Mean Activity + STD", color=color
    )
    axes[0].fill_between(
        times,
        mean_activities - std_activities,
        mean_activities + std_activities,
        color=color,
        alpha=0.2,
    )

axes[0].set_title("Inter-ictal Network Burst Activity")
axes[0].set_xlabel("Time relative to Pyr burst start (ms)")
axes[0].set_ylabel("Convolved Spike Rate (Hz)")
axes[0].legend()

# Pre-ictal Plot
# Assuming mean_std_activities for pre-ictal are prepared from your 'aligned_activities_last_burst' for each cell type
for cell_type, color in colors.items():
    times, mean_activities, std_activities = mean_std_activities_pre_dpb[
        cell_type
    ]  # For pre-ictal
    axes[1].plot(
        times, mean_activities, label=f"{cell_type} Mean Activity + STD", color=color
    )
    axes[1].fill_between(
        times,
        mean_activities - std_activities,
        mean_activities + std_activities,
        color=color,
        alpha=0.2,
    )

axes[1].set_title("Pre-ictal Network Burst Activity")
axes[1].set_xlabel("Time relative to depolarization onset (ms)")
axes[1].legend()

# Ictal Plot
# Assuming 'aligned_activities_ictal_burst' and its processing for the ictal plot
# Here you would use the results from your 'calculate_mean_and_std_activities' directly for the ictal activity
times, mean_activities, std_activities = calculate_mean_and_std_activities(
    aligned_activities_ictal_burst
)
axes[2].plot(
    times, mean_activities, label="Pyr Mean Activity + STD", color=colors["Pyr"]
)
axes[2].fill_between(
    times,
    mean_activities - std_activities,
    mean_activities + std_activities,
    color=colors["Pyr"],
    alpha=0.2,
)

axes[2].set_title("Ictal Network Burst Activity")
axes[2].set_xlabel("Time relative to first burst post depolarization (ms)")
axes[2].legend()

plt.tight_layout()
plt.show()
