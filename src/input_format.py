# Puts the users input in the correct format 

import numpy as np
import yaml
from gtsam import Pose2

def load_input(file_path):
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    
    # Convert lists to NumPy arrays for computations
    beacon_positions = np.array(data["beacons"])
    fiducial_map = Pose2(*data["FM"]["fm_map"])
    fiducial_robot= Pose2(*data["sensor_data"]["camera"])
    range_measurements = np.array(data["sensor_data"]["range_measurements"])

    return beacon_positions, fiducial_map, fiducial_robot, range_measurements