import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import numpy as np
import pytest
import matplotlib
matplotlib.use("Agg")

from src.input_format import InputData

"""Testing that the inputs are valid"""

def test_map_image():
    """Tests to see if image is valid for map -> R1"""
    input = InputData(input_file="test/test_input.yaml")
    
    map_path = input.get_map()
    assert os.path.exists(map_path), "Map image file not found"
    
    
def test_coordinates():
    """Tests to check if coordinates are valid inputs -> R2"""
    
    input = InputData(input_file="test/test_input.yaml")

    beacons = input.get_beacons()
    fm_map = input.get_fmMap()

    assert beacons.shape[1] == 2, "Beacon coordinates must be 2D"
    assert fm_map.shape[1] == 3, "FM map must have x, y, theta per marker"
    
    # Type and value check
    assert np.issubdtype(beacons.dtype, np.floating), "Beacon values must be numeric"
    assert np.issubdtype(fm_map.dtype, np.floating), "FM values must be numeric"

    # Sanity check for valid numbers
    assert np.all(np.isfinite(beacons)), "Beacon coordinates contain NaN or inf"
    assert np.all(np.isfinite(fm_map)), "FM map contains NaN or inf"
    
def test_range_meausrement():
    
    """Tests if range and trajectory are the correct shape"""
    
    input = InputData(input_file="test/test_input.yaml")

    range_m = input.get_ranges()
    trajectory = input.get_trajectory()
    beacons = input.get_beacons()

    assert range_m.shape == (trajectory.shape[0], beacons.shape[0]), \
        "Range matrix shape mismatch"
    
    assert np.issubdtype(range_m.dtype, np.floating), "Range measurements values must be numeric"
