# Setting up the range measurements from the trajectory

import numpy as np

from trajectory import trajectory


def noisy_range(beacons, variances):
    path = trajectory()

    m, n = (np.size(path, 0), np.size(beacons, 0))

    r = np.zeros((m, n))  # Initializing range measurements

    # Getting variance for each beacon (sigma squared)

    # Making loop to calculate measurements
    for i in range(m):  # Rows (num. of positions)
        for j in range(n):  # Num. of beacons
            sigma = np.sqrt(variances[j])
            eta = sigma * np.random.randn()  # Sensor noise (uncertainty)
            r[i, j] = np.linalg.norm(path[i, :] - beacons[j, :]) + eta
    return r
