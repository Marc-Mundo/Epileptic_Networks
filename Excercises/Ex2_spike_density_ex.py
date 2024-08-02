# As usual, we'll begin by importing the necessary libraries
import numpy as np
import matplotlib.pyplot as plt

# Define the two average spiking rates as probabilities
p1 = 50 / 1000  # on average, 50 spikes in the 1000 time points
p2 = 15 / 1000  # on average, 15 spikes in the 1000 time points

# In order to create the data, we will create a matrix that
# is numTrials by numTimePoints in size. We will initialize
# it with zeros and then fill in the spikes later.
dataMat = np.zeros((50, 1000))

# Here, we will create a nested loop. The outer loop will
# loop through the 50 trials. The inner loop will loop through
# the time points and use a random number generator to determine
# the placement of each spike.

# Data creation loop of 50 trials
for j in range(50):
    # In each of the 50 trials, loop through 1000 time points
    for i in range(1000):
        # At each time point, we want the neuron to fire with
        # probability p1 in the first 300 ms, and probability p2
        # for the remainder of the trial.

        # To do this, we will first create a conditional to determine
        # whether or not we are in the first 300 ms. If so, we will
        # use p1, and if not, we will use p2.
        if i < 300:
            p = p1
        else:
            p = p2

        # At each time point, we flip a random coin using np.random.rand().
        # This generates a random value between 0 and 1. If this value
        # is less than our target probability, the neuron will fire.
        if np.random.rand() < p:
            dataMat[j, i] = 1

        # Note that we do not need an "else" here because the rest of the
        # matrix is already 0.

# Now that we have created our data, we can calculate the spike
# density rate.

# Sum all the trials to plot the total number of spikes in each
# time bin, and store them in counts (HINT: we wish to sum over
# all the rows, and numpy denotes rows before columns. This is
# the reason we use axis=0 (i.e. the first axis))
counts = np.sum(dataMat, axis=0)

# Now, we need to translate these counts into a rate by dividing
# by the number of trials and the dt
density = (1 / (1 / 1000)) * counts / 50

# In order to create a plot, we need to create a vector of time
# points to plot it against
time = np.arange(1000)

# Create spike density vs. time graph
plt.figure()
plt.plot(time, density)
plt.xlabel("Time in ms")
plt.ylabel("Spike density (Spikes per second)")
plt.show()
