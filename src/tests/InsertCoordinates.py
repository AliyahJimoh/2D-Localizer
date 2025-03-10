# Verifying that coordinates can be put on the image

import numpy as np

a = np.array([
    [3,4],
    [6 ,8],
    [10 ,21]
]) #Inserting coordinates for beacons (m)[x,y]

for j in range(a.shape[0]):
    print(a[j,:])


