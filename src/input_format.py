# Puts the users input in the correct format

import numpy as np
import yaml
from gtsam_wrapper import Pose2

from range_measurements import noisy_range


def load_input(file_path):
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)

    # Convert lists to NumPy arrays for computations
    beacon_positions = np.array(data["beacons"])
    fiducial_map = Pose2(*data["FM"]["fm_map"])
    fiducial_robot = Pose2(*data["sensor_data"]["camera"])
    map = data["map"]
    # range_measurements = np.array(data["sensor_data"]["range_measurements"])
    range_measurements = noisy_range(beacon_positions)

    return beacon_positions, fiducial_map, fiducial_robot, map, range_measurements
