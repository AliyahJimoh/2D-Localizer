import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.input_format import InputData
from src.localization import localize

def test_pose_estimation():
    """
    F-ES-01: Validates that localize() returns a usable Pose2 estimate
    """
    input = InputData(input_file="test/test_input.yaml")
    beacons = input.get_beacons()
    fm_map = input.get_fmMap()
    range_m = input.get_ranges()
    trajectory = input.get_trajectory()

    pose = localize(beacons, fm_map, range_m[0, :], trajectory[0, :])
    assert hasattr(pose, "x") and hasattr(pose, "theta"), "Pose2 output invalid"
    assert abs(pose.x()) < 1e3 and abs(pose.y()) < 1e3, "Pose out of bounds"