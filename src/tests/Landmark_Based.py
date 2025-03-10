import gtsam
from gtsam import symbol, Pose2, Rot2
import numpy as np

# Create factor graph
graph = gtsam.NonlinearFactorGraph()

# Create keys for variables
i1 = symbol('x', 1)
i2 = symbol('x', 2)
i3 = symbol('x', 3)
j1 = symbol('l', 1)
j2 = symbol('l', 2)

# Add prior factor at the origin
prior_mean = Pose2(0.0, 0.0, 0.0)
prior_noise = gtsam.noiseModel.Diagonal.Sigmas(np.array([0.3, 0.3, 0.1]))
graph.add(gtsam.PriorFactorPose2(i1, prior_mean, prior_noise))

# Add odometry factors
odometry = Pose2(2.0, 0.0, 0.0)
odometry_noise = gtsam.noiseModel.Diagonal.Sigmas(np.array([0.2, 0.2, 0.1]))
graph.add(gtsam.BetweenFactorPose2(i1, i2, odometry, odometry_noise))
graph.add(gtsam.BetweenFactorPose2(i2, i3, odometry, odometry_noise))

# Add bearing and range measurement factors
degrees = np.pi / 180  # Convert degrees to radians
br_noise = gtsam.noiseModel.Diagonal.Sigmas(np.array([0.1, 0.2]))

graph.add(gtsam.BearingRangeFactor2D(i1, j1, Rot2(45 * degrees), np.sqrt(8), br_noise))
graph.add(gtsam.BearingRangeFactor2D(i2, j1, Rot2(90 * degrees), 2, br_noise))
graph.add(gtsam.BearingRangeFactor2D(i3, j2, Rot2(90 * degrees), 2, br_noise))

# Print the factor graph
print("Factor Graph:\n", graph)
