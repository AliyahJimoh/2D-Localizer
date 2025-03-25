"""Accuracy Evaluation Module: Checks the accuracy (uncertainty) for each estimated pose"""

import numpy as np


def compute_fim(estimated_pose, beacons, variances):
    """
    Computes the Fisher Information Matrix (FIM) of the estimated pose
    """

    fim = np.zeros((2, 2))
    x = estimated_pose.x()  # Extract X position
    y = estimated_pose.y()  # Extract Y position
    for i in range(len(beacons)):
        j = np.array([x - beacons[i, 0], y - beacons[i, 1]])
        # Setting up Joint FIM
        fim += 1 / variances[i] * (np.outer(j, j) / np.square(np.linalg.norm(j)))

    return fim


def compute_crlb(fim):
    """
    Computes the Cramer-Rao Lower Bound (CRLB) to evaluate uncertainty
    """
    C = np.linalg.inv(fim)

    return C
