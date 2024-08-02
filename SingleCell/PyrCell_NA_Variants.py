# This script allows for investigation of synaptic activity in a single PyrAdr cell with varying sodium conductances.
# Import the necessary modules
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


def vary_na_conductances():
    """
    This function creates a PyrAdr cell and varies the sodium conductance in the soma.
    It then runs the simulation and plots the membrane potential of the soma.
    """
    # Lists to store data for each condition
    all_time_data = []
    all_voltage_data = []

    for percent_increase in range(0, 100, 10):
        gna = 0.1 + (percent_increase / 100) * 0.1

        # Create a new PyrAdr cell for each condition
        pyr_cell = PyrAdr(x=0, y=0, z=0, id=0)

        # Adjust the sodium conductance in the specific compartment (e.g., Adend2)
        pyr_cell.Adend2(0.5).nacurrent.g = gna

        net_stim = h.NetStim()  # Create a NetStim instance
        net_stim.number = 1  # Number of spikes
        net_stim.start = 0  # Start time of the first spike
        net_stim.interval = 10  # Interval between spikes in ms
        net_stim.noise = 1  # Set the NetStim instance to generate random spikes

        syn = h.ExpSyn(
            pyr_cell.soma(0.5)
        )  # Create an ExpSyn synapse at the center of the soma
        netcon = h.NetCon(net_stim, syn)  # Connects the NetStim instance to the synapse
        noise_amp = 0.1  # Adjust the amplitude of the noise as needed
        netcon.weight[
            0
        ] = noise_amp  # Determines the amplitude of the noise via the weight parameter

        # Set up recording for each condition
        time_vec = h.Vector()  # Record the time
        voltage_vec = h.Vector()  # Record the membrane potential of the soma

        time_vec.record(h._ref_t)  # Records the simulation time
        voltage_vec.record(
            pyr_cell.soma(0.5)._ref_v
        )  # Records the membrane potential of the soma at the center

        # Initialize the simulation
        h.finitialize(-65 * units.mV)

        # Run the simulation
        h.continuerun(h.tstop)  # Set simulation duration

        # Store data for this condition
        all_time_data.append(np.array(time_vec))
        all_voltage_data.append(np.array(voltage_vec))

        # Clear recordings and cell instance for the next iteration
        del pyr_cell

    # Plot the results for all conditions
    for i, gna in enumerate(range(0, 100, 10)):
        plt.plot(
            all_time_data[i],
            all_voltage_data[i],
            label=f"gna = {0.1 + (gna / 100) * 0.1}",
        )

    plt.xlabel("Time (ms)")
    plt.ylabel("Membrane Potential (mV)")
    plt.title("PyrAdr Cell Activity")
    plt.legend()
    plt.show()


# Call the function
vary_na_conductances()
