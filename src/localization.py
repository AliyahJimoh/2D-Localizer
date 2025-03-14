# This is to mathematically compute the estimate pose

import gtsam
from gtsam import symbol, Point2, Pose2
import numpy as np

def localize(beacons, fm_map, fm_robot,range_m):
    
    # Robot position (MLE will estimate this) defined with 'x'
    robot_id = symbol('x', 1)  # Robot variable in factor graph

    # Beacon symbols defined with 'a'
    beacon_ids = [symbol('a', i+1) for i in range(len(beacons))]  
    
    #Fiducial Markers defined with 'f'
    fiducial_id = symbol('f', 1)
    
    # Setting Up fiducial marker poses
    # Compute transformation from fiducial marker to robot
    T_fr = fm_robot.inverse()
    T_mf = fm_map

    # Factor graph needs to be initialized
    graph = gtsam.NonlinearFactorGraph()

    # Add prior on robot's initial position (for stability)
    #Basically the actual position of the robot
    prior_noise = gtsam.noiseModel.Isotropic.Sigma(3, 1.0)
    graph.add(gtsam.PriorFactorPose2(robot_id, Pose2(0, 0, 0), prior_noise))

    # Define noise model for range measurements
    range_noise = gtsam.noiseModel.Isotropic.Sigma(1, 0.5)

    # Add range measurement factors to the graph
    for i, beacon_pos in enumerate(beacons):
        beacon_symbol = beacon_ids[i]  
        graph.add(gtsam.RangeFactor2D(robot_id, beacon_symbol, range_m[i], range_noise))

    # Fix one beacon's position with a very small noise model
    beacon_prior_noise = gtsam.noiseModel.Isotropic.Sigma(2, 0.5)  # Small uncertainty
    graph.add(gtsam.PriorFactorPoint2(beacon_ids[0], Point2(beacons[0][0], beacons[0][1]), beacon_prior_noise))

    # Create initial values for optimization
    initial_estimates = gtsam.Values()
    
    # Use Fiducial markers as first pose estimate
    T_mr = T_mf.compose(T_fr)
    initial_estimates.insert(robot_id, T_mr)

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
    
    return mle_robot_pose
