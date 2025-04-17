"""Input Format Module: Puts the user input in the correct data structure for the program"""
import os
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
        self.base_dir = os.path.dirname(os.path.abspath(input_file))
        self.data = self.load_input()

    def _resolve_path(self, path):
        abs_path = os.path.join(self.base_dir, path)
        if os.path.exists(abs_path):
            return abs_path
        raise FileNotFoundError(f"Cannot resolve path: {abs_path}")
    
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
        path = self._resolve_path(self.data["beacons"])
        with open(path, "r") as f:
            reader = csv.reader(f, delimiter=",")
            next(reader)
            return np.array(list(reader)).astype("float")

    def get_fmMap(self):
        """
        Gives the coordinates of fiducial markers with respect to the map's frame of reference
        """
        path = self._resolve_path(self.data["FM"]["fm_map"])
        with open(path, "r") as f:
            reader = csv.reader(f, delimiter=",")
            next(reader)
            return np.array(list(reader)).astype("float")

    def get_map(self):
        """
        Gives the name of the map's image
        """
        return self._resolve_path(self.data["map"]["name"])

    def get_mapSize(self):
        """
        Gives the name of the map's image
        """
        return np.array(self.data["map"]["size"])

    def get_trajectory(self):
        """
        Gives the trajectory of the robot
        """
        path = self._resolve_path(self.data["trajectory"])
        with open(path, "r") as f:
            reader = csv.reader(f, delimiter=",")
            next(reader)
            return np.array(list(reader)).astype("float")

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
