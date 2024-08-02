import numpy as np
import matplotlib.pyplot as plt


def analyze_single_noise_level(results_dict):
    analysis_results = {}
    total_trials_fixed = 15  # Fixed total number of trials per variant

    for variant, trials in results_dict.items():
        depolarization_events_count = 0
        total_duration = 0
        start_times_all = []  # Collect all start times
        end_times_all = []  # Collect all end times

        # Iterate through each trial for the variant
        for trial_results in trials.values():
            if trial_results:  # Check if trial_results is not None
                start_times, end_times, threshold, duration = trial_results
                # Check if there is a depolarization event and collect times
                if start_times and end_times:
                    depolarization_events_count += len(start_times)
                    start_times_all.extend(
                        start_times
                    )  # Add start times for this trial
                    end_times_all.extend(end_times)  # Add end times for this trial
                total_duration += (
                    duration  # Add the duration from this trial to the total
                )

        # Calculate the average duration for depolarization events, if any
        average_duration = (
            round(total_duration / depolarization_events_count, 1)
            if depolarization_events_count > 0
            else 0.0
        )

        # Calculate the percentage of trials with depolarization events
        percentage_depolarization_trials = (
            depolarization_events_count / total_trials_fixed * 100
        )

        # Calculate the average delay and its standard deviation for depolarization events, if any
        if start_times_all:
            average_delay = np.mean(start_times_all)
            std_delay = np.std(start_times_all)
        else:
            average_delay, std_delay = 0.0, 0.0

        # Store the comprehensive analysis results for this variant
        analysis_results[variant] = {
            "Depolarization Events": depolarization_events_count,
            "Start Times": start_times_all,
            "End Times": end_times_all,
            "Total Depolarization Duration": total_duration,
            "Average Depolarization Duration": average_duration,
            "Percentage Depolarization Trials": f"{depolarization_events_count} out of {total_trials_fixed} ({percentage_depolarization_trials:.1f}%)",
            "Average Depolarization Delay": average_delay,
            "STD Depolarization Delay": std_delay,
        }

    return analysis_results


def plot_depolarization_percentage_matrix(
    analysis_results, gna_values, gk_values, noise_level
):
    # Initialize the matrix to store the percentage of depolarization trials
    depolarization_matrix = np.zeros((len(gk_values), len(gna_values)))

    # Fill the matrix with the percentage depolarization trials data
    for i, gk in enumerate(gk_values):
        for j, gna in enumerate(gna_values):
            variant_key = f"gna_{gna:.2f}_gk_{gk:.2f}_noise_{noise_level:.2f}"
            if variant_key in analysis_results:
                # Extracting the numerical percentage value
                percentage_str = analysis_results[variant_key][
                    "Percentage Depolarization Trials"
                ]
                percentage_value = float(percentage_str.split("(")[-1].rstrip("%)"))
                depolarization_matrix[i, j] = percentage_value

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 8))
    cax = ax.matshow(depolarization_matrix, cmap="viridis", vmin=0, vmax=100)
    fig.colorbar(cax, label="Percentage of Trials", ticks=range(0, 101, 10))
    ax.set_xticks(range(len(gna_values)))
    ax.set_yticks(range(len(gk_values)))
    ax.set_xticklabels([f"{value:.2f}" for value in gna_values])
    ax.set_yticklabels([f"{value:.2f}" for value in gk_values])
    ax.xaxis.set_ticks_position("bottom")
    ax.yaxis.set_ticks_position("left")
    ax.set_xlabel("gNa (times baseline)")
    ax.set_ylabel("gK (times baseline)")
    ax.set_title(
        f"Depolarization blocks in Trials (gNa vs gK, % of Trials) - Noise Level: {noise_level:.2f}"
    )
    plt.xticks(rotation=90)

    # Annotate each cell with the percentage of depolarization trials
    for i in range(len(gk_values)):
        for j in range(len(gna_values)):
            ax.text(
                j,
                i,
                f"{depolarization_matrix[i, j]:.1f}%",
                ha="center",
                va="center",
                color="w",
            )

    plt.show()


def plot_depolarization_delay_matrix(
    analysis_results, gna_values, gk_values, noise_level
):
    max_value = 5000  # Define the maximum value for cells with 0.0, 0.0
    # Initialize the matrix to store the average delay of depolarization trials
    depolarization_delay_matrix = np.zeros((len(gk_values), len(gna_values)))
    depolarization_std_matrix = np.zeros((len(gk_values), len(gna_values)))  # For STD

    # Fill the matrix with the average delay and STD data
    for i, gk in enumerate(gk_values):
        for j, gna in enumerate(gna_values):
            variant_key = f"gna_{gna:.2f}_gk_{gk:.2f}_noise_{noise_level:.2f}"
            if variant_key in analysis_results:
                avg_delay = analysis_results[variant_key][
                    "Average Depolarization Delay"
                ]
                std_delay = analysis_results[variant_key]["STD Depolarization Delay"]
                if avg_delay == 0.0 and std_delay == 0.0:
                    depolarization_delay_matrix[i, j] = max_value
                    depolarization_std_matrix[i, j] = max_value
                else:
                    depolarization_delay_matrix[i, j] = avg_delay
                    depolarization_std_matrix[i, j] = std_delay
            else:
                depolarization_delay_matrix[i, j] = max_value
                depolarization_std_matrix[i, j] = max_value

    # Plotting for Average Delay
    fig, ax = plt.subplots(figsize=(10, 8))
    cax = ax.matshow(
        depolarization_delay_matrix, cmap="inferno_r", vmin=0, vmax=max_value
    )
    fig.colorbar(cax, label="Average Depolarization Delay (ms)")
    ax.set_xticks(range(len(gna_values)))
    ax.set_yticks(range(len(gk_values)))
    ax.set_xticklabels([f"{value:.2f}" for value in gna_values])
    ax.set_yticklabels([f"{value:.2f}" for value in gk_values])
    ax.xaxis.set_ticks_position("bottom")
    ax.yaxis.set_ticks_position("left")
    ax.set_xlabel("gNa (times baseline)")
    ax.set_ylabel("gK (times baseline)")
    ax.set_title(
        f"Depolarization Delay in Trials (gNa vs gK, Avg Delay) - Noise Level: {noise_level:.2f}"
    )
    plt.xticks(rotation=90)

    # Annotate each cell with the average delay and STD, or * for max_value
    for i in range(len(gk_values)):
        for j in range(len(gna_values)):
            value = depolarization_delay_matrix[i, j]
            if value == max_value:
                text_str = "*"
            else:
                text_str = f"{value:.1f}\n±{depolarization_std_matrix[i, j]:.1f}"
            ax.text(j, i, text_str, ha="center", va="center", color="w", fontsize=8)

    plt.show()
