"""Simulation Module: Simulates noisy range measurements from the trajectory provided"""

import numpy as np


def noisy_range(beacons, variances, trajectory):
    """
    Creates noisy measurements from ground truth
    """
    path = trajectory[:,:2]
    # path = trajectory

    m, n = (np.size(path, 0), np.size(beacons, 0))

    r = np.zeros((m, n))  # Initializing range measurements

    # Getting variance for each beacon (sigma squared)
    sigma = np.sqrt(variances)
    eta = sigma * np.random.randn(m, n)  # Sensor noise (uncertainty)

    r = path[:, np.newaxis, :] - beacons[np.newaxis, :, :]
    n_r = np.linalg.norm(r, axis=2) + eta

    return n_r

def fm_robot(trajectory, fm_map):
    """
    Crates the fiducial marker pose with respect to the robot's frame of reference
    """
    
    x_r, y_r,theta_r = trajectory
    x_fm, y_fm,_ = fm_map
    
    # Relative vector (world frame)
    dx = x_fm - x_r
    dy = y_fm - y_r

    # Rotate into robot frame
    x_local =  np.cos(theta_r) * dx + np.sin(theta_r) * dy
    y_local = -np.sin(theta_r) * dx + np.cos(theta_r) * dy

    # Angle from robot's heading to fiducial marker (in robot frame)
    phi = np.arctan2(y_local, x_local)

    return (x_local, y_local, phi)
    
def visible_fms(robot_pose, fm_map, max_range=10, fov_angle=np.radians(15)):
    """
    Filters fiducial markers that are visible to the robot.
    """
    visible_fms = []

    for i, fm in enumerate(fm_map):
        x_rel, y_rel, phi = fm_robot(robot_pose, fm)
        distance = np.hypot(x_rel, y_rel)

        if distance <= max_range and 0 <= phi <= fov_angle:
            visible_fms.append((i, (x_rel, y_rel, phi)))

    return visible_fms
