# Control Module
import time

import numpy as np

from input_format import load_input
from localization import localize
from plot import plot_localization_live, update_trajectory
from trajectory import trajectory

# from output import update_output


def main():
    # Loading Data
    beacons, fm_map, fm_robot, map, range_m = load_input(f"src/user_input.yaml")

    print("Starting Real-Time Localization...")

    m = np.size(range_m, 0)

    path = trajectory()

    # Allow at least one update before starting the plot
    estimated_pose = localize(beacons, fm_map, fm_robot, range_m[0, :], path[0, :])
    update_trajectory(estimated_pose)
    # update_output(1, estimated_pose)

    # Launch the live trajectory visualization on the factory layout
    #     plot_localization_live(beacons, fm_map, map)

    # Simulating continuous localization updates

    for t in range(1, m):
        estimated_pose = localize(beacons, fm_map, fm_robot, range_m[t, :], path[t, :])

        # Store the trajectory for real-time plotting
        update_trajectory(estimated_pose)
        # update_output(t+1, estimated_pose)

        print(f"Time {t}: Estimated Pose -> {estimated_pose}")

        time.sleep(0.01)  # Simulate delay between measurements

    plot_localization_live(beacons, fm_map, map, path)


if __name__ == "__main__":
    main()
