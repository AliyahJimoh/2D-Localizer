# Control Module

from localization import localize
from input_format import load_input
from gtsam import Point2, Pose2

try:
        beacons, fm_map, fm_robot,range_m = load_input(f"src/user_input" + ".yaml")
except Exception as e:
        print(f"Error loading input file: {e}")


print(localize(beacons, fm_map, fm_robot,range_m))