# plot.py
import time

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

trajectory = []  # Stores estimated positions over time
robot_trajectory = None
robot_dot = None
ani = None


def plot_localization_live(beacons, fm_map, map, g_truth):
    """
    Live updating plot for localization trajectory on a factory layout image.
    """
    plt.ion()  # Enable interactive mode

    # Load the factory layout image
    img = mpimg.imread(f"src/{map}")

    fig, ax = plt.subplots(figsize=(10, 8))

    # Set axis limits based on your environment dimensions
    ax.set_xlim(0, 60)  # Adjust this based on real-world map scaling
    ax.set_ylim(0, 45)
    ax.set_title("Real-Time Robot Localization on Factory Layout")
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")

    # Display the background image (Factory Layout)
    ax.imshow(img, extent=[0, 60, 0, 45], alpha=0.6, aspect="auto")

    # Static landmarks (beacons and fiducial markers)
    beacons = np.array(beacons)
    ax.scatter(beacons[:, 0], beacons[:, 1], c="blue", marker="o", label="Beacons")
    ax.scatter(fm_map.x(), fm_map.y(), c="green", marker="s", label="Fiducial Marker")

    # Static ground truth
    ax.plot(g_truth[:, 0], g_truth[:, 1], "b-", label="Ground Truth")

    # Dynamic elements (robot trajectory and current position)
    global robot_trajectory, robot_dot, ani
    (robot_trajectory,) = ax.plot([], [], "r-", label="Trajectory")  # Line for path
    (robot_dot,) = ax.plot([], [], marker=(3, 0, 0),c="black", label="Robot", markersize=12)

    max_wait_time = 5  # Maximum wait time (seconds)
    start_time = time.time()

    while len(trajectory) == 0:
        if time.time() - start_time > max_wait_time:
            print(
                "Warning: No trajectory data received! Continuing with empty trajectory."
            )
            break  # Exit waiting loop
        plt.pause(0.1)  # Keep UI responsive

    def update(frame):
        """
        This function updates the plot at each frame.
        """
        if len(trajectory) == 0:
            print("Warning: No trajectory data available. Skipping update.")
            return robot_trajectory, robot_dot  # Avoid errors

        if frame >= len(trajectory):
            print(
                f"Warning: Frame {frame} exceeds trajectory length {len(trajectory)}."
            )
            return robot_trajectory, robot_dot  # Prevent out-of-bounds access

        x, y, theta = trajectory[frame]  # Extract only x, y

        # Update the trajectory line
        trajectory_x, trajectory_y,= zip(
            *[(p[0], p[1]) for p in trajectory[: frame + 1]]
        )  # Fix iteration issue
        robot_trajectory.set_data(trajectory_x, trajectory_y)

        # Update the current robot position (red dot)
        robot_dot.set_data(x, y)
        robot_dot.set_markersize(10)
        robot_dot.set_marker((3, 0, theta*(180/np.pi)))

        plt.draw()
        plt.pause(0.1)  # Allow the UI to refresh

        return robot_trajectory, robot_dot

    ani = FuncAnimation(
        fig,
        update,
        frames=lambda: iter(range(len(trajectory))),
        interval=500,
        repeat=False,
    )

    # print("Trajectory data:", trajectory)

    ax.legend()
    plt.show(block=True)  # Ensures the plot remains open
    # plt.pause(0.1)

    while plt.fignum_exists(fig.number):
        plt.pause(0.1)


def update_trajectory(estimated_pose):
    """
    Stores the latest estimated pose for visualization.
    """
    trajectory.append((estimated_pose.x(), estimated_pose.y(), estimated_pose.theta()))
