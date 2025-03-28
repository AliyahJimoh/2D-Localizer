"""Localization Module: Mathematically computes the estimate pose with the wrapped GTSAM library"""

import gtsam_wrapper as gtsam
from gtsam_wrapper import Point2, Pose2, symbol


def localize(beacons, fm_map, fm_robot, range_m, init_guess):
    """
    Gives estimated pose from selected set of measurements for position i
    """

    init_x = init_guess[0]
    init_y = init_guess[1]

    # Robot position (MLE will estimate this) defined with 'x'
    robot_id = symbol("x", 1)  # Robot variable in factor graph

    # Beacon symbols defined with 'a'
    # visible_beacon_indices = [i for i in range(
    #     len(beacons)) if range_m[i] <= max_distance]
    beacon_ids = [symbol("a", j + 1) for j in range(len(beacons))]

    # Fiducial Markers defined with 'f'
    symbol("f", 1)

    # Setting Up fiducial marker poses
    # Compute transformation from fiducial marker to robot
    T_fr = gtsam.inverse(fm_robot)
    T_mf = fm_map
    T_mr = gtsam.compose(T_mf, T_fr)
    # Factor graph needs to be initialized
    graph = gtsam.NonlinearFactorGraph()

    # Add prior on robot's initial position (for stability)
    # Basically the actual position of the robot
    prior_noise = gtsam.noiseModel_Isotropic_Sigma(3, 1)
    graph.add(gtsam.PriorFactorPose2(robot_id, Pose2(init_x, init_y, 0), prior_noise))

    # Define noise model for range measurements
    range_noise = gtsam.noiseModel_Isotropic_Sigma(1, 0.5)

    # Add range measurement factors to the graph
    for j, beacon_pos in enumerate(beacons):
        beacon_symbol = beacon_ids[j]
        graph.add(gtsam.RangeFactor2D(robot_id, beacon_symbol, range_m[j], range_noise))

    # Fix one beacon's position with a very small noise model
    beacon_prior_noise = gtsam.noiseModel_Isotropic_Sigma(2, 0.5)  # Small uncertainty
    graph.add(
        gtsam.PriorFactorPoint2(
            beacon_ids[0], Point2(beacons[0][0], beacons[0][1]), beacon_prior_noise
        )
    )

    # Create initial values for optimization
    initial_estimates = gtsam.Values()

    # Use Fiducial markers as first pose estimate

    if init_y == 38.0:
        gtsam.insert(initial_estimates, robot_id, T_mr)
    else:
        gtsam.insert(initial_estimates, robot_id, Pose2(init_x, init_y, 0))

    for j, beacon_pos in enumerate(beacons):
        gtsam.insert(
            initial_estimates, beacon_ids[j], Point2(beacon_pos[0], beacon_pos[1])
        )

    # initial_estimates.insert(fiducial_id, T_mf)

    # # Print initial estimates for debugging
    # print("Initial Estimates:")
    # print(initial_estimates)

    # Solve using Levenberg-Marquardt optimizer (more stable)
    optimizer = gtsam.LevenbergMarquardtOptimizer(graph, initial_estimates)
    result = optimizer.optimize()

    # Extract estimated robot position
    mle_robot_pose = gtsam.atPose2(result, robot_id)

    return mle_robot_pose
