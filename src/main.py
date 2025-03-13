# Control Module

from localization import localize
import input_format
from gtsam import Point2, Pose2

try:
        beacons, fm_map, fm_robot,range_m = input_format.load_input(f"src/user_input" + ".yaml")
except Exception as e:
        print(f"Error loading input file: {e}")


print(localize(beacons, fm_map, fm_robot,range_m))