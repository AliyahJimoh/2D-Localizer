# plot.py
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation

trajectory = []  # Stores estimated positions over time

def plot_localization_live(beacons, fm_map, image_path):
    """
    Live updating plot for localization trajectory on a factory layout image.
    """
    # Load the factory layout image
    img = mpimg.imread(image_path)

    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Set axis limits based on your environment dimensions
    ax.set_xlim(0, 15)  # Adjust this based on real-world map scaling
    ax.set_ylim(0, 15)
    ax.set_title("Real-Time Robot Localization on Factory Layout")
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")

    # Display the background image (Factory Layout)
    ax.imshow(img, extent=[0, 15, 0, 15], alpha=0.6, aspect='auto')

    # Static landmarks (beacons and fiducial markers)
    beacons = np.array(beacons)
    ax.scatter(beacons[:, 0], beacons[:, 1], c='blue', marker='o', label="Beacons")
    ax.scatter(fm_map.x(), fm_map.y(), c='green', marker='s', label="Fiducial Marker")

    # Dynamic elements (robot trajectory)
    robot_trajectory, = ax.plot([], [], 'r-', label="Trajectory")  # Line for path
    robot_dot, = ax.plot([], [], 'ro', label="Current Position")  # Red dot for current position

    def update(frame):
        """
        This function updates the plot at each frame.
        """
        if frame < len(trajectory):
            x, y, _ = trajectory[frame]
            robot_trajectory.set_data(*zip(*trajectory[:frame+1]))  # Update path
            robot_dot.set_data(x, y)  # Update robot dot
            plt.pause(0.1)  # Ensure updates are visible

        return robot_trajectory, robot_dot

    ani = FuncAnimation(fig, update, frames=len(trajectory), interval=500, repeat=False)

    ax.legend()
    plt.show(block=True)  # Ensures the plot remains open

def update_trajectory(estimated_pose):
    """
    Stores the latest estimated pose for visualization.
    """
    trajectory.append((estimated_pose.x(), estimated_pose.y(), estimated_pose.theta()))
