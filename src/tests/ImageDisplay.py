#Testing how to display a map with python for gtsam

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
img = mpimg.imread('factorylayout3.jpg')
imgplot = plt.imshow(img)
plt.show()