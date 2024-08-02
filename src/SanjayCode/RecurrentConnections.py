import numpy as np
import matplotlib.pyplot as plt


def analyze_single_RC_strength(results_dict):
    analysis_results = {}
    total_trials_fixed = (
        15  # Fixed total number of trials per variant, for context if needed
    )

    for variant, trials in results_dict.items():
        depolarization_events_count = 0  # Count of depolarization events
        total_duration = 0
        start_times_all = []  # Collect all start times
        end_times_all = []  # Collect all end times
        trials_with_no_events = 0  # Count trials with "No depolarization events"

        # Iterate through each trial for the variant
        for trial_results in trials.values():
            if trial_results == "No depolarization events":
                trials_with_no_events += 1  # Increment count of trials without events
            else:
                # Process trials with depolarization events
                start_times, end_times, _, duration = trial_results
                depolarization_events_count += len(start_times)
                start_times_all.extend(start_times)
                end_times_all.extend(end_times)
                total_duration += duration

        # Calculate the average duration for depolarization events, if any
        average_duration = (
            round(total_duration / depolarization_events_count, 1)
            if depolarization_events_count > 0
            else 0.0
        )

        # Calculate the percentage of trials with depolarization events
        percentage_depolarization_trials = (
            (total_trials_fixed - trials_with_no_events) / total_trials_fixed * 100
        )

        # Calculate the average delay and its standard deviation for depolarization events, if any
        if start_times_all:
            average_delay = np.mean(start_times_all)
            std_delay = np.std(start_times_all)
        else:
            average_delay, std_delay = 0.0, 0.0

        # Store the comprehensive analysis results for this variant
        analysis_results[variant] = {
            "Depolarization Events Count": depolarization_events_count,
            "Start Times": start_times_all,
            "End Times": end_times_all,
            "Total Depolarization Duration": total_duration,
            "Average Depolarization Duration": average_duration,
            "Percentage Depolarization Trials": f"{total_trials_fixed - trials_with_no_events} out of {total_trials_fixed} ({percentage_depolarization_trials:.1f}%)",
            "Average Depolarization Delay": average_delay,
            "STD Depolarization Delay": std_delay,
        }

    return analysis_results


def plot_rc_depolarization_percentage_matrix(
    analysis_results, gna_values, gk_values, bwb_weights
):
    # Initialize the matrix to store the percentage of depolarization trials for each bwb_weight
    depolarization_matrices = {
        bwb: np.zeros((len(gk_values), len(gna_values))) for bwb in bwb_weights
    }

    # Fill the matrices with the percentage depolarization trials data
    for bwb_weight in bwb_weights:
        for i, gk in enumerate(gk_values):
            for j, gna in enumerate(gna_values):
                variant_key = (
                    f"gna_{gna:.2f}_gk_{gk:.2f}_bwb_bwb_weight_{bwb_weight:.2f}"
                )
                if variant_key in analysis_results:
                    # Extracting the numerical percentage value
                    percentage_str = analysis_results[variant_key][
                        "Percentage Depolarization Trials"
                    ]
                    percentage_value = float(percentage_str.split("(")[-1].rstrip("%)"))
                    depolarization_matrices[bwb_weight][i, j] = percentage_value

    # Plotting for each bwb_weight
    for bwb_weight, depolarization_matrix in depolarization_matrices.items():
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
            f"Depolarization blocks in Trials (gNa vs gK, % of Trials) - RC Strength: {bwb_weight:.2f}"
        )
        plt.xticks(rotation=90)

        # Annotate each cell with the percentage of depolarization trials
        for i in range(len(gk_values)):
            for j in range(len(gna_values)):
                text_color = "w" if depolarization_matrix[i, j] < 50 else "black"
                ax.text(
                    j,
                    i,
                    f"{depolarization_matrix[i, j]:.1f}%",
                    ha="center",
                    va="center",
                    color=text_color,
                )

        plt.show()


def plot_rc_depolarization_events_matrix(
    analysis_results, gna_values, gk_values, bwb_weights
):
    # Initialize the matrix to store the count of depolarization events for each bwb_weight
    depolarization_matrices = {
        bwb: np.zeros((len(gk_values), len(gna_values))) for bwb in bwb_weights
    }

    # Fill the matrices with the depolarization events count data
    for bwb_weight in bwb_weights:
        for i, gk in enumerate(gk_values):
            for j, gna in enumerate(gna_values):
                variant_key = (
                    f"gna_{gna:.2f}_gk_{gk:.2f}_bwb_bwb_weight_{bwb_weight:.2f}"
                )
                if variant_key in analysis_results:
                    # Extracting the count of depolarization events
                    events_count = analysis_results[variant_key][
                        "Depolarization Events Count"
                    ]
                    depolarization_matrices[bwb_weight][i, j] = events_count

    # Plotting for each bwb_weight
    for bwb_weight, depolarization_matrix in depolarization_matrices.items():
        fig, ax = plt.subplots(figsize=(10, 8))
        max_events = np.max(depolarization_matrix)
        cax = ax.matshow(depolarization_matrix, cmap="viridis", vmin=0, vmax=max_events)
        fig.colorbar(cax, label="Count of Depolarization Events")
        ax.set_xticks(range(len(gna_values)))
        ax.set_yticks(range(len(gk_values)))
        ax.set_xticklabels([f"{value:.2f}" for value in gna_values])
        ax.set_yticklabels([f"{value:.2f}" for value in gk_values])
        ax.xaxis.set_ticks_position("bottom")
        ax.yaxis.set_ticks_position("left")
        ax.set_xlabel("gNa (times baseline)")
        ax.set_ylabel("gK (times baseline)")
        ax.set_title(
            f"Depolarization Events Count (gNa vs gK) - RC Strength: {bwb_weight:.2f}"
        )
        plt.xticks(rotation=90)

        # Annotate each cell with the count of depolarization events
        for i in range(len(gk_values)):
            for j in range(len(gna_values)):
                text_color = (
                    "w" if depolarization_matrix[i, j] < max_events * 0.5 else "black"
                )
                ax.text(
                    j,
                    i,
                    int(depolarization_matrix[i, j]),
                    ha="center",
                    va="center",
                    color=text_color,
                )

        plt.show()
