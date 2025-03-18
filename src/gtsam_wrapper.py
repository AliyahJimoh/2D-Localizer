import gtsam


def Pose2(x, y, theta):
    return gtsam.Pose2(x, y, theta)


def Point2(x, y):
    return gtsam.Point2(x, y)


def symbol(str, num):
    return gtsam.symbol(str, num)  # str -> a string


def NonlinearFactorGraph():
    return gtsam.NonlinearFactorGraph()


def PriorFactorPose2(key, pose, noise_model):
    return gtsam.PriorFactorPose2(key, pose, noise_model)


def PriorFactorPoint2(key, point, noise_model):
    return gtsam.PriorFactorPoint2(key, point, noise_model)


def RangeFactor2D(key1, key2, measured, noise_model):
    return gtsam.RangeFactor2D(key1, key2, measured, noise_model)


def noiseModel_Isotropic_Sigma(dim, sigma):
    return gtsam.noiseModel.Isotropic.Sigma(dim, sigma)


def LevenbergMarquardtOptimizer(graph, values):
    return gtsam.LevenbergMarquardtOptimizer(graph, values)


def Values():
    return gtsam.Values()


def insert(values, key, value):
    values.insert(key, value)


def atPose2(result, key):
    return result.atPose2(key)


# Wrapper for Pose2 methods
def compose(pose1, pose2):
    return pose1.compose(pose2)


def inverse(pose):
    return pose.inverse()
