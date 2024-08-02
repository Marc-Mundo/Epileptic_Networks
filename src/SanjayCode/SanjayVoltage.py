import numpy as np
import matplotlib.pyplot as plt


def plot_average_voltage(data, start_gid, end_gid, time_step):
    """
    Plots the average soma voltage for a range of GIDs.

    Parameters:
    - data: dict, simulation data with GIDs as keys.
    - start_gid: int, the starting GID.
    - end_gid: int, the ending GID (inclusive).
    - time_step: float, the time step in milliseconds.
    """
    basket_cell_GIDs = range(start_gid, end_gid + 1)
    all_voltages = []

    # Determine the maximum length among all voltages
    max_length = 0
    for gid in basket_cell_GIDs:
        if gid in data["simData"]:
            voltage = data["simData"][gid].soma_v
            all_voltages.append(voltage)
            if len(voltage) > max_length:
                max_length = len(voltage)
        else:
            print(f"Data for GID {gid} not found.")

    if not all_voltages:
        print("No voltage data found for the specified GIDs.")
        return

    # Pad each voltage array to have the same length and create a 2D numpy array
    padded_voltages = np.zeros((len(all_voltages), max_length))
    for i, voltage in enumerate(all_voltages):
        length = len(voltage)
        padded_voltages[i, :length] = voltage

    # Calculate the mean across all voltages
    average_voltage = np.mean(padded_voltages, axis=0)

    # Plotting
    total_sim_time = time_step * max_length
    time_points = np.linspace(0, total_sim_time, max_length)
    plt.figure(figsize=(10, 6))
    plt.plot(time_points, average_voltage)
    plt.xlabel("Time (ms)")
    plt.ylabel("Average Voltage (mV)")
    plt.title("Average Soma Voltage of Basket Cells")
    plt.grid(True)
    plt.show()

    return average_voltage


def find_sustained_blocks(voltage, threshold, duration, condition="average"):
    """
    Finds sustained blocks where the condition (either above or absolute (average) the threshold) is met.

    Parameters:
    - voltage: np.array, the voltage data.
    - threshold: float, the voltage threshold.
    - duration: int, the minimum number of consecutive time points.
    - condition: str, 'average' for depolarization, 'absolute' for absolute voltage depolarization.
    """
    if condition == "average":
        indices = np.where(voltage > threshold)[0]
    else:  # 'absolute'
        indices = np.where(voltage < threshold)[0]

    sustained_blocks = []
    start_index = None

    for i in range(len(indices) - 1):
        if start_index is None:
            start_index = indices[i]

        if indices[i + 1] != indices[i] + 1:
            if (indices[i] - start_index + 1) >= duration:
                sustained_blocks.append((start_index, indices[i]))
            start_index = None

    if start_index is not None and (indices[-1] - start_index + 1) >= duration:
        sustained_blocks.append((start_index, indices[-1]))

    return sustained_blocks


def plot_voltage_with_depolarization_blocks(
    average_voltage, sustained_blocks, threshold, time_points, time_step=0.1
):
    plt.figure(figsize=(10, 6))
    plt.plot(time_points, average_voltage, label="Average Voltage")
    depolarization_label_added = False

    for block in sustained_blocks:
        plt.axvspan(
            time_points[block[0]],
            time_points[block[1]],
            color="red",
            alpha=0.2,
            label="Depolarization Block" if not depolarization_label_added else None,
        )
        depolarization_label_added = True  # Ensure label is added only once

    plt.axhline(y=threshold, color="r", linestyle="--", label="Threshold")
    plt.xlabel("Time (ms)")
    plt.ylabel("Average Voltage (mV)")
    plt.title(
        "Average Soma Voltage of Basket Cells with Depolarization Blocks Highlighted"
    )
    plt.legend()
    plt.grid(True)
    plt.show()

    # Print block information
    for block in sustained_blocks:
        start_time = block[0] * time_step
        end_time = block[1] * time_step
        duration = (block[1] - block[0] + 1) * time_step
        print(
            f"Block from {start_time:.1f} ms to {end_time:.1f} ms, duration: {duration:.1f} ms"
        )


# Usage example
# depolarization_threshold = -40.0  # in mV
# significant_duration = 50  # Number of consecutive time points
# usual_total_time_ms = 5000
# num_usual_indices = 50000

# average_voltage = ... # Assume this is defined elsewhere
# time_step, time_points = calculate_time_step_and_points(average_voltage, usual_total_time_ms, num_usual_indices)
# sustained_blocks = find_sustained_depolarization(average_voltage, depolarization_threshold, significant_duration)
# plot_voltage_with_depolarization_blocks(average_voltage, sustained_blocks, depolarization_threshold, time_points)


# Absolute voltage
def plot_average_absolute_voltage(data, start_gid, end_gid, time_step=0.1):
    """
    Plots the average absolute soma voltage for a range of GIDs.

    Parameters:
    - data: dict, simulation data with GIDs as keys.
    - start_gid: int, the starting GID.
    - end_gid: int, the ending GID.
    - time_step: float, the time step in milliseconds.

    The function plots the average absolute soma voltage for GIDs in the specified range.
    """
    basket_cell_GIDs = range(start_gid, end_gid + 1)
    all_absolute_voltages = []  # To collect all absolute voltages

    for gid in basket_cell_GIDs:
        if gid in data["simData"]:
            absolute_voltage = np.abs(data["simData"][gid].soma_v)
            all_absolute_voltages.append(absolute_voltage)
        else:
            print(f"Data for GID {gid} not found.")

    if not all_absolute_voltages:  # Check if list is empty
        print("No voltage data found for the specified GIDs.")
        return

    average_absolute_voltage = np.mean(all_absolute_voltages, axis=0)
    total_sim_time = time_step * len(average_absolute_voltage)  # ms
    time_points = np.linspace(0, total_sim_time, len(average_absolute_voltage))

    plt.figure(figsize=(10, 6))
    plt.plot(time_points, average_absolute_voltage)
    plt.xlabel("Time (ms)")
    plt.ylabel("Average Absolute Voltage (mV)")
    plt.title("Average Absolute Soma Voltage of Basket Cells")
    plt.grid(True)
    plt.show()

    return average_absolute_voltage


def plot_absolute_voltage_depolarization_blocks(
    average_absolute_voltage,
    sustained_blocks,
    threshold,
    time_points,
    time_step=0.1,
):
    """
    Identifies and plots regions of reduced activity where the average absolute voltage
    is below a specified threshold for a significant duration.

    Parameters:
    - average_absolute_voltage: numpy array, the average absolute voltage data.
    - depolarization threshold: float, threshold for reduced activity in mV.
    - significant_duration: int, number of consecutive time points to be considered significant.
    - time_step: float, the time step in milliseconds.
    """
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(time_points, average_absolute_voltage, label="Average Absolute Voltage")

    for block in sustained_blocks:
        start_time, end_time = time_points[block[0]], time_points[block[1]]
        plt.axvspan(
            start_time,
            end_time,
            color="red",
            alpha=0.2,
            label=(
                "Reduced Activity Block"
                if not plt.gca().get_legend_handles_labels()[1]
                else ""
            ),
        )

    plt.axhline(y=threshold, color="r", linestyle="--", label="Threshold")
    plt.xlabel("Time (ms)")
    plt.ylabel("Average Absolute Voltage (mV)")
    plt.title(
        "Average Absolute Soma Voltage of Basket Cells with Reduced Activity Highlighted"
    )
    plt.legend()
    plt.grid(True)
    plt.show()

    # Print information about each block
    for block in sustained_blocks:
        start_time = block[0] * time_step
        end_time = block[1] * time_step
        duration = (block[1] - block[0] + 1) * time_step
        print(
            f"Reduced activity block from {start_time:.1f} ms to {end_time:.1f} ms, duration: {duration:.1f} ms"
        )


# Example usage (ensure 'average_absolute_voltage' is defined as a numpy array):
# plot_reduced_activity(average_absolute_voltage, 40.0, 50, 0.1)
