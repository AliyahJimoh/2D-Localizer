# Trajectory simulation for robot

import numpy as np


def trajectory():

    trajectory = []

    for i in np.arange(5, 38.5, 0.5):
        trajectory.append([8, i])

    trajectory = np.array(trajectory)  # Converting to an array

    return trajectory
