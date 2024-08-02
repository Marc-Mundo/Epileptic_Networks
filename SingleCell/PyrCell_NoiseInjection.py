# This script simulates a single PyrAdr cell with noise injection.
import sys
import numpy as np
import matplotlib.pyplot as plt
from neuron import h, units

# Load external files & initialize
h.load_file("stdrun.hoc")  # Load NEURON libraries

# Add the directory containing geom.py to sys.path
sys.path.append("/home/Marc/Documents/internship/models/Sanjay_model")

# Import the cell classes
from geom import Cell, Synapse, SynapseNMDA, PyrAdr

# Load external mechanism files
try:
    h.nrn_load_dll(
        "/home/Marc/Documents/internship/models/Sanjay_model/x86_64/libnrnmech.so"
    )
except:
    pass

h.tstop = 100  # Duration of the simulation in ms
h.dt = 0.025  # Time step of the simulation in ms

# Create a PyrAdr cell
pyr_cell = PyrAdr(x=0, y=0, z=0, id=0)  # Position of the cell in space

# Set up recording
time_vec = h.Vector()  # Record the time
voltage_vec = h.Vector()  # Record the membrane potential of the soma

time_vec.record(h._ref_t)  # Records the simulation time
voltage_vec.record(
    pyr_cell.soma(0.5)._ref_v
)  # Records the membrane potential of the soma at the center

# Set up noise injection
noise_amp = 0.1  # Adjust the amplitude of the noise as needed
noise_dur = 100  # Duration of noise injection in ms, currently unused

# Create a NetStim instance to generate random spikes
net_stim = h.NetStim()  # Create a NetStim instance
net_stim.number = 1  # Number of spikes
net_stim.start = 0  # Start time of the first spike
net_stim.interval = 10  # Interval between spikes in ms
net_stim.noise = 1  # Set the NetStim instance to generate random spikes

# Create an ExpSyn synapse for noise injection
syn = h.ExpSyn(pyr_cell.soma(0.5))  # Create an ExpSyn synapse at the center of the soma

# Connect NetStim to the synapse
netcon = h.NetCon(net_stim, syn)  # Connects the NetStim instance to the synapse
netcon.weight[
    0
] = noise_amp  # determines the amplitude of the noise via the weight parameter

# Initialize the simulation
h.finitialize(-65 * units.mV)

# Run the simulation
h.continuerun(h.tstop)  # Set simulation duration

# Plot the results
plt.plot(time_vec, voltage_vec)
plt.xlabel("Time (ms)")
plt.ylabel("Membrane Potential (mV)")
plt.title("PyrAdr Cell Activity")
plt.show()
