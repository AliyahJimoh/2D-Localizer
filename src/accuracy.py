import numpy as np


def compute_fim(estimated_pose, beacons,variance):
    j = estimated_pose-beacons
    fim = 1/variance * ((j*np.transpose(j))/np.square(np.norm(j)))

    return fim


def compute_crlb(fim):
    C = np.inverse(fim)

    return C
