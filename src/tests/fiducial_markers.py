import gtsam
from gtsam import symbol, Point2, Pose2
import numpy as np

# Define known fiducial marker poses (x, y, theta(orientation)) This would be T_mf as it is the pose of the fms wrt the map's frame
T_mf = Pose2(2, 3, np.pi/4)

# Next would be the fm wrt the robot's frame when its camera detects it
T_rf = Pose2(1, 0.5, 0)

# To set up this pose, we need to inverse it to acquire T_fr
T_fr = T_rf.inverse()

# With these variables, we can calculate T_mr with the compose function that cam multiply matrices
T_mr = T_mf.compose(T_fr)

print(T_mr)
    