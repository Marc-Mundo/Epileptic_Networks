import numpy as np
import matplotlib.pyplot as plt
import pickle
import glob
import re


def load(data_path):
    "Load the data from the simulation using the data path."
    folders = glob.glob(f"{data_path}/*/")
    data = {}
    for folder in folders:
        name = folder.split("/")[-2]  # .split("_")[0]
        data[name] = {}
        for file in glob.glob(f"{folder}/*.pkl"):
            pattern = r"(\d+)"
            match = re.search(pattern, file.split("/")[-1])
            run = match.group(1)
            with open(file, "rb") as f:
                data[name][run] = pickle.load(f)
            print("Loaded:", file)
    return data


def process_data(simData):
    """Process the data from the simulation containing variants in experiment 04+"""
    from src.SanjayCode import (
        compute_population_firing_rates,
        calc_lfp,
        calc_psd,
    )

    # Define lists to store calculated information
    # init mean firing rate lists per population
    pyr_mean_firing_rates_list = []
    bwb_mean_firing_rates_list = []
    olm_mean_firing_rates_list = []

    # init std firing rate lists per population
    pyr_std_firing_rates_list = []
    bwb_std_firing_rates_list = []
    olm_std_firing_rates_list = []

    # init sem firing rate lists per population
    pyr_sem_firing_rates_list = []
    bwb_sem_firing_rates_list = []
    olm_sem_firing_rates_list = []

    # init list to store lfp data
    lfps_list = []

    # init lists to store dominant theta-gamma frequencies
    gamma_frequencies_list = []
    theta_frequencies_list = []

    # init lists to store mean theta-gamma power
    mean_gamma_power_list = []
    mean_theta_power_list = []

    # Define cell populations using list comprehensions
    pyr_cells = [cell for gid, cell in simData.items() if cell._gid < 800]
    bwb_cells = [cell for gid, cell in simData.items() if 800 <= cell._gid < 1000]
    olm_cells = [cell for gid, cell in simData.items() if 1000 <= cell._gid < 1200]

    # Compute firing rates for each population
    simulation_duration = 5000  # in milliseconds
    dt = 0.1  # time step in milliseconds
    num_trials = 20  # The number of trials for each condition, number of pickle files in the condition folder

    pyr_mean, pyr_std = compute_population_firing_rates(
        pyr_cells, simulation_duration, dt
    )
    bwb_mean, bwb_std = compute_population_firing_rates(
        bwb_cells, simulation_duration, dt
    )
    olm_mean, olm_std = compute_population_firing_rates(
        olm_cells, simulation_duration, dt
    )

    # Calculate SEMs
    pyr_sem = pyr_std / np.sqrt(num_trials)
    bwb_sem = bwb_std / np.sqrt(num_trials)
    olm_sem = olm_std / np.sqrt(num_trials)

    # Store the calculated information
    pyr_mean_firing_rates_list.append(pyr_mean)
    bwb_mean_firing_rates_list.append(bwb_mean)
    olm_mean_firing_rates_list.append(olm_mean)

    pyr_std_firing_rates_list.append(pyr_std)
    bwb_std_firing_rates_list.append(bwb_std)
    olm_std_firing_rates_list.append(olm_std)

    # Store SEM information in new lists
    pyr_sem_firing_rates_list.append(pyr_sem)
    bwb_sem_firing_rates_list.append(bwb_sem)
    olm_sem_firing_rates_list.append(olm_sem)

    # Compute LFP
    lfp = calc_lfp(pyr_cells)
    lfps_list.append(lfp)

    # Compute PSD
    mean_theta_power, mean_gamma_power, theta_freq, gamma_freq, Pxx = calc_psd(lfp)

    # Store the calculated information for PSD
    theta_frequencies_list.append(theta_freq)
    gamma_frequencies_list.append(gamma_freq)

    mean_theta_power_list.append(mean_theta_power)
    mean_gamma_power_list.append(mean_gamma_power)

    return {
        "pyr_mean": pyr_mean_firing_rates_list,
        "bwb_mean": bwb_mean_firing_rates_list,
        "olm_mean": olm_mean_firing_rates_list,
        "pyr_std": pyr_std_firing_rates_list,
        "bwb_std": bwb_std_firing_rates_list,
        "olm_std": olm_std_firing_rates_list,
        "pyr_sem": pyr_sem_firing_rates_list,
        "bwb_sem": bwb_sem_firing_rates_list,
        "olm_sem": olm_sem_firing_rates_list,
        "lfps": lfps_list,
        "gamma_frequencies": gamma_frequencies_list,
        "theta_frequencies": theta_frequencies_list,
        "mean_gamma_power": mean_gamma_power_list,
        "mean_theta_power": mean_theta_power_list,
        "Pxx": Pxx,
    }


def plot_firing_rates(results, variant, variant_type):
    """Plot the firing rates of the different cell types for each condition.

    Inputs: Dictionary of results, containing condition names as keys and pickle files as values

    Returns: None
    """
    fig, ax1 = plt.subplots(figsize=(10, 6))
    symbols = ["o", "^", "s"]  # Symbols for pyramidal, basket, and OLM cells
    colors = ["b", "g", "r"]  # Colors for pyramidal, basket, and OLM cells
    cell_types = ["pyr_mean", "bwb_mean", "olm_mean"]
    std_types = ["pyr_std", "bwb_std", "olm_std"]
    sem_types = ["pyr_sem", "bwb_sem", "olm_sem"]
    labels = ["Pyramidal", "Basket", "OLM"]

    # Prepare x-axis data
    x_values = np.arange(len(variant))

    # Iterate over the cell types
    for i, (cell_type, std_type, sem_type, symbol, color, label) in enumerate(
        zip(cell_types, std_types, sem_types, symbols, colors, labels)
    ):
        mean_rates = []
        std_rates = []
        sem_rates = []
        for condition in variant:
            condition_means = [
                np.mean(run_data[cell_type])
                for run, run_data in results[condition].items()
            ]
            condition_stds = [
                np.mean(run_data[std_type])
                for run, run_data in results[condition].items()
            ]
            condition_sems = [
                np.mean(run_data[sem_type])
                for run, run_data in results[condition].items()
            ]
            mean_rates.append(np.mean(condition_means))
            std_rates.append(np.mean(condition_stds))
            sem_rates.append(np.mean(condition_sems))

        ax1.errorbar(
            x_values,
            mean_rates,
            yerr=sem_rates,
            marker=symbol,
            linestyle="-",  # Connect the points
            color=color,
            label=label,
        )

    # Set up the plot
    ax1.set_xlabel(f"{variant_type}")
    ax1.set_ylabel("Firing Rate (Hz)")
    ax1.set_title("Individual Cell Firing Rates per Population")

    # Format x-tick labels to include both keys and values
    ax1.set_xticks(x_values)
    ax1.set_xticklabels(variant.values())
    ax1.legend()

    # Hide the primary y-axis
    ax1.yaxis.set_ticks([])  # Hide y-axis ticks
    ax1.yaxis.set_ticklabels([])  # Hide y-axis tick labels

    # Add secondary y-axis on the right side
    ax_right = ax1.twinx()
    ax_right.set_ylim(
        *ax1.get_ylim()
    )  # Ensure the secondary y-axis has the same limits

    plt.show()


def plot_theta_gamma_frequencies(results, variant, variant_type):
    """Plot the theta and gamma frequencies for each condition.

    Inputs: Dictionary of results, containing condition names as keys and pickle files as values
    """
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Prepare x-axis data
    x_values = np.arange(len(variant))

    # Extract and plot Theta and Gamma frequencies for each condition
    theta_frequencies = []
    gamma_frequencies = []

    for condition in variant:
        condition_theta = [
            np.mean(run_data["theta_frequencies"])
            for run, run_data in results[condition].items()
        ]
        condition_gamma = [
            np.mean(run_data["gamma_frequencies"])
            for run, run_data in results[condition].items()
        ]

        theta_frequencies.append(np.mean(condition_theta))
        gamma_frequencies.append(np.mean(condition_gamma))

    ax1.plot(
        x_values, theta_frequencies, marker="s", linestyle="-", label="Theta Frequency"
    )
    ax1.plot(
        x_values, gamma_frequencies, marker="o", linestyle="-", label="Gamma Frequency"
    )

    # Set up the plot
    ax1.set_xlabel(f"{variant_type}")
    ax1.set_ylabel("Frequency (Hz)")
    ax1.set_title("Change in Theta and Gamma Frequencies")
    ax1.set_xticks(x_values)
    ax1.set_xticklabels(variant.values())
    ax1.legend()

    # Hide the primary y-axis
    ax1.yaxis.set_ticks([])  # Hide y-axis ticks
    ax1.yaxis.set_ticklabels([])  # Hide y-axis tick labels

    # Add secondary y-axis on the right side
    ax_right = ax1.twinx()
    ax_right.set_ylim(
        *ax1.get_ylim()
    )  # Ensure the secondary y-axis has the same limits

    plt.show()


def plot_theta_gamma_power(results, variant, variant_type):
    """Plot the theta and gamma power for each condition.

    Input: Dictionary of results, containing condition names as keys and pickle files as values
    """
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Prepare x-axis data
    x_values = np.arange(len(variant))

    # Extract and plot Theta and Gamma power for each condition
    mean_theta_power = []
    mean_gamma_power = []

    for condition in variant:
        condition_theta_power = [
            np.mean(run_data["mean_theta_power"])
            for run, run_data in results[condition].items()
        ]
        condition_gamma_power = [
            np.mean(run_data["mean_gamma_power"])
            for run, run_data in results[condition].items()
        ]

        mean_theta_power.append(np.mean(condition_theta_power))
        mean_gamma_power.append(np.mean(condition_gamma_power))

    ax1.plot(x_values, mean_theta_power, marker="s", linestyle="-", label="Theta Power")
    ax1.plot(x_values, mean_gamma_power, marker="o", linestyle="-", label="Gamma Power")

    # Set up the plot
    ax1.set_xlabel(f"{variant_type}")
    ax1.set_ylabel("Power (sq-mV/Hz)")
    ax1.set_title("Change in Theta and Gamma Power")
    ax1.set_xticks(x_values)
    ax1.set_xticklabels(variant.values())
    ax1.legend()

    # Hide the primary y-axis
    ax1.yaxis.set_ticks([])  # Hide y-axis ticks
    ax1.yaxis.set_ticklabels([])  # Hide y-axis tick labels

    # Add secondary y-axis on the right side
    ax_right = ax1.twinx()
    ax_right.set_ylim(
        *ax1.get_ylim()
    )  # Ensure the secondary y-axis has the same limits

    plt.show()
