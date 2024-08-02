import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines


def get_sorted_spike_times_for_pyr_cells(data, gid_start=0, gid_end=799):
    """
    Collects the spike times for Pyr cells and sorts them for each cell.
    """
    # Initialize a dictionary to hold sorted spike times for each Pyr cell
    sorted_spike_times_per_cell = {}

    # Loop through the GID range for Pyr cells
    for gid in range(gid_start, gid_end + 1):
        if gid in data["simData"]:
            # Sort the spike times for this cell and store them in the dictionary
            sorted_spike_times_per_cell[gid] = np.sort(data["simData"][gid].spike_times)

    return sorted_spike_times_per_cell


def calculate_interspike_intervals(sorted_spike_times_per_cell: dict) -> dict:
    """
    Calculates the interspike intervals for each Pyramidal (Pyr) cell.

    Parameters:
    - sorted_spike_times_per_cell: dict
      A dictionary with cell GIDs as keys and arrays of sorted spike times as values.

    Returns:
    - interspike_intervals_per_cell: dict
      A dictionary with cell GIDs as keys and arrays of interspike intervals as values.
    """
    interspike_intervals_per_cell = {}
    for gid, spike_times in sorted_spike_times_per_cell.items():
        # Calculate the differences between consecutive spike times to get the interspike intervals
        interspike_intervals = np.diff(spike_times)
        interspike_intervals_per_cell[gid] = interspike_intervals
    return interspike_intervals_per_cell


def calculate_isi_stats(interspike_intervals_per_cell: dict) -> dict:
    """
    Calculates the mean, standard deviation, and coefficient of variation for interspike intervals of each Pyramidal (Pyr) cell.

    Parameters:
    - interspike_intervals_per_cell: dict
      A dictionary with cell GIDs as keys and arrays of interspike intervals as values.

    Returns:
    - isi_stats: dict
      A dictionary with cell GIDs as keys and dictionaries of ISI stats as values.
    """
    isi_stats = {}
    for gid, interspike_intervals in interspike_intervals_per_cell.items():
        if len(interspike_intervals) == 0:
            # Handle empty arrays
            mean_isi, std_isi, cv_isi = np.nan, np.nan, np.nan
        else:
            # Convert interspike_intervals to a higher precision before calculations
            interspike_intervals = interspike_intervals.astype(np.float64)

            # Calculate the mean, standard deviation, and coefficient of variation for the interspike intervals
            mean_isi = np.mean(interspike_intervals)
            std_isi = np.std(interspike_intervals)
            cv_isi = (
                std_isi / mean_isi if mean_isi != 0 else np.nan
            )  # Avoid division by zero

        isi_stats[gid] = {
            "mean": mean_isi,
            "std": std_isi,
            "cv": cv_isi,
        }
    return isi_stats


def plot_isi_histogram(interspike_intervals: np.array, bins=100):
    """
    Plots a histogram of interspike intervals.

    Parameters:
    - interspike_intervals: np.array
      An array of interspike intervals.
    - bins: int
      The number of bins to use for the histogram.
    """

    plt.hist(interspike_intervals, bins=bins)
    plt.xlabel("Interspike Interval (ms)")
    plt.ylabel("Count")
    plt.title("Interspike Interval Histogram")
    plt.xlim(0, 150)
    plt.show()


def detect_bursts(
    spike_times,
    gid_start,
    gid_end,
    trial_end=5000,
    window_size=5,
    burst_onset_threshold=3,
):
    """
    Detect bursts in spike times data, returning burst onset and offset times, and burst times per cell.

    :param spike_times: Dictionary with gids as keys and lists of sorted spike times as values.
    :param gid_start: The starting gid for pyramidal cells.
    :param gid_end: The ending gid for pyramidal cells.
    :param trial_end: The maximum trial time index.
    :param window_size: The size of the sliding window in milliseconds.
    :param burst_onset_threshold: The minimum number of cells that need to fire to consider it a burst onset.
    :return: Tuple of (list of (onset, offset) times, dictionary of burst times per cell).
    """
    bursts = []
    burst_times_per_cell = {gid: [] for gid in range(gid_start, gid_end + 1)}
    in_burst = False
    burst_start_time = None

    for start_time in range(trial_end - window_size + 1):
        window_end = start_time + window_size
        active_cells = 0
        active_cells_in_window = []

        # Check each cell for activity within the current window
        for gid in range(gid_start, gid_end + 1):
            times = spike_times.get(gid, [])
            for time in times:
                if start_time <= time < window_end:
                    active_cells += 1
                    active_cells_in_window.append(gid)
                    break  # Break to ensure a cell is only counted once per window

        # Check for burst onset
        if not in_burst and active_cells >= burst_onset_threshold:
            in_burst = True
            burst_start_time = start_time

        # Check for burst offset
        elif in_burst and active_cells < burst_onset_threshold:
            in_burst = False
            bursts.append((burst_start_time, start_time))
            burst_start_time = None

        # Record active cells in burst
        if in_burst:
            for gid in active_cells_in_window:
                burst_times_per_cell[gid].append(start_time)

    # Handle case where burst continues until the end of the trial
    if in_burst:
        bursts.append((burst_start_time, trial_end))

    return bursts, burst_times_per_cell


def plot_raster_with_bursts(
    spike_times,
    burst_times_per_cell,
    depolarization_onset,
    gid_start,
    gid_end,
    window=100,
):
    """
    Plot a raster of spikes and highlight spikes that are part of bursts, using the updated burst detection format.

    :param spike_times: Dictionary with gids as keys and lists of sorted spike times as values.
    :param burst_times: List of tuples representing burst (onset, offset) times.
    :param burst_times_per_cell: Dictionary of burst times per cell.
    :param depolarization_onset: The onset time of the depolarization block.
    :param gid_start: The starting gid for pyramidal cells.
    :param gid_end: The ending gid for pyramidal cells.
    :param window: The window around the depolarization onset to display in the plot.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot each spike
    for gid in range(gid_start, gid_end + 1):
        times = spike_times.get(gid, [])
        for time in times:
            # Determine if this spike is part of a burst for this cell
            is_burst_spike = time in burst_times_per_cell[gid]
            color = "r" if is_burst_spike else "b"
            ax.plot(time, gid, "|", color=color, markersize=10 if is_burst_spike else 5)

    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("GID")
    ax.set_yticks(
        range(gid_start, gid_end + 1)
    )  # Set y-ticks to cover the range of GIDs

    ax.get_yaxis().set_major_formatter(
        plt.FuncFormatter(lambda x, _: f"{int(x)}")
    )  # Format y-tick labels as integers
    ax.set_title("Spike Raster Plot with Burst Detection")

    plt.xlim(depolarization_onset - window, depolarization_onset + window)

    # Add a red vertical line for the depolarization onset
    plt.axvline(x=depolarization_onset, color="magenta", linestyle="-")

    # Manually create legend items
    spike_line = mlines.Line2D(
        [], [], color="blue", marker="|", linestyle="None", markersize=5, label="Spike"
    )
    burst_line = mlines.Line2D(
        [],
        [],
        color="red",
        marker="|",
        linestyle="None",
        markersize=10,
        label="Burst Spike",
    )
    depol_line = mlines.Line2D(
        [],
        [],
        color="magenta",
        linestyle="-",
        label=f"DPB Onset ({depolarization_onset} ms)",
    )

    # Create a legend
    ax.legend(handles=[spike_line, burst_line, depol_line], loc="best")
    plt.show()
