import numpy as np


def compute_fim(estimated_pose, beacons,variance):
    j = estimated_pose-beacons
    I = 1/variance * ((j*np.transpose(j))/np.square(np.norm(j)))

    return I


def compute_crlb(fim):
    C = np.inverse(fim)

    return C
