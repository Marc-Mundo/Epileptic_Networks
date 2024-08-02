####################################################################################################
# Defaults for Sanjay code and used in plot_fft_positive_quadrant

# sampling_rate = 10000
####################################################################################################

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def plot_fft_lfp(lfps, sampling_rate):
    """
    Plots the positive quadrant of the Fourier Transform of the given Local Field Potential (LFP) data.
    Displays the magnitude spectrum in the positive frequency domain.

    Parameters:
    - lfps: numpy array, the Local Field Potential data
    - sampling_rate: float, the sampling rate at which the signal was recorded

    Returns:
    - None, this function will plot the Fourier Transform
    """

    # Perform the FFT on the LFP data
    fft_values = np.fft.fft(lfps)

    # Generate the frequency values corresponding to the FFT result
    frequencies = np.fft.fftfreq(len(fft_values), d=1 / sampling_rate)

    # Considering only the positive half since FFT is symmetric around the zero frequency
    mask = frequencies > 0
    positive_frequencies = frequencies[mask]
    positive_magnitude = np.abs(fft_values[mask])

    # Plotting the positive quadrant
    frequency_range = 80
    plt.figure(figsize=(10, 6))
    plt.plot(positive_frequencies, positive_magnitude)
    plt.title("Fourier Transform of LFP")
    plt.xlim([0, frequency_range])
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.show()


def get_label_from_key(variant_key):
    """
    Extracts the cell type from the variant key path based on the expected structure.
    The structure is expected to be 'DataXX_Celltype_X_Variants'.

    Parameters:
    variant_key (str): The key that contains path segments.

    Returns:
    str: The extracted cell type.
    """
    # Split the key by the "_" character
    parts = variant_key.split("_")
    # The cell type is expected to be the second part of the split path,
    # following the 'DataXX' part.
    celltype_part = parts[1] if len(parts) >= 3 else None
    # Extract the cell type which is between the first and the third underscore '_'
    if celltype_part:
        celltype = (
            celltype_part.split("_")[1] if "_" in celltype_part else celltype_part
        )
        return celltype
    return "Unknown"  # Return 'Unknown' if the path doesn't match the structure


def plot_average_fft_lfp(datasets, variant_key, condition_key, sampling_rate):
    """
    Plots the Fourier Transform of the average Local Field Potential (LFP) data over all trials in a specific condition.
    Displays the magnitude spectrum in the positive frequency domain.

    Parameters:
    - na_datasets: dict, contains LFP data for multiple variants and conditions
    - variant_key: string, the key to access a specific variant in the dataset
    - condition_key: string, the key to access a specific condition within the variant
    - sampling_rate: float, the sampling rate at which the signal was recorded

    Returns:
    - None, this function will plot the Fourier Transform
    """

    sum_lfps = None
    num_trials = 0

    # Loop through each trial in the specified condition and sum the LFP data
    for trial_key in datasets[variant_key][condition_key].keys():
        lfps = datasets[variant_key][condition_key][trial_key]["lfps"][0]

        if sum_lfps is None:
            sum_lfps = lfps
        else:
            sum_lfps += lfps

        num_trials += 1

    # Compute the average LFP
    avg_lfps = sum_lfps / num_trials

    # Perform FFT on the average LFP
    avg_fft_values = np.fft.fft(avg_lfps)

    # Generate frequency values
    frequencies = np.fft.fftfreq(len(avg_fft_values), d=1 / sampling_rate)

    # Only positive frequencies
    mask = frequencies > 0
    positive_frequencies = frequencies[mask]
    positive_magnitude = np.abs(avg_fft_values[mask])

    # Plot
    frequency_range = 80
    plt.figure(figsize=(10, 6))
    plt.plot(positive_frequencies, positive_magnitude)
    plt.title(
        "Fourier Transform of Average LFP across Trials for "
        + get_label_from_key(variant_key)
        + " "
        + condition_key
    )
    plt.xlim([0, frequency_range])
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.show()


def calculate_average_fft_lfp(datasets, variant_key, condition_key, sampling_rate):
    sum_lfps = None
    num_trials = 0

    for trial_key in datasets[variant_key][condition_key].keys():
        lfps = datasets[variant_key][condition_key][trial_key]["lfps"][0]

        if sum_lfps is None:
            sum_lfps = lfps
        else:
            sum_lfps += lfps

        num_trials += 1

    avg_lfps = sum_lfps / num_trials
    avg_fft_values = np.fft.fft(avg_lfps)
    frequencies = np.fft.fftfreq(len(avg_fft_values), d=1 / sampling_rate)
    mask = frequencies > 0

    return frequencies[mask], np.abs(avg_fft_values[mask])


def plot_comparative_ffts(
    datasets,
    baseline_variant_key,
    comparison_variant_keys,
    baseline_condition,
    comparison_conditions,  # Changed to a list
    sampling_rate,
):
    plt.figure(figsize=(12, 6))

    # Plot baseline
    frequencies, positive_magnitude = calculate_average_fft_lfp(
        datasets, baseline_variant_key, baseline_condition, sampling_rate
    )
    plt.plot(
        frequencies,
        positive_magnitude,
        label=get_label_from_key(baseline_variant_key) + " " + baseline_condition,
    )

    # Plot comparison datasets with multiple conditions
    for variant_key in comparison_variant_keys:
        for condition in comparison_conditions:  # Loop over each condition
            frequencies, positive_magnitude = calculate_average_fft_lfp(
                datasets, variant_key, condition, sampling_rate
            )
            plt.plot(
                frequencies,
                positive_magnitude,
                label=get_label_from_key(variant_key) + " " + condition,
            )

    plt.title("Comparative Fourier Transform of Average LFP")
    plt.xlim([0, 80])
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.legend()
    plt.show()


def calculate_average_psd_per_condition(dataset):
    average_psds = {}
    for condition, trials in dataset.items():
        psd_sum = None
        trial_count = 0
        for trial_id, trial_data in trials.items():
            if "Pxx" in trial_data:
                if psd_sum is None:
                    psd_sum = np.array(trial_data["Pxx"])
                else:
                    psd_sum += np.array(trial_data["Pxx"])
                trial_count += 1
        if trial_count > 0:
            average_psds[condition] = psd_sum / trial_count
    return average_psds


def plot_average_psd(dataset):
    average_psds = calculate_average_psd_per_condition(dataset)

    plt.figure(figsize=(10, 6))
    for condition, psd in average_psds.items():
        sns.lineplot(data=psd, label=condition)

    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power Spectrum Density (mV^2/Hz)")
    plt.title("Average Power Spectrum Density per Condition")
    plt.xlim(0, 80)
    plt.grid(True)
    plt.legend()
    plt.show()
