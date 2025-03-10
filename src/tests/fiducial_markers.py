import gtsam
from gtsam import symbol, Point2, Pose2
import numpy as np
import models as mod

# Define known fiducial marker poses (x, y, theta(orientation))
fm = np.array([
    [3, 4, np.pi/2],   
    [6, 8, ],   
    [10, 2]  
])

# Define robot position (MLE will estimate this)
robot_id = symbol('x', 1)  # Robot variable in factor graph

# Define beacon symbols with 'a' instead of 'l'
beacon_ids = [symbol('a', i+1) for i in range(len(beacons))]  

# Create factor graph
graph = gtsam.NonlinearFactorGraph()

# Add prior on robot's initial position (for stability)
#Basically the actual position of the robot
prior_mean = Pose2(5, 9, 0)
prior_noise = gtsam.noiseModel.Isotropic.Sigma(3, 1.0)
graph.add(gtsam.PriorFactorPose2(robot_id, prior_mean, prior_noise))

# Define noise model for range measurements
range_noise = gtsam.noiseModel.Isotropic.Sigma(1, 0.5)

# Define measured range data (assume noisy distances)
range_measurements = [np.linalg.norm(beacon - np.array([5, 9])) + np.random.normal(0, 0.2) for beacon in beacons]

# Add range measurement factors to the graph
for i, beacon_pos in enumerate(beacons):
    beacon_symbol = beacon_ids[i]  
    graph.add(gtsam.RangeFactor2D(robot_id, beacon_symbol, range_measurements[i], range_noise))

# Fix one beacon's position with a very small noise model
beacon_prior_noise = gtsam.noiseModel.Isotropic.Sigma(2, 0.5)  # Small uncertainty
graph.add(gtsam.PriorFactorPoint2(beacon_ids[0], Point2(beacons[0][0], beacons[0][1]), beacon_prior_noise))

# Create initial values for optimization
initial_estimates = gtsam.Values()
initial_estimates.insert(robot_id, Pose2(4, 5, 0))  # Initial guess for robot pose
for i, beacon_pos in enumerate(beacons):
    initial_estimates.insert(beacon_ids[i], Point2(beacon_pos[0], beacon_pos[1]))  # Fixed beacons as Point2

# Print initial estimates for debugging
print("Initial Estimates:")
print(initial_estimates)

# Solve using Levenberg-Marquardt optimizer (more stable)
optimizer = gtsam.LevenbergMarquardtOptimizer(graph, initial_estimates)
result = optimizer.optimize()

# Extract estimated robot position
mle_robot_pose = result.atPose2(robot_id)
print("MLE Estimated Robot Position:", mle_robot_pose)
