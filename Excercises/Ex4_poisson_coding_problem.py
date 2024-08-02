"""
Part a. Create a Poisson spike train to simulate a neuron that fires for 2000 ms at an average rate of 50 Hz. 
The Poisson distribution is a useful concept to create random spike locations within a time frame (2000 ms in this case) that produce an average desired frequency (50 Hz in this case). 
The randomness can be achieved by using the np.random.rand() function, which generates a random value uniformly sampled between 0 and 1. 
If this random value is less than the specified probability of firing, than the code will generate a 1 indicating a spike. 
Otherwise, the spike train will contain zeros.
Part b Using the following code template, add a counting variable to measure the number of spikes produced in the simulation. 
Use this total spike count to calculate the final spike count rate (spikes/second, or Hz) and see how it compares to the desired frequency of 50 Hz (50 spikes/second).
"""

# Part A: Creating a Poisson Spike Train
"""
1. Initialize the time vector (timeVec): Since the simulation runs for 2000 ms and we want to simulate each millisecond, we should create an array from 0 to 1999.
2. Set the firing probability: For an average rate of 50 Hz over 2000 ms, the probability of firing at any given millisecond is 50 spikes per second. 
This means in 1 ms, the probability is 50/1000.
3. Initialize the spikes array: This array will hold 1s and 0s, representing spikes and no spikes respectively.
"""
# Part B: Counting Spikes and Calculating Spike Rate
"""
1. Loop through each time point: We'll iterate over the timeVec array, and at each point, decide whether there's a spike or not.
2. Count the spikes and calculate the spike rate: After the loop, we'll count the number of spikes and then calculate the rate in Hz.
"""

# The resulting code
"""
The following code will generate a Poisson spike train and then calculate and display the actual firing rate of the neuron, comparing it to the desired 50 Hz rate. 
The randomness inherent in the Poisson process means the actual rate might not be exactly 50 Hz, but it should be close on average.
"""

# Import the necessary libraries
import matplotlib.pyplot as plt
import numpy as np

# Initialize data structures
timeVec = np.arange(2000)  # Time vector for 2000 ms

# Probability of a spike in each ms for a desired rate of 50 Hz
probability = 50 / 1000

# Initialize spikes array with default value zero
spikes = np.zeros(2000)

# Loop through each time point
for i in range(2000):
    if np.random.rand() < probability:
        spikes[i] = 1  # Set to 1 if there's a spike

# Compute the spike count rate
spikeCountRate = np.sum(spikes) / (2000 / 1000)  # Spikes per second

# Print the spike count rate
print("The firing rate was: {} Hz".format(spikeCountRate))

# Create a figure of the spike train
plt.figure()
plt.plot(timeVec, spikes)
plt.title("Spikes versus Time")
plt.xlabel("Time (ms)")
plt.ylabel("Spikes")
plt.show()
