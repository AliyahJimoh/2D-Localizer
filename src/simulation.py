"""Simulation Module: Simulates noisy range measurements from the trajectory provided"""

import numpy as np


def noisy_range(beacons, variances, trajectory):
    """
    Creates noisy measurements from ground truth
    """
    path = trajectory

    m, n = (np.size(path, 0), np.size(beacons, 0))

    r = np.zeros((m, n))  # Initializing range measurements

    # Getting variance for each beacon (sigma squared)
    sigma = np.sqrt(variances)
    eta = sigma * np.random.randn(m, n)  # Sensor noise (uncertainty)

    r = path[:, np.newaxis, :] - beacons[np.newaxis, :, :]
    n_r = np.linalg.norm(r, axis=2) + eta

    return n_r
