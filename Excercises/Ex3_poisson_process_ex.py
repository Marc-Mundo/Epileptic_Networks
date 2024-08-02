# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt

# Define the probability of a spike occurring in each interval
prob = 15 / 1000
# We are sampling 1000 times/s and the neuron fires 15x/s on average

# Initiate data structure to hold the spike train
timePoints = 2 * 60 * 1000  # 2 minutes * 60s/minute * 1000 samples/second
poissonNeuron = np.zeros(timePoints)

# Create a loop to simulate each time point
for i in range(len(poissonNeuron)):
    # conditional statement to asssess if spike has occurred
    if np.random.rand() < prob:  # if a random number between 0 and 1 is < prob
        # store a 1 in poissonNeuron. This means the neuron has fired
        poissonNeuron[i] = 1

# Compute the overall spike count rate
numSpikes = sum(poissonNeuron)
# total number of action potentials in 2 minutes
print("The spike count rate was {} Hz".format(numSpikes / 2 * 60))
# 2 minutes * 60s/minute

# Plot the distribution of ISIs
# Step 1: determine the time stamps of each spike
spikeTimes = np.where(poissonNeuron == 1)[0]
# Remember the difference between = and ==
# The [0] at the end is because np.where returns two arrays and we
# only need the first one

# Step 2: Initialize data structure to hold ISIs
isi = np.zeros(len(spikeTimes) - 1)
# There will be one fewer ISI than the number of spikes

# Step 3: Loop through each pair of consecutive spikes, compute isi
# and store
for x in range(len(isi)):
    # Each ISI is the time between spike x and spike x+1
    isi[x] = spikeTimes[x + 1] - spikeTimes[x]

# Plot the ISI distribution
plt.hist(isi, 110)  # create a histogram with 110 bins
plt.xlabel("ISI (ms)")
plt.ylabel("Frequency")
plt.show()
