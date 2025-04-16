"""Input Format Module: Puts the user input in the correct data structure for the program"""

import csv

import numpy as np
import yaml

from simulation import noisy_range


class InputData:
    """
    This class is an abstract data type used for getting user inputs
    """

    def __init__(self, input_file=f"user_input.yaml"):
        self.input_file = input_file
        self.data = self.load_input()

    def load_input(self):
        """
        Loads user input file
        """
        try:
            with open(self.input_file, "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Error: User input file '{self.input_file}' not found!"
            )
        except yaml.YAMLError:
            raise ValueError(f"Error: Invalid YAML format in '{self.input_file}'.")

    def get_beacons(self):
        """
        Gives the coordinates of all beacons mentioned
        """
        reader = csv.reader(open(f"inputs/{self.data['beacons']}", "r"), delimiter=",")
        next(reader)
        x = list(reader)
        return np.array(x).astype("float")

    def get_fmMap(self):
        """
        Gives the coordinates of fiducial markers with respect to the map's frame of reference
        """
        reader = csv.reader(
            open(f"inputs/{self.data['FM']['fm_map']}", "r"), delimiter=","
        )
        next(reader)
        x = list(reader)
        return np.array(x).astype("float")
        # return Pose2(np.array(x).astype("float"))

    # def get_fmRobot(self):
    #     """
    #     Gives the coordinates of fiducial markers with respect to the robot's frame of reference
    #     """
    #     return Pose2(*self.data["sensor_data"]["camera"])

    def get_map(self):
        """
        Gives the name of the map's image
        """
        return f"inputs/{self.data['map']['name']}"

    def get_mapSize(self):
        """
        Gives the name of the map's image
        """
        return np.array(self.data["map"]["size"])

    def get_trajectory(self):
        """
        Gives the trajectory of the robot
        """
        reader = csv.reader(
            open(f"inputs/{self.data['trajectory']}", "r"), delimiter=","
        )
        next(reader)
        x = list(reader)
        return np.array(x).astype("float")

    def get_ranges(self):
        """
        Gives noisy range measurements
        """
        beacons = self.get_beacons()
        variances = self.get_variances()
        trajectory = self.get_trajectory()
        return noisy_range(beacons, variances, trajectory)

    def get_variances(self):
        """
        Gives a set noise variances (one for each beacon)
        """
        return np.array(self.data["sensor_data"]["variances"])
