# Libary imports
import sys
import numpy as np
import matplotlib.pyplot as plt
from neuron import h, units

# Load external files & initialize
h.load_file("stdrun.hoc")

# Add path to the directory containing the .mod files
sys.path.append("/home/Marc/Documents/internship/models/Sanjay_model")

# Import the cell classes
from geom import Cell, Synapse, SynapseNMDA, Bwb

# Load external mechanism files
try:
    h.nrn_load_dll(
        "/home/Marc/Documents/internship/models/Sanjay_model/x86_64/libnrnmech.so"
    )
except:
    pass

h.tstop = 100  # Duration of the simulation in ms
h.dt = 0.025  # Time step of the simulation in ms


def vary_na_conductances_basket():
    """
    This function creates a Bwb cell and varies the sodium conductance in the soma.
    It then runs the simulation and plots the membrane potential of the soma.
    """
    # Lists to store data for each condition
    all_time_data = []
    all_voltage_data = []

    # Create a new Bwb cell
    basket_cell = Bwb(x=0, y=0, z=0, id=0)

    synapses_dict = {
        "somaAMPAf": "soma",
        "somaGABAf": "soma",
        "somaGABAss": "soma",
        "somaNMDA": "soma",
    }

    # for percent_increase in range(0, 100, 10):
    for p in np.arange(0.1, 10, 0.5):
        # gna = 0.1 + (percent_increase / 100) * 0.1

        h.t = 0  # Reset the simulation time

        # Create a new Bwb cell
        basket_cell = Bwb(x=0, y=0, z=0, id=0)

        # Adjust the sodium conductance in the Bwb cell
        basket_cell.soma(0.5).Nafbwb.gna *= p

        # Set up recording for each condition
        time_vec = h.Vector()  # Record the time
        voltage_vec = h.Vector()  # Record the membrane potential of the soma

        time_vec.record(h._ref_t)  # Records the simulation time
        voltage_vec.record(
            basket_cell.soma(0.5)._ref_v
        )  # Records the membrane potential

        # Create a dictionary to store VecStim instances and NetCons for each synapse
        vec_stim_dict = {}
        netcon_dict = {}

        np.random.seed(87)  # Set seed for reproducibility
        for synapse_name in synapses_dict:
            vec_stim = h.VecStim()  # Create a VecStim instance
            spike_times = sorted(
                np.random.uniform(0, h.tstop, 100)
            )  # Generate 100 random spike times
            spike_times = h.Vector(spike_times)  # Convert to a NEURON vector
            vec_stim.play(spike_times)  # Play the spike times

            # Access the correct synapse attribute
            synapse = getattr(basket_cell, synapse_name)

            # Connect VecStim to the synapse
            netcon = h.NetCon(
                vec_stim, synapse.syn
            )  # Connect the VecStim instance to the synapse
            netcon.weight[0] = 0.00005  # Adjust the weight as needed
            netcon.delay = 2  # Adjust the delay as needed
            netcon.threshold = 0  # Adjust the threshold as needed

            # Store the VecStim and NetCon instances in the dictionaries
            vec_stim_dict[synapse_name] = vec_stim
            netcon_dict[synapse_name] = netcon

        # Run the simulation
        h.finitialize(-65 * units.mV)  # Set the initial membrane potential
        h.continuerun(h.tstop)  # Set simulation duration

        # Store data for this condition
        all_time_data.append(np.array(time_vec))  # Convert to numpy array
        all_voltage_data.append(np.array(voltage_vec))  # Convert to numpy array

        # Clear recordings for the next iteration
        del time_vec
        del voltage_vec

        # Clear VecStim and NetCon instances for the next iteration
        for vec_stim, netcon in zip(
            vec_stim_dict.values(), netcon_dict.values()
        ):  # Loop over the values of the dictionaries
            del vec_stim
            del netcon

        # Clear Bwb cell instance
        del basket_cell

    # Plot the results for all conditions (soma only)
    for i, gna in enumerate(all_time_data):
        plt.plot(
            all_time_data[i],
            all_voltage_data[i],  # Assuming this array contains soma voltage data only
            label=f"gna = {0.1 + (gna / 100) * 0.1}",
        )

    plt.xlabel("Time (ms)")
    plt.ylabel("Membrane Potential (mV)")
    plt.title("Basket Cell Activity")
    plt.legend()
    plt.show()


# Call the function
vary_na_conductances_basket()
