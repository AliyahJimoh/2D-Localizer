import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import numpy as np
import pytest

from src.input_format import InputData
from src.localization import localize
from src.accuracy import compute_fim, compute_crlb

def test_accuracy():
    """
    Checks if FIM and CRLB values are computable and well-behaved
    """
    input = InputData(input_file="test/test_input.yaml")
    beacons = input.get_beacons()
    fm_map = input.get_fmMap()
    range_m = input.get_ranges()
    variances = input.get_variances()
    trajectory = input.get_trajectory()

    pose = localize(beacons, fm_map, range_m[0, :], trajectory[0, :])
    fim = compute_fim(pose, beacons, variances)
    crlb = compute_crlb(fim)

    assert fim.shape == (2, 2)
    assert crlb.shape == (2, 2)
    assert np.all(np.isfinite(crlb)), "CRLB contains non-finite values"