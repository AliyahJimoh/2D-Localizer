import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import numpy as np

from src.accuracy import compute_crlb, compute_fim
from src.input_format import InputData
from src.localization import localize


def test_accuracy():
    """
    NF-ACC-01: Validates estimation accuracy through RMSE and CRLB constraints.
    """
    input = InputData(input_file="../test/test_input.yaml")
    beacons = input.get_beacons()
    fm_map = input.get_fmMap()
    range_m = input.get_ranges()
    variances = input.get_variances()
    trajectory = input.get_trajectory()

    # Estimated pose from sensor data
    pose = localize(beacons, fm_map, range_m[0, :], trajectory[0, :])

    # Ground truth pose (used for RMSE)
    gt_pose = trajectory[0, :]  # [x, y, theta]

    # Compute RMSE between estimated and ground truth (for x, y)
    rmse = np.sqrt(np.mean((np.array([pose.x(), pose.y()]) - gt_pose[:2]) ** 2))
    assert np.isfinite(rmse), "RMSE is not finite"
    assert rmse < 5.0, f"RMSE too high: {rmse:.4f}"

    # Compute CRLB through FIM
    fim = compute_fim(pose, beacons, variances)
    crlb = compute_crlb(fim)

    # Structural and numerical assertions
    assert fim.shape == (2, 2)
    assert crlb.shape == (2, 2)
    assert np.all(np.isfinite(crlb)), "CRLB contains non-finite values"

    det = np.linalg.det(crlb)
    assert det > 1e-6, f"CRLB matrix is nearly singular (det = {det:.6e})"
