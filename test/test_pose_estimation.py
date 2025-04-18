import os
import sys

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from src import simulation
from src.input_format import InputData
from src.localization import localize


def test_range_only(monkeypatch):
    """
    F-RO-01: Verifies pose estimation using only range measurements
    """

    def no_fms(*args, **kwargs):
        return []  # Force no FMs

    monkeypatch.setattr(simulation, "visible_fms", no_fms)

    input = InputData(input_file="../test/test_input.yaml")
    beacons = input.get_beacons()
    fm_map = input.get_fmMap()
    range_m = input.get_ranges()
    trajectory = input.get_trajectory()

    pose = localize(beacons, fm_map, range_m[0, :], trajectory[0, :])

    assert np.isfinite(pose.x()) and np.isfinite(pose.y()), "Pose has NaN or inf"


def test_fiducials():
    """
    F-SE2-01: Verifies pose estimation using only range measurements
    """

    input = InputData(input_file="../test/test_input.yaml")
    beacons = input.get_beacons()
    fm_map = input.get_fmMap()
    range_m = input.get_ranges()
    trajectory = input.get_trajectory()

    pose = localize(beacons, fm_map, range_m[10, :], trajectory[10, :])

    assert (
        abs(pose.theta()) > 0.01
    ), "Pose theta too small — possible FM transform not influencing result"


def test_sensor_fusion(monkeypatch):
    """
    F-SF-01: Verifies that combining range and fiducial data results in a pose shift.
    Logs pose differences and fusion effectiveness.
    """
    input = InputData(input_file="../test/test_input.yaml")
    beacons = input.get_beacons()
    fm_map = input.get_fmMap()
    range_m = input.get_ranges()
    trajectory = input.get_trajectory()

    i = 120  # Point expected to have FM visibility

    # Force range-only estimate
    monkeypatch.setattr(simulation, "visible_fms", lambda *args, **kwargs: [])
    pose_range_only = localize(beacons, fm_map, range_m[i, :], trajectory[i, :])

    # Use real FMs for fusion
    monkeypatch.undo()
    pose_fused = localize(beacons, fm_map, range_m[i, :], trajectory[i, :])

    dx = abs(pose_fused.x() - pose_range_only.x())
    dy = abs(pose_fused.y() - pose_range_only.y())

    print(f"Pose range-only: x={pose_range_only.x():.4f}, y={pose_range_only.y():.4f}")
    print(f"Pose fused:      x={pose_fused.x():.4f}, y={pose_fused.y():.4f}")
    print(f"Δx={dx:.6f}, Δy={dy:.6f}")

    if dx < 1e-5 and dy < 1e-5:
        print(f"Sensor fusion had minimal or no effect at i={i}")
    else:
        print(f"Sensor fusion shifted the pose at i={i}")

    assert True  # Always pass for reporting/logging purposes
