# Setting up the range measurements from the trajectory

from trajectory import trajectory
import numpy as np

def noisy_range(beacons):
    eta = 0.02  # Sensor noise (uncertainty)

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
