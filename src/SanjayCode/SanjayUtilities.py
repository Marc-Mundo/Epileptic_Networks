import numpy as np
from neuron import h
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import spectrogram


def extract_voltage_data(population):
    # Extract voltage data from the population into a list of NumPy arrays
    voltage_data = []

    for cell in population.cell:
        if hasattr(cell, "Adend3_volt") and hasattr(cell, "Bdend_volt"):
            voltage_data.append(np.array(cell.Adend3_volt) - np.array(cell.Bdend_volt))
        # Add similar conditions for other cell types if needed
        # elif hasattr(cell, 'SomeOtherAttribute'):
        #     voltage_data.append(np.array(cell.SomeOtherAttribute))

    return voltage_data


def calc_lfp_from_population(population):
    # Extract voltage data from the population
    voltage_data = extract_voltage_data(population)

    # Calculate LFP as the mean of the voltage data
    lfp = np.mean(voltage_data, axis=0)

    return lfp


def power_in_range(spectrogram, frequencies, freq_range):
    # Find indices corresponding to the specified frequency range
    indices = np.where((frequencies >= freq_range[0]) & (frequencies <= freq_range[1]))[
        0
    ]

    # Extract power within the specified frequency range from the spectrogram
    power_vector = spectrogram[indices, :]
    scalar_power = np.sum(power_vector, axis=0)

    return scalar_power, power_vector


def mean_power_in_range(spectrogram, frequencies, freq_range):
    # Find indices corresponding to the specified frequency range
    indices = np.where((frequencies >= freq_range[0]) & (frequencies <= freq_range[1]))[
        0
    ]

    # Extract power within the specified frequency range from the spectrogram
    power_vector = spectrogram[indices, :]

    # Calculate the mean power within the frequency range
    mean_power = np.mean(power_vector, axis=0)

    return mean_power


# Assuming you have loaded the pickled data and accessed the populations
# pop_list = [pyr_population, bas_population, olm_population]
# pop_names = ["pyr_population", "bas_population", "olm_population"]
# pop_colors = {'pyr_population': 'red', 'bas_population': 'green', 'olm_population': 'blue'}


def calculate_spike_times(pop_list):
    spike_times_list = []

    for pop in pop_list:
        pop_spike_times = []
        for cell_index in range(len(pop.ltimevec)):
            spike_times = pop.ltimevec[cell_index]
            pop_spike_times.append(spike_times)
        spike_times_list.append(pop_spike_times)

    return spike_times_list


def plot_single_population(pop, pop_name):
    plt.figure(figsize=(8, 6))
    plt.title(f"Raster Plot for {pop_name}")
    plt.xlabel("Time (ms)")
    plt.ylabel("Cell Index")

    for cell_index in range(len(pop.ltimevec)):
        spike_times = pop.ltimevec[cell_index]
        plt.vlines(
            spike_times, cell_index, cell_index + 1, "b"
        )  # 'b' for blue, you can customize the color

    plt.show()


def plot_all_populations(pop_list, pop_names, pop_colors):
    plt.figure(figsize=(15, 10))

    current_cell_index = 0

    for i, pop in enumerate(pop_list):
        num_cells = len(pop.ltimevec)
        for cell_index in range(num_cells):
            spike_times = pop.ltimevec[cell_index]
            plt.vlines(
                spike_times,
                current_cell_index,
                current_cell_index + 1,
                color=pop_colors[pop_names[i]],
            )
            current_cell_index += 1

    plt.title("Raster Plot for All Populations")
    plt.xlabel("Time (ms)")
    plt.ylabel("Cell Index")

    plt.show()


def calculate_population_kde(population):
    kde_data = []

    num_cells = len(population.ltimevec)

    for cell_index in range(num_cells):
        spike_times = population.ltimevec[cell_index]
        kde_data.append(spike_times)

    return kde_data


def plot_kde(kde_data, population_name):
    # Create subplots for individual populations
    fig, ax = plt.subplots(figsize=(10, 7))

    ax.set_title(f"Kernel Density Estimate for {population_name}")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Density")

    for cell_index, spike_times in enumerate(kde_data):
        sns.kdeplot(spike_times, label=f"Cell {cell_index + 1}", fill=True, ax=ax)

    plt.tight_layout()
    plt.show()


# Example usage:
# Assuming you have loaded the pickled data and accessed a population
# population = pyr_population  # replace with your actual population

# #Calculate KDE data
# kde_data = calculate_population_kde(pyr_population)

# #Plot KDE
# plot_kde(kde_data, "pyr_population")


def calculate_voltage_statistics(pop_list, pop_names):
    population_stats = []

    for pop, pop_name in zip(pop_list, pop_names):
        voltage_data = [cell.soma_volt for cell in pop.cell]
        mean_voltage = np.mean(voltage_data, axis=0)
        std_voltage = np.std(voltage_data, axis=0)

        population_stats.append(
            {"name": pop_name, "mean_voltage": mean_voltage, "std_voltage": std_voltage}
        )

    total_voltage_data = [cell.soma_volt for pop in pop_list for cell in pop.cell]
    total_mean_voltage = np.mean(total_voltage_data, axis=0)
    total_std_voltage = np.std(total_voltage_data, axis=0)

    population_stats.append(
        {
            "name": "Total",
            "mean_voltage": total_mean_voltage,
            "std_voltage": total_std_voltage,
        }
    )

    return population_stats


# Example usage:
# Assuming you have loaded the pickled data and accessed the populations
# pop_list = [pyr_population, bas_population, olm_population]
# pop_names = ["pyr_population", "bas_population", "olm_population"]

# Calculate voltage statistics
# voltage_stats = calculate_voltage_statistics(pop_list)


def plot_voltage_traces(voltage_stats):
    # Calculate the number of subplots needed
    num_subplots = len(voltage_stats)

    # Calculate the number of rows and columns for subplots
    num_rows = (num_subplots + 1) // 2  # Add 1 to handle an odd number of subplots
    num_cols = 2

    # Create subplots for individual populations
    fig, axs_voltage = plt.subplots(num_rows, num_cols, figsize=(15, 10))

    for i, (stats, axs) in enumerate(zip(voltage_stats, axs_voltage.flatten())):
        axs.set_title(f'Voltage Traces of {stats["name"]}')
        axs.set_xlabel("Time Steps")
        axs.set_ylabel("Soma Voltage (mV)")

        # Plot mean voltage with a solid line in blue
        axs.plot(
            stats["mean_voltage"],
            label=f'Mean {stats["name"]} Voltage',
            linestyle="-",
            linewidth=2,
            color="blue",
        )

        # Plot std voltage with a shaded area in light blue
        axs.fill_between(
            range(len(stats["mean_voltage"])),
            stats["mean_voltage"] - stats["std_voltage"],
            stats["mean_voltage"] + stats["std_voltage"],
            color="lightblue",
            alpha=0.4,
            label=f'Std {stats["name"]} Voltage',
        )

    plt.tight_layout()
    plt.legend()
    plt.show()


# Example usage:
# Assuming you have calculated voltage statistics using calculate_voltage_statistics
# voltage_stats = calculate_voltage_statistics(pop_list, pop_names)


def create_spectrogram(lfp_signal, sampling_rate):
    # Set the desired frequency range (adjust as needed)
    freq_range = (0, 1000)  # Example: Plot frequencies up to 100 Hz

    # Create spectrogram using scipy.signal.spectrogram
    frequencies, times, Sxx = spectrogram(lfp_signal, fs=sampling_rate, nperseg=256)

    # Find indices corresponding to the specified frequency range
    freq_indices = np.where(
        (frequencies >= freq_range[0]) & (frequencies <= freq_range[1])
    )[0]

    # Return relevant data for future use
    return frequencies[freq_indices], times, 10 * np.log10(Sxx[freq_indices, :])


def plot_spectrogram(frequencies, times, spectrogram_data):
    # Plot the spectrogram with the specified frequency range
    plt.pcolormesh(times, frequencies, spectrogram_data, shading="auto")
    plt.ylabel("Frequency [Hz]")
    plt.xlabel("Time (s)")
    plt.title("Spectrogram of LFP Signal")
    plt.colorbar(label="Power/Frequency (dB/Hz)")
    plt.show()


# Example usage:
# Assuming lfp_signal is your LFP signal and sampling_rate is the sampling rate of your signal
# lfp_signal = lfp_result  # Replace with your LFP signal
# sampling_rate = 10000  # Replace with your sampling rate
