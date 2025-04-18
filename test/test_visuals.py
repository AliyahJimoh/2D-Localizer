import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import matplotlib

matplotlib.use("Agg")

from src.input_format import InputData
from src.plot import plot_localization_live


def test_visualization():
    """
    F-MO-01: Confirms the map and localization overlays render successfully without crashing.
    Includes beacons, FMs, robot heading and trajectory.
    """
    ind = InputData(input_file="../test/test_input.yaml")
    beacons = ind.get_beacons()
    fm_map = ind.get_fmMap()
    map_size = ind.get_mapSize()
    map_file = ind.get_map()
    gt = ind.get_trajectory()

    try:
        plot_localization_live(beacons, fm_map, map_file, gt, map_size, show=False)
    except Exception as e:
        assert False, f"Visualization crashed: {e}"
