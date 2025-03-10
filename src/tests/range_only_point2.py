import gtsam
from gtsam import symbol, Point2
import numpy as np

# Define known beacon positions (landmarks)
beacons = np.array([
    [3, 4],   
    [6, 8],   
    [10, 21]  
])

# Define robot position (MLE will estimate this)
robot_id = symbol('x', 1)  # Robot variable in factor graph

# Define beacon symbols with 'a' instead of 'l'
beacon_ids = [symbol('a', i+1) for i in range(len(beacons))]  

# Create factor graph
graph = gtsam.NonlinearFactorGraph()

# Add prior on robot's initial position (optional, for stability)
prior_mean = Point2(5, 9)  
prior_noise = gtsam.noiseModel.Isotropic.Sigma(2, 1.0)  
graph.add(gtsam.PriorFactorPoint2(robot_id, prior_mean, prior_noise))

# Define measured range data (assume noisy distances)
range_measurements = [np.linalg.norm(beacon - np.array([5, 9])) + np.random.normal(0, 0.2) for beacon in beacons]

# Define noise model for range measurements
range_noise = gtsam.noiseModel.Isotropic.Sigma(1, 0.5)  

# Add range measurement factors to the graph (MLE estimation)
for i, beacon_pos in enumerate(beacons):
    beacon_symbol = beacon_ids[i]  # Uses 'a' as symbol namespace
    beacon_point = Point2(beacon_pos[0], beacon_pos[1])
    
    # Add range factor (robot → beacon)
    graph.add(gtsam.RangeFactor2D(robot_id, beacon_symbol, range_measurements[i], range_noise))

# Create initial values for optimization
initial_estimates = gtsam.Values()
initial_estimates.insert(robot_id, Point2(4, 8))  # Initial guess for robot pose
for i, beacon_pos in enumerate(beacons):
    initial_estimates.insert(beacon_ids[i], Point2(beacon_pos[0], beacon_pos[1]))  # Fixed beacons

# Solve using Levenberg-Marquardt (MLE maximizes likelihood via least-squares)
optimizer = gtsam.LevenbergMarquardtOptimizer(graph, initial_estimates)
result = optimizer.optimize()

# Extract estimated robot position (MLE result)
mle_robot_pose = result.atPoint2(robot_id)
print("MLE Estimated Robot Position:", mle_robot_pose)
