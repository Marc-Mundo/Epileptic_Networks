import numpy as np
import scipy.signal
import matplotlib.pyplot as plt


# Function to get spike times for all basket cells
def get_spike_times_for_basket_cells(data, gid_start, gid_end):
    # Retrieve and concatenate the spike times for all basket cells
    all_spike_times = [
        data["simData"][gid].spike_times
        for gid in range(gid_start, gid_end + 1)
        if gid in data["simData"]
    ]

    # Check if we have any spike times to concatenate
    if all_spike_times:
        # If we do, concatenate them
        return np.concatenate(all_spike_times)
    else:
        # Otherwise, return an empty array
        return np.array([])


def create_time_series(spike_times, total_duration, time_resolution=1):
    """
    Convert spike times to a binary time series, ensuring indices are within bounds.
    """
    time_series = np.zeros(total_duration)
    # Adjust spike times to ensure indices are within bounds
    spike_indices = (spike_times / time_resolution).astype(int)
    spike_indices = np.clip(
        spike_indices, 0, total_duration - 1
    )  # Ensure indices are within valid range
    time_series[spike_indices] = 1
    return time_series


def apply_gaussian_convolution(time_series, window_size=150, std=20):
    """
    Apply Gaussian convolution to the time series.
    """
    gaussian_window = scipy.signal.windows.gaussian(window_size, std=std)
    gaussian_window /= np.sum(gaussian_window)  # Normalize the window
    convolved_signal = np.convolve(time_series, gaussian_window, mode="same")
    return convolved_signal[:-window_size]


def get_convolved_signal_per_neuron(
    spike_times_list, total_duration, window_size=150, std=20, time_resolution=1
):
    """
    Apply Gaussian convolution to each neuron's time series individually and then sum them for the population.
    """
    summed_convolved_signal = np.zeros(total_duration - window_size)

    for neuron_spike_times in spike_times_list:
        neuron_time_series = create_time_series(
            neuron_spike_times, total_duration, time_resolution
        )
        neuron_convolved_signal = apply_gaussian_convolution(
            neuron_time_series, window_size, std
        )
        summed_convolved_signal += neuron_convolved_signal

    return summed_convolved_signal


def detect_depolarization_blocks(
    convolved_signal,
    total_duration,
    time_resolution=1,
    min_duration=100,
    exclude_start=50,
):
    """
    Detect depolarization blocks based on a threshold and a minimum duration, considering the time resolution,
    print details of each block, and return the total duration of depolarization blocks.
    """
    threshold = 0.001  # fixed threshold
    # Exclude the first 50 ms
    start_index = exclude_start // time_resolution

    crossings = np.diff((convolved_signal[start_index:] < threshold).astype(int))
    depolarization_starts = (
        np.where(crossings == 1)[0] * time_resolution + exclude_start
    )
    depolarization_ends = np.where(crossings == -1)[0] * time_resolution + exclude_start

    # Ensure depolarization_ends does not exceed total_duration
    if depolarization_ends.size > 0 and depolarization_ends[-1] > total_duration:
        depolarization_ends[-1] = total_duration

    if len(depolarization_ends) < len(depolarization_starts):
        # Adding total_duration ensures we do not exceed the signal bounds
        depolarization_ends = np.append(depolarization_ends, total_duration)

    # Check for minimum duration requirement
    valid_blocks = (depolarization_ends - depolarization_starts) >= min_duration
    depolarization_starts = depolarization_starts[valid_blocks]
    depolarization_ends = depolarization_ends[valid_blocks]

    total_depolarization_duration = np.sum(depolarization_ends - depolarization_starts)

    # Print details for each block
    for start, end in zip(depolarization_starts, depolarization_ends):
        print(
            f"Depolarization block from {start}ms to {end}ms, Duration: {end - start}ms"
        )

    print(f"Total Depolarization Duration: {total_depolarization_duration}ms")

    return (
        depolarization_starts,
        depolarization_ends,
        threshold,
        total_depolarization_duration,
    )


def plot_results(
    convolved_signal,
    depolarization_starts,
    depolarization_ends,
    threshold,
    total_duration,
    window_size=150,
    time_resolution=1,
    title="Convolved Firing Rate of Basket Cells",
):
    """
    Plot the convolved signal and depolarization blocks, taking into account the time resolution.
    """
    plt.figure(figsize=(15, 5))
    # Ensure the label is added only once
    depo_label_added = False
    for start, end in zip(depolarization_starts, depolarization_ends):
        label = "Depolarization Block" if not depo_label_added else None
        plt.axvspan(start, end, color="red", alpha=0.2, label=label)
        depo_label_added = True  # Avoid adding the label again

    plt.plot(
        np.arange(0, total_duration - window_size) * time_resolution,
        convolved_signal,
        label="Basket Cells",
        color="orange",
    )
    plt.axhline(y=threshold, color="r", linestyle="--", label="Threshold")
    plt.title(title)
    plt.xlabel("Time (ms)")
    plt.ylabel("Firing Rate (Hz)")
    plt.legend()
    plt.grid(True)
    plt.show()


# Example usage
# basket_spike_times = get_spike_times_for_basket_cells(data, 800, 1000)  # Assumes data is defined elsewhere
# total_duration = int(5000 / time_resolution)  # Adjust as needed
# time_series = create_time_series(basket_spike_times, total_duration -window_size)
# convolved_signal = apply_gaussian_convolution(time_series)
# depolarization_starts, depolarization_ends, threshold = detect_depolarization_blocks(convolved_signal, total_duration)
# plot_results(convolved_signal, depolarization_starts, depolarization_ends, threshold, total_duration)
