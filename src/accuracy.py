"""Accuracy Evaluation Module: Checks the accuracy (uncertainty) for each estimated pose"""

import numpy as np


def compute_fim(estimated_pose, beacons, variances):
    """
    Computes the Fisher Information Matrix (FIM) of the estimated pose
    """

    fim = np.zeros((2, 2))
    x = estimated_pose.x()  # Extract X position
    y = estimated_pose.y()  # Extract Y position
    
    # Calculate differences of each axis
    x_diff = x -  beacons[:, 0]
    y_diff = y -  beacons[:, 1]
    
    j = np.stack([x_diff, y_diff],axis=0) # 2 x 5
    # print(j.shape)
    var = 1 / variances # 5x 1
    # print(var.shape)
    norm = np.square(np.linalg.norm(j, axis=0)) # 5 x 1
    # print(norm.shape)
    fim = np.einsum("ik,jk,k->ij", j, j, var / norm)


    return fim


def compute_crlb(fim):
    """
    Computes the Cramer-Rao Lower Bound (CRLB) to evaluate uncertainty
    """
    C = np.linalg.inv(fim)

    return C
