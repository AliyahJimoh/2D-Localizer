# Puts the users input in the correct format

import numpy as np
import yaml

from gtsam_wrapper import Pose2
from range_measurements import noisy_range


class InputData:
    """
    Abstract Data Type used for getting user inputs
    """

    def __init__(self, input_file=f"src/user_input.yaml"):
        self.input_file = input_file
        self.data = self.load_input()

    def load_input(self):
        try:
            with open(self.input_file, "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Error: User input file '{self.input_file}' not found!")
        except yaml.YAMLError:
            raise ValueError(
                f"Error: Invalid YAML format in '{self.input_file}'.")

    def get_beacons(self):
        return np.array(self.data["beacons"])
    
    def get_fmMap(self):
        return Pose2(*self.data["FM"]["fm_map"])
    
    def get_fmRobot(self):
        return Pose2(*self.data["sensor_data"]["camera"])
    
    def get_map(self):
        return self.data["map"]
    
    def get_ranges(self):
        # return np.array(self.data["sensor_data"]["range_measurements"])
        beacons = self.get_beacons()
        variances = self.get_variances()
        return noisy_range(beacons, variances)
    
    def get_variances(self):
        return np.array(self.data["sensor_data"]["variances"])
        # return np.random.uniform(0.0025, 0.01, size=len(self.get_beacons()))
    