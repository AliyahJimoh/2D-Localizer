"""Plotting Module: Used to plot the visual representation of the map"""

import time
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Polygon


trajectory = []  # Stores estimated positions over time
robot_trajectory = None
robot_dot = None
ani = None


def plot_localization_live(beacons, fm_map, map, g_truth, map_size, show=True):
    """
    Creates the plot that shows the robot positions, beacons and fiducial markers live on the map
    """

    plt.ion()  # Enable interactive mode

    # Load the factory layout image
    img = mpimg.imread(f"{map}")

    fig, ax = plt.subplots(figsize=(10, 8))

    # Set axis limits based on your environment dimensions
    ax.set_xlim(0, map_size[0])  # Adjust this based on real-world map scaling
    ax.set_ylim(0, map_size[1])
    ax.set_title("Real-Time Robot Localization on Factory Layout")
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")

    # Display the background image (Factory Layout)
    ax.imshow(img, extent=[0, map_size[0], 0, map_size[1]], alpha=0.6, aspect="auto")

    # Static landmarks (beacons and fiducial markers)
    beacons = np.array(beacons)
    ax.scatter(beacons[:, 0], beacons[:, 1], c="blue", marker="o", label="Beacons")
    ax.scatter(
        fm_map[:, 0], fm_map[:, 1], c="purple", marker="s", label="Fiducial Marker"
    )

    # Static ground truth
    ax.plot(g_truth[:, 0], g_truth[:, 1], "b-", label="Ground Truth")

    # Dynamic elements (robot trajectory and current position)
    global robot_trajectory, robot_dot, ani
    (robot_trajectory,) = ax.plot([], [], "r-", label="Trajectory")  # Line for path
    triangle_patch = [
        ax.add_patch(
            Polygon([[0, 0], [0, 0], [0, 0]], closed=True, color="black", label="Robot")
        )
    ]

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
        Updates the plot at each frame.
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
        (
            trajectory_x,
            trajectory_y,
        ) = zip(
            *[(p[0], p[1]) for p in trajectory[: frame + 1]]
        )  # Fix iteration issue
        robot_trajectory.set_data(trajectory_x, trajectory_y)

        # Isosceles triangle parameters
        length = 1.25  # distance from center to tip
        width = 1.0  # total base width

        # Triangle points (before rotation): tip, bottom-left, bottom-right
        points = np.array(
            [
                [length, 0],  # tip of the triangle
                [-length * 0.5, -width / 2],  # bottom left
                [-length * 0.5, width / 2],  # bottom right
            ]
        )

        # Rotation matrix for theta
        R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

        # Rotate and shift
        rotated_points = points @ R.T + np.array([x, y])

        # Update triangle patch
        triangle_patch[0].set_xy(rotated_points)

    global ani
    ani = FuncAnimation(
        fig,
        update,
        frames=lambda: iter(range(len(trajectory))),
        interval=500,
        repeat=False,
    )

    ax.legend()
    if show:
        plt.show(block=True)  # Show plot only in GUI mode

        # Wait until user closes the plot
        while plt.fignum_exists(fig.number):
            plt.pause(0.1)
    else:
        plt.close(
            fig
        )  # Avoid lingering or GUI blocking during tests  # Ensures the plot remains open

    while plt.fignum_exists(fig.number):
        plt.pause(0.1)


def update_trajectory(estimated_pose):
    """
    Stores the latest estimated pose for visualization.
    """
    trajectory.append((estimated_pose.x(), estimated_pose.y(), estimated_pose.theta()))
