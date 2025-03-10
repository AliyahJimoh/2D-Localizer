# Theoretical models used in 2D Localizer
import math as m
import numpy as np

    
def se2(x, y, theta):
    """
    This method sets up a Special Euclidean 2D Transformation and returns its matrix
    """
    
    matrix = np.array([
        [m.cos(theta), -m.sin(theta), x],
        [m.sin(theta), m.cos(theta), y],
        [0, 0 ,1]
    ])
    return matrix