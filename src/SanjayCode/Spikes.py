import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d


def scatter_plot(simData: dict):
    """
    Scatter plot of spike times for each cell type.
    """
    colors = {"Pyr": "blue", "Olm": "red", "Bwb": "green"}

    plt.figure(figsize=(13, 8))
    gids = {"Pyr": range(800), "Bwb": range(800, 1000), "Olm": range(1000, 1200)}
    for k, color in colors.items():
        xs = []
        ys = []
        for gid in gids[k]:
            st = simData[gid].spike_times
            xs.extend(st)
            ys.extend(np.ones_like(st) + gid)
        plt.scatter(xs, ys, color=color, marker=",", s=1, alpha=1.0)
    plt.xlabel("Time (ms)")
    plt.ylabel("Neuron ID")
    plt.title("Pyr-blue | OLM-red | Bwb-green")


def print_firing_rate(simData: dict):
    """
    Print the mean and standard deviation of the firing rates for each cell type.
    """
    pyr = []
    bwb = []
    olm = []
    for gid, cell in simData.items():
        if cell._gid < 800:
            pyr.append(cell.compute_firing_rate())
        elif 800 <= cell._gid < 1000:
            bwb.append(cell.compute_firing_rate())
        elif 1000 <= cell._gid < 1200:
            olm.append(cell.compute_firing_rate())
    print(f"Pyr :: {np.mean(pyr):.2f} Hz +- {np.std(pyr):.2f} Hz (std)")
    print(f"Bwb :: {np.mean(bwb):.2f} Hz +- {np.std(bwb):.2f} Hz (std)")
    print(f"Olm :: {np.mean(olm):.2f} Hz +- {np.std(olm):.2f} Hz (std)")


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


def plot_spike_activity_DPB(
    simData, depolarization_onset, window=100, show_ms_input=False
):
    """
    Plots the spike activity of all cell types around the depolarization onset time.

    Parameters:
    simData (dict): Dictionary containing spike times data for each cell.
    depolarization_onset (float): The onset time of the depolarization block.
    window (int): The window size (in ms) around the depolarization onset to plot.
    """
    # Define the GID ranges for each cell type
    gids = {"Pyr": range(800), "Bwb": range(800, 1000), "Olm": range(1000, 1200)}
    colors = {"Pyr": "blue", "Bwb": "green", "Olm": "red"}

    # Set up the plot
    plt.figure(figsize=(12, 8))
    plt.xlabel("Time (ms)")
    plt.ylabel("Neuron ID")
    plt.title(f"Spike activity around depolarization onset ({depolarization_onset} ms)")
    plt.xlim(depolarization_onset - window, depolarization_onset + window)
    plt.grid(True)

    # Plot the spikes for each cell type within the window
    for cell_type, gid_range in gids.items():
        color = colors[cell_type]
        for gid in gid_range:
            spike_times = simData[gid].spike_times
            # Select spike times within the window around the depolarization onset
            relevant_spikes = spike_times[
                (spike_times > depolarization_onset - window)
                & (spike_times < depolarization_onset + window)
            ]
            plt.scatter(
                relevant_spikes,
                np.full_like(relevant_spikes, gid),
                color=color,
                marker=",",
                s=1,
                alpha=0.8,
            )

    # Add a red vertical line for the depolarization onset
    plt.axvline(
        x=depolarization_onset,
        color="red",
        linestyle="--",
        label="Depolarization Onset",
    )

    if show_ms_input:
        # Add fixed vertical lines every 150 ms for medial septum input
        t0 = 0.2  # Starting time of the medial septum input
        end_time = 5000  # End time of the simulation
        interval = 150  # Interval for the vertical lines
        start_line = ((depolarization_onset - window) // interval) * interval
        label_added = False  # Flag to check if the label has been added
        for t in np.arange(start_line, end_time, interval):
            if t0 <= t <= end_time and (depolarization_onset - window) < t < (
                depolarization_onset + window
            ):
                if not label_added:
                    plt.axvline(
                        x=t,
                        color="magenta",
                        linestyle="--",
                        linewidth=2,
                        alpha=0.8,
                        label="Medial Septum Input",  # Label is added only for the first line
                    )
                    label_added = (
                        True  # Update flag to indicate the label has been added
                    )
                else:
                    plt.axvline(
                        x=t,
                        color="magenta",
                        linestyle="--",
                        linewidth=2,
                        alpha=0.8,
                        # No label for subsequent lines
                    )

    # Plot invisible points for legend
    for cell_type, color in colors.items():
        plt.scatter([], [], color=color, label=cell_type)

    plt.legend(title="Cell Type")
    plt.show()


def convolve_spike_activity_DPB(
    simData, depolarization_onset, window=100, resolution=1, sigma=1
):
    """
    Calculates and plots the convolved spike activity for each cell population around the depolarization onset.

    Parameters:
    simData (dict): Dictionary containing spike times data for each cell.
    depolarization_onset (float): The onset time of the depolarization block.
    window (int): The window size (in ms) around the depolarization onset for convolution.
    resolution (int): Temporal resolution (in ms) for spike rate calculation.
    sigma (float): Standard deviation for Gaussian filter used in convolution.
    """
    gids = {"Pyr": range(800), "Bwb": range(800, 1000), "Olm": range(1000, 1200)}
    colors = {"Pyr": "blue", "Bwb": "green", "Olm": "red"}
    time_bins = np.arange(
        depolarization_onset - window,
        depolarization_onset + window + resolution,
        resolution,
    )

    plt.figure(figsize=(12, 8))
    plt.xlabel("Time (ms)")
    plt.ylabel("Convolved Spike Rate")
    plt.title(
        f"Convolved Spike Activity around depolarization onset ({depolarization_onset} ms)"
    )
    plt.grid(True)

    for cell_type, gid_range in gids.items():
        spike_times = np.concatenate(
            [simData[gid].spike_times for gid in gid_range if gid in simData]
        )
        spike_counts, _ = np.histogram(spike_times, bins=time_bins)
        convolved_activity = gaussian_filter1d(spike_counts, sigma=sigma / resolution)

        plt.plot(
            time_bins[:-1],
            convolved_activity,
            color=colors[cell_type],
            label=f"{cell_type} population",
        )

    # Add a red vertical line for the depolarization onset
    plt.axvline(
        x=depolarization_onset,
        color="red",
        linestyle="--",
        label="Depolarization Onset",
    )

    plt.legend()
    plt.show()


def plot_spike_activity_around_block_subset(
    simData, depolarization_onset, window=30, subset_size=10
):
    """
    Plots the spike activity of a subset of cells from each type around the depolarization onset time.

    Parameters:
    simData (dict): Dictionary containing spike times data for each cell.
    depolarization_onset (float): The onset time of the depolarization block.
    window (int): The window size (in ms) around the depolarization onset to plot.
    subset_size (int): The number of cells to plot from each cell type.
    """
    # Define the GID ranges for each cell type and select a subset for each
    total_cells = {"Pyr": 800, "Bwb": 200, "Olm": 200}  # Total cells in each population
    start_gids = {
        "Pyr": 700,
        "Bwb": 800,
        "Olm": 1000,
    }  # Starting GID for each cell type
    gids = {
        cell_type: range(start_gid, start_gid + subset_size)
        for cell_type, start_gid in start_gids.items()
    }
    colors = {"Pyr": "blue", "Bwb": "green", "Olm": "red"}

    # Set up the plot
    plt.figure(figsize=(12, 8))
    plt.xlabel("Time (ms)")
    plt.ylabel("Neuron ID")
    plt.title(
        f"Spike activity around depolarization onset ({depolarization_onset} ms) - Subset of cells"
    )
    plt.xlim(depolarization_onset - window, depolarization_onset + window)
    plt.grid(True)

    # Plot the spikes for each cell type within the window
    for cell_type, gid_range in gids.items():
        color = colors[cell_type]
        for gid in gid_range:
            spike_times = simData[
                gid
            ].spike_times  # Adjusted to access 'spike_times' correctly
            # Select spike times within the window around the depolarization onset
            relevant_spikes = [
                time
                for time in spike_times
                if depolarization_onset - window < time < depolarization_onset + window
            ]
            plt.scatter(
                relevant_spikes,
                np.full_like(relevant_spikes, gid),
                color=color,
                marker=",",
                s=1,
                alpha=0.8,
            )
    # Add a red vertical line for the depolarization onset
    plt.axvline(
        x=depolarization_onset,
        color="red",
        linestyle="--",
        label="Depolarization Onset",
    )

    # Plot invisible points for legend
    for cell_type, color in colors.items():
        plt.scatter([], [], color=color, label=cell_type)

    plt.legend(title="Cell Type")
    plt.show()
