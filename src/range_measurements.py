# Setting up the range measurements from the trajectory

import numpy as np

from trajectory import trajectory


def noisy_range(beacons):
    sigma = 0.03  # Noise variance
    eta = sigma * np.random.randn()  # Sensor noise (uncertainty)
    # Beacon symbols defined with 'a'
    # beacon_ids = [symbol('a', i+1) for i in range(len(beacons))]

    path = trajectory()

    m, n = (np.size(path, 0), np.size(beacons, 0))

    r = np.zeros((m, n))  # Initializing range measurements

    # print("Range measurements initialized:", r.shape)

    # Making loop to calculate measurements
    for i in range(m):
        for j in range(n):
            r[i, j] = np.linalg.norm(path[i, :] - beacons[j, :]) + eta
    return r
