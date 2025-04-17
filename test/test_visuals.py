import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import numpy as np
import pytest
import matplotlib
matplotlib.use("Agg")

from src.input_format import InputData
from src.plot import plot_localization_live

def test_visualization():
    """
    Test for visualization pipeline
    """
    ind = InputData(input_file="test/test_input.yaml")
    beacons = ind.get_beacons()
    fm_map = ind.get_fmMap()
    map_size = ind.get_mapSize()
    map_file = ind.get_map()
    gt = ind.get_trajectory()

    try:
        plot_localization_live(beacons, fm_map, map_file, gt,map_size, show=False)
    except Exception as e:
        assert False, f"Visualization crashed: {e}"