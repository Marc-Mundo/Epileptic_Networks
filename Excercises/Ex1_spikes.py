# First, import the necessary libraries
import numpy as np
import matplotlib.pyplot as plt

spikes = np.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0])

# Calculate the total number of spikes and store them in totalSpikes
# Because the vector is binary, the sum of the 1s and 0s gives the total
totalSpikes = np.sum(spikes)

# Calculate the neuron’s spike count rate, and store it in spikeRate
# We divide by 10 because we want our rate to be in the unit of spikes/second (Hz)
spikeRate = totalSpikes / 10

# plot the spikes over time
plt.plot(spikes)
plt.show()

# Print the spike count rate
print("The spike count rate is: {} Hz".format(spikeRate))
