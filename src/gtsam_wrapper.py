"""GTSAM Module: Creates wrapper for the Georgia Tech Smoothing and Mapping (GTSAM) library"""

import gtsam


def Pose2(x, y, theta):
    """
    Create a 2D pose from (x, y, theta).\\
    Wraps gtsam.Pose2 constructor.
    """
    return gtsam.Pose2(x, y, theta)


def Point2(x, y):
    """
    Create a 2D point from (x, y).\\
    Wraps gtsam.Point2 constructor.
    """
    return gtsam.Point2(x, y)


def symbol(char, int):
    """
    Create a GTSAM symbol key using a character and index.\\
    Used for labeling variables in the factor graph.
    """
    return gtsam.symbol(char, int)


def NonlinearFactorGraph():
    """
    Instantiate a new NonlinearFactorGraph.\\
    Represents the factor graph structure for optimization.
    """
    return gtsam.NonlinearFactorGraph()


def PriorFactorPose2(key, pose, noise_model):
    """
    Create a prior factor for a 2D pose.\\
    Constrains a pose variable to a known value with uncertainty.
    """
    return gtsam.PriorFactorPose2(key, pose, noise_model)


def PriorFactorPoint2(key, point, noise_model):
    """
    Create a prior factor for a 2D point.\\
    Constrains a point variable to a known value with uncertainty.
    """
    return gtsam.PriorFactorPoint2(key, point, noise_model)


def RangeFactor2D(key1, key2, measured, noise_model):
    """
    Create a range factor between two 2D variables.\\
    Represents a range (distance) measurement between key1 and key2.
    """
    return gtsam.RangeFactor2D(key1, key2, measured, noise_model)


def BetweenFactor(key1, key2, between, noise_model):
    """
    Create a between factor for two Pose2 variables.\\
    Encodes relative transformation between two poses.
    """
    return gtsam.BetweenFactorPose2(key1, key2, between, noise_model)


def noiseModel_Isotropic_Sigma(dim, sigma):
    """
    Generate an isotropic noise model with standard deviation sigma.\\
    Useful for pose or point uncertainty.
    """
    return gtsam.noiseModel.Isotropic.Sigma(dim, sigma)


def LevenbergMarquardtOptimizer(graph, values):
    """
    Run Levenberg-Marquardt optimization on a factor graph.\\
    Returns optimized variable estimates.
    """
    return gtsam.LevenbergMarquardtOptimizer(graph, values)


def Values():
    """
    Instantiate a GTSAM Values container.\\
    Used to store variable initial guesses and results.
    """
    return gtsam.Values()


def insert(Values, key, value):
    """
    Insert a key–value pair into the GTSAM Values container.\\
    Used to define variable initial estimates.
    """
    Values.insert(key, value)


def atPose2(result, key):
    """
    Retrieve a Pose2 result from optimized Values using a key.
    """
    return result.atPose2(key)


# Wrapper for Pose2 methods


def compose(pose1, pose2):
    """
    Compose two Pose2 objects.\\
    Used to apply relative transformations.
    """
    return pose1.compose(pose2)


def inverse(pose):
    """
    Compute the inverse of a Pose2 object.\\
    Used to flip frame reference (e.g., robot to world).
    """
    return pose.inverse()
