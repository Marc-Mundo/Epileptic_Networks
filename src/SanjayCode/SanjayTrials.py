# This uses the functions by sean to run over the data.
# Data contains 20 trials per run (connection strength).
import numpy as np
from .Plots import calc_lfp
import matplotlib.pyplot as plt
import seaborn as sns
from numpy.fft import rfft, rfftfreq


def my_psd(data, run):
    """Compute PSD across all trials"""
    psds = []
    for trial in range(20):
        t = f"{trial:02}"
        # Extracting pyramidal cells for each trial
        simData = data[run][t]["simData"]
        pyr_cells = [cell for _, cell in simData.items() if cell._gid < 800]
        g = calc_lfp(pyr_cells)
        N = 50_001
        SAMPLE_RATE = 1000 / 0.1
        yf = rfft(g - np.mean(g))
        xf = rfftfreq(N, 1 / SAMPLE_RATE)

        psd = np.abs(yf) ** 2
        psds.append(psd)

    return np.mean(psds, axis=0), xf


def plot_psd(data, my_runs):
    """Compute PSD for every run (various connection strengths)"""
    psds = {}
    xfs = {}
    for run in my_runs:
        print(run, end="\r")
        psd, xf = my_psd(data, run)
        psds[run] = psd[1:]
        xfs[run] = xf[1:]

    plt.figure(figsize=(15, 7))
    for run in my_runs:
        sns.lineplot(x=xf[1:], y=psds[run], label=run)
    plt.xlim([-1, 100])
    return psds, xfs


def get_theta_gamma_power(psds, xfs, my_runs):
    tfs = []
    gfs = []
    for run in my_runs:
        psd = psds[run]
        xf = xfs[run]
        tr = [3, 12]  # [2.5, 7.5]
        gr = [30, 80]  # [20, 60]

        theta_band_indices = np.where((xf >= tr[0]) & (xf <= tr[1]))
        filtered_psd = psd[theta_band_indices]
        total_power = np.sum(filtered_psd)
        tfs.append(total_power)

        gamma_band_indices = np.where((xf >= gr[0]) & (xf <= gr[1]))
        filtered_psd = psd[gamma_band_indices]
        total_power = np.sum(filtered_psd)
        gfs.append(total_power)
    return tfs, gfs
