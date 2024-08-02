import numpy as np
import matplotlib.pyplot as plt
from .BatchVariants import extract_variant_type


def plot_variant_firing_rates(variant_results, variant_type, x_tick_labels):
    """
    Plot the firing rates for a specific variant (NA or K).
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    cell_types = ["pyr_mean", "bwb_mean", "olm_mean"]
    std_types = ["pyr_std", "bwb_std", "olm_std"]
    sem_types = ["pyr_sem", "bwb_sem", "olm_sem"]
    labels = ["Pyramidal", "Basket", "OLM"]
    symbols = ["o", "^", "s"]
    color_palette = plt.cm.viridis(
        np.linspace(0, 1, len(variant_results) * len(cell_types))
    )

    for dataset_idx, (dataset_name, dataset) in enumerate(variant_results.items()):
        x_values = np.arange(len(dataset))
        for cell_idx, (cell_type, std_type, sem_type, symbol, label) in enumerate(
            zip(cell_types, std_types, sem_types, symbols, labels)
        ):
            mean_rates, std_rates, sem_rates = [], [], []
            color = color_palette[dataset_idx * len(cell_types) + cell_idx]

            for condition in dataset:
                condition_means = [
                    np.mean(run_data[cell_type])
                    for run_data in dataset[condition].values()
                ]
                condition_stds = [
                    np.mean(run_data[std_type])
                    for run_data in dataset[condition].values()
                ]
                condition_sems = [
                    np.mean(run_data[sem_type])
                    for run, run_data in dataset[condition].items()
                ]
                mean_rates.append(np.mean(condition_means))
                std_rates.append(np.mean(condition_stds))
                sem_rates.append(np.mean(condition_sems))

            variant_label = extract_variant_type(dataset_name)
            ax.errorbar(
                x_values,
                mean_rates,
                # yerr=sem_rates,
                fmt=symbol,
                linestyle="-",
                color=color,
                label=f"{label} - {variant_label}",
            )

    ax.set_xlabel("Condition")
    ax.set_ylabel("Firing Rate (Hz)")
    ax.set_title(f"Cell Firing Rates in {variant_type} Variants")
    ax.legend()

    # Setting x-tick labels
    ax.set_xticks(np.arange(len(x_tick_labels)))
    ax.set_xticklabels(list(x_tick_labels.keys()))

    plt.show()


def plot_separate_cell_type_firing_rates(variant_results, variant_type, x_tick_labels):
    """
    Plot the firing rates for each cell type across all datasets within a variant.
    """
    cell_types = ["pyr_mean", "bwb_mean", "olm_mean"]
    std_types = ["pyr_std", "bwb_std", "olm_std"]
    sem_types = ["pyr_sem", "bwb_sem", "olm_sem"]
    labels = ["Pyramidal", "Basket", "OLM"]

    # Generate a color for each dataset
    colors = plt.cm.tab10(np.linspace(0, 1, len(variant_results)))

    # Create a plot for each cell type
    for cell_idx, (cell_type, std_type, sem_type, label) in enumerate(
        zip(cell_types, std_types, sem_types, labels)
    ):
        fig, ax = plt.subplots(figsize=(10, 6))
        for dataset_idx, (dataset_name, dataset) in enumerate(variant_results.items()):
            mean_rates, std_rates, sem_rates = [], [], []
            color = colors[dataset_idx]
            x_values = np.arange(len(dataset))

            for condition in dataset:
                condition_means = [
                    np.mean(run_data[cell_type])
                    for run_data in dataset[condition].values()
                ]
                condition_stds = [
                    np.mean(run_data[std_type])
                    for run_data in dataset[condition].values()
                ]
                condition_sems = [
                    np.mean(run_data[sem_type])
                    for run, run_data in dataset[condition].items()
                ]
                mean_rates.append(np.mean(condition_means))
                std_rates.append(np.mean(condition_stds))
                sem_rates.append(np.mean(condition_sems))

            variant_label = extract_variant_type(dataset_name)
            ax.errorbar(
                x_values,
                mean_rates,
                yerr=sem_rates,
                fmt="o",
                linestyle="-",
                color=color,
                label=variant_label,
            )

        ax.set_xlabel("Condition")
        ax.set_ylabel(f"Firing Rate (Hz) - {label}")
        ax.set_title(f"{label} Cell Firing Rates in {variant_type} Variants")
        ax.legend()

        # Setting x-tick labels
        ax.set_xticks(np.arange(len(x_tick_labels)))
        ax.set_xticklabels(list(x_tick_labels.keys()), rotation=45)

        plt.tight_layout()
        plt.show()


def plot_frequencies_for_variants(variant_results, variant_type, x_tick_labels):
    """
    Plot the theta and gamma frequencies for all datasets within a variant type.
    """
    # Set up the color map
    colors = plt.cm.tab10(np.linspace(0, 1, len(variant_results)))

    # Prepare x-axis data
    x_values = np.arange(len(x_tick_labels))

    # Plot for Theta Frequencies
    fig, ax_theta = plt.subplots(figsize=(10, 6))
    for dataset_idx, (dataset_name, dataset) in enumerate(variant_results.items()):
        mean_theta_freq = []
        for condition in dataset:
            condition_theta_freq = [
                np.mean(run_data["theta_frequencies"])
                for run_data in dataset[condition].values()
            ]
            mean_theta_freq.append(np.mean(condition_theta_freq))
        color = colors[dataset_idx]
        # Using extract_variant_type for legend labels
        variant_label = extract_variant_type(dataset_name)
        ax_theta.plot(
            x_values,
            mean_theta_freq,
            marker="s",
            linestyle="-",
            color=color,
            label=variant_label,
        )

    ax_theta.set_xlabel("Condition")
    ax_theta.set_ylabel("Theta Frequency (Hz)")
    ax_theta.set_title(f"Theta Frequency in {variant_type} Variants")
    ax_theta.set_xticks(x_values)
    ax_theta.set_xticklabels(list(x_tick_labels.keys()), rotation=45)
    ax_theta.legend()
    plt.tight_layout()
    plt.show()

    # Plot for Gamma Frequencies
    fig, ax_gamma = plt.subplots(figsize=(10, 6))
    for dataset_idx, (dataset_name, dataset) in enumerate(variant_results.items()):
        mean_gamma_freq = []
        for condition in dataset:
            condition_gamma_freq = [
                np.mean(run_data["gamma_frequencies"])
                for run_data in dataset[condition].values()
            ]
            mean_gamma_freq.append(np.mean(condition_gamma_freq))
        color = colors[dataset_idx]
        # Using extract_variant_type for legend labels
        variant_label = extract_variant_type(dataset_name)
        ax_gamma.plot(
            x_values,
            mean_gamma_freq,
            marker="o",
            linestyle="-",
            color=color,
            label=variant_label,
        )

    ax_gamma.set_xlabel("Condition")
    ax_gamma.set_ylabel("Gamma Frequency (Hz)")
    ax_gamma.set_title(f"Gamma Frequency in {variant_type} Variants")
    ax_gamma.set_xticks(x_values)
    ax_gamma.set_xticklabels(list(x_tick_labels.keys()), rotation=45)
    ax_gamma.legend()
    plt.tight_layout()
    plt.show()


def plot_power_for_variants(variant_results, variant_type, x_tick_labels):
    """
    Plot the theta and gamma power for all datasets within a variant type.
    """
    # Set up the color map
    colors = plt.cm.tab10(np.linspace(0, 1, len(variant_results)))

    # Prepare x-axis data
    x_values = np.arange(len(x_tick_labels))

    # Plot for Theta Power
    fig, ax_theta = plt.subplots(figsize=(10, 6))
    for dataset_idx, (dataset_name, dataset) in enumerate(variant_results.items()):
        mean_theta_power = []
        for condition in dataset:
            condition_theta_power = [
                np.mean(run_data["mean_theta_power"])
                for run_data in dataset[condition].values()
            ]
            mean_theta_power.append(np.mean(condition_theta_power))
        color = colors[dataset_idx]
        # Using extract_variant_type for legend labels
        variant_label = extract_variant_type(dataset_name)
        ax_theta.plot(
            x_values,
            mean_theta_power,
            marker="s",
            linestyle="-",
            color=color,
            label=variant_label,
        )

    ax_theta.set_xlabel("Condition")
    ax_theta.set_ylabel("Theta Power (sq-mV/Hz)")
    ax_theta.set_title(f"Theta Power in {variant_type} Variants")
    ax_theta.set_xticks(x_values)
    ax_theta.set_xticklabels(list(x_tick_labels.keys()), rotation=45)
    ax_theta.legend()
    plt.tight_layout()
    plt.show()

    # Plot for Gamma Power
    fig, ax_gamma = plt.subplots(figsize=(10, 6))
    for dataset_idx, (dataset_name, dataset) in enumerate(variant_results.items()):
        mean_gamma_power = []
        for condition in dataset:
            condition_gamma_power = [
                np.mean(run_data["mean_gamma_power"])
                for run_data in dataset[condition].values()
            ]
            mean_gamma_power.append(np.mean(condition_gamma_power))
        color = colors[dataset_idx]
        # Using extract_variant_type for legend labels
        variant_label = extract_variant_type(dataset_name)
        ax_gamma.plot(
            x_values,
            mean_gamma_power,
            marker="o",
            linestyle="-",
            color=color,
            label=variant_label,
        )

    ax_gamma.set_xlabel("Condition")
    ax_gamma.set_ylabel("Gamma Power (sq-mV/Hz)")
    ax_gamma.set_title(f"Gamma Power in {variant_type} Variants")
    ax_gamma.set_xticks(x_values)
    ax_gamma.set_xticklabels(list(x_tick_labels.keys()), rotation=45)
    ax_gamma.legend()
    plt.tight_layout()
    plt.show()
