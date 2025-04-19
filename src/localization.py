"""Localization Module: Mathematically computes the estimate pose with the wrapped GTSAM library"""

import gtsam_wrapper as gtsam
from gtsam_wrapper import Point2, Pose2, symbol
from simulation import visible_fms


def localize(beacons, fm_map, range_m, init_guess):
    """
    Gives estimated pose from selected set of measurements for position i
    """
    max_distance = 15
    init_x = init_guess[0]
    init_y = init_guess[1]

    # Robot position (MLE will estimate this) defined with 'x'
    robot_id = symbol("x", 1)  # Robot variable in factor graph

    visible_beacons = [
        (j, beacons[j], range_m[j])
        for j in range(len(beacons))
        if range_m[j] <= max_distance
    ]

    visible_beacon_indices = [symbol("a", j + 1)
                              for j, _, _ in visible_beacons]

    # Fiducial Markers defined with 'f'
    fms = visible_fms(init_guess, fm_map)  # Getting FMs within robot's range
    fm_noise = gtsam.noiseModel_Isotropic_Sigma(3, 0.2)  # FM noise

    graph = gtsam.NonlinearFactorGraph()

    # Add prior on robot's initial position (for stability)
    prior_noise = gtsam.noiseModel_Isotropic_Sigma(3, 0.2)
    graph.add(
        gtsam.PriorFactorPose2(
            robot_id, Pose2(init_x, init_y, init_guess[2]), prior_noise
        )
    )

    # Define noise model for range measurements
    range_noise = gtsam.noiseModel_Isotropic_Sigma(1, 0.5)

    # Add range measurement factors to the graph
    for j, beacon_pos, measured_range in visible_beacons:
        beacon_symbol = symbol("a", j + 1)
        graph.add(
            gtsam.RangeFactor2D(robot_id, beacon_symbol,
                                measured_range, range_noise)
        )

    # Fix one beacon's position with a very small noise model
    beacon_prior_noise = gtsam.noiseModel_Isotropic_Sigma(
        2, 0.1)  # Small uncertainty
    _, beacon_pos, _ = visible_beacons[0]
    graph.add(
        gtsam.PriorFactorPoint2(
            visible_beacon_indices[0],
            Point2(beacon_pos[0], beacon_pos[1]),
            beacon_prior_noise,
        )
    )

    # Create initial values for optimization
    initial_estimates = gtsam.Values()

    # Adding Fiducial Markers and their initial estimates
    for i, (x_rel, y_rel, phi) in fms:
        fm_symbol = symbol("f", i + 1)

        T_fr = Pose2(x_rel, y_rel, phi)

        # Getting the factor between the robot and fiducial marker
        graph.add(gtsam.BetweenFactor(robot_id, fm_symbol, T_fr, fm_noise))

        # Add prior for fiducial marker pose (map-known)
        T_mf = Pose2(
            fm_map[i][0], fm_map[i][1], fm_map[i][2]
        )  # assume 0 orientation for now
        fm_prior_noise = gtsam.noiseModel_Isotropic_Sigma(3, 0.05)
        graph.add(gtsam.PriorFactorPose2(fm_symbol, T_mf, fm_prior_noise))

        # Add initial estimate for fiducial pose
        gtsam.insert(initial_estimates, fm_symbol, T_mf)

    # Initial estimate for robot
    gtsam.insert(initial_estimates, robot_id,
                 Pose2(init_x, init_y, init_guess[2]))

    # Static estimates for each beacon in range
    for j, (_, beacon_pos, _) in enumerate(visible_beacons):
        gtsam.insert(
            initial_estimates,
            visible_beacon_indices[j],
            Point2(beacon_pos[0], beacon_pos[1]),
        )

    # Solve using Levenberg-Marquardt optimizer (more stable)
    optimizer = gtsam.LevenbergMarquardtOptimizer(graph, initial_estimates)
    result = optimizer.optimize()

    # Extract estimated robot position
    mle_robot_pose = gtsam.atPose2(result, robot_id)

    return mle_robot_pose
