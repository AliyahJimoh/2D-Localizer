# Control Module
import time
from multiprocessing import Process, Queue

import numpy as np

from accuracy import compute_crlb, compute_fim
from input_format import load_input
from localization import localize
from output import run_gui
from plot import plot_localization_live, update_trajectory
from trajectory import trajectory


def main():
    # Loading Data
    beacons, fm_map, fm_robot, map, range_m, variances = load_input(
        f"src/user_input.yaml"
    )

    data_queue = Queue()

    # Starting the live table
    process = Process(target=run_gui, args=(data_queue,))
    process.start()

    print("Starting Real-Time Localization...")

    m = np.size(range_m, 0)

    path = trajectory()

    # Allow at least one update before starting the plot
    estimated_pose = localize(beacons, fm_map, fm_robot, range_m[0, :], path[0, :])
    update_trajectory(estimated_pose)
    data_queue.put((1, estimated_pose.x(), estimated_pose.y(), estimated_pose.theta()))

    # Simulating continuous localization updates

    for t in range(1, m):
        estimated_pose = localize(beacons, fm_map, fm_robot, range_m[t, :], path[t, :])

        # Computing FIM & CRLB
        fim = compute_fim(estimated_pose, beacons, variances)
        crlb = compute_crlb(fim)

        print(f"Time {t}: CRLB=\n{crlb}")

        # Store the trajectory for real-time plotting
        update_trajectory(estimated_pose)
        data_queue.put(
            (t + 1, estimated_pose.x(), estimated_pose.y(), estimated_pose.theta())
        )

        time.sleep(0.1)  # Simulate delay between measurements

    plot_localization_live(beacons, fm_map, map, path)


if __name__ == "__main__":
    main()
