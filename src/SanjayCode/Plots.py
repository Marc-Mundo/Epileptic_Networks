import numpy as np
from neuron import h
import pylab


def compute_manual_firing_rate(spike_times, stim_duration, dt):
    spike_times_list = list(spike_times)
    num_spikes = len(spike_times_list)
    total_time = (
        len(np.arange(0, stim_duration, dt)) * dt / 1000
    )  # Convert stim_duration and dt to seconds
    firing_rate = num_spikes / total_time
    return firing_rate


def compute_population_firing_rates(cells, simulation_duration, dt):
    firing_rates = [
        compute_manual_firing_rate(cell.spike_times, simulation_duration, dt)
        for cell in cells
    ]
    mean_rate, std_rate = np.mean(firing_rates), np.std(firing_rates)
    return mean_rate, std_rate


def calc_lfp(pyr_cells):
    """
    Calculate the LFP signal from the pyramidal cells.
    """

    vlfp = np.zeros((pyr_cells[0].Adend3_v.shape[0]))

    for cell in pyr_cells:
        vlfp += cell.Adend3_v
        vlfp -= cell.Bdend_v
    vlfp /= len(pyr_cells)
    return vlfp


def calc_psd(lfp):
    """
    Calculate the mean theta and gamma power of the LFP signal.

    Parameters:
    - lfp: numpy array, LFP signal
    - fs: int, sampling frequency (default is 1000 Hz)
    - tr: tuple, theta frequency range (default is (3, 12) Hz)
    - gr: tuple, gamma frequency range (default is (30, 80) Hz)

    Returns:
    - mean_theta_power: float, mean power of theta frequency range (sq-mV/Hz)
    - mean_gamma_power: float, mean power of gamma frequency range (sq-mV/Hz)
    - theta_freq: float, dominant frequency in the theta range (Hz)
    - gamma_freq: float, dominant frequency in the gamma range (Hz)
    - Pxx: numpy array, power spectral density of the LFP signal
    """

    tr = [3, 12]  # Theta frequency range
    gr = [30, 80]  # Gamma frequency range

    h.dt = 0.1  # Set the integration time step to 0.1 ms

    # Reject the first millisecond of the signal
    t0 = 200  # You can adjust this value based on your preference

    # Set the upper limit for the periodogram frequency
    fmax = 200  # Adjust as needed

    # Downsample the signal based on the chosen fmax
    div = int(1000 / h.dt / (2 * fmax))

    t0i = int(t0 / h.dt)  # Convert t0 to an index

    # Check if the length of the LFP signal is sufficient
    if t0i > len(lfp):  # You can adjust this value based on your preference
        print("LFP is too short! (<200 ms)")
        return 0, 0, 0, 0

    data = lfp[t0i::div]

    # Calculate the FFT power spectrum
    Pxx, f = pylab.psd(data - data.mean(), Fs=1000 / h.dt / div)

    # Find indices corresponding to theta and gamma frequency ranges
    tr = np.array(tr)  # Convert tr to numpy array
    gr = np.array(gr)  # Convert gr to numpy array

    theta_indices = np.where((f >= tr[0]) & (f <= tr[1]))[0]
    gamma_indices = np.where((f >= gr[0]) & (f <= gr[1]))[0]

    # Calculate mean theta and gamma power
    mean_theta_power = Pxx[theta_indices].mean() * np.diff(
        tr
    )  # integral over theta power
    mean_gamma_power = Pxx[gamma_indices].mean() * np.diff(
        gr
    )  # integral over gamma power

    # Find dominant frequencies in theta and gamma ranges
    theta_freq = f[theta_indices[np.argmax(Pxx[theta_indices])]]
    gamma_freq = f[gamma_indices[np.argmax(Pxx[gamma_indices])]]

    # print(f"Mean Theta Power: {mean_theta_power:.3e} sq-mV/Hz")
    # print(f"Mean Gamma Power: {mean_gamma_power:.3e} sq-mV/Hz")
    # print(f"Dominant Theta Frequency: {theta_freq:.2f} Hz")
    # print(f"Dominant Gamma Frequency: {gamma_freq:.2f} Hz")

    return mean_theta_power, mean_gamma_power, theta_freq, gamma_freq, Pxx
