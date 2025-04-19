"""Control Module: Manages the execution of the program"""

import time
from multiprocessing import Process, Queue

import numpy as np

from accuracy import compute_crlb, compute_fim
from input_format import InputData
from localization import localize
from output import run_gui
from plot import plot_localization_live, update_trajectory


def main():
    """
    Executes the program
    """
    # Loading Data
    input = InputData()

    beacons = input.get_beacons()
    fm_map = input.get_fmMap()
    map_size = input.get_mapSize()
    map = input.get_map()
    range_m = input.get_ranges()
    variances = input.get_variances()
    path = input.get_trajectory()

    data_queue = Queue()  # Queue responsible for holding all of pose estimates

    # Starting the live table
    process = Process(target=run_gui, args=(data_queue,))
    process.start()

    print("Starting Real-Time Localization...")

    m = np.size(range_m, 0)  # Number of sets for range measurements

    # Allow at least one update before starting the plot
    estimated_pose = localize(beacons, fm_map, range_m[0, :], path[0, :])
    update_trajectory(estimated_pose)

    fim = compute_fim(estimated_pose, beacons, variances)
    crlb = compute_crlb(fim)
    print(f"Position {1}: CRLB=\n{crlb}")

    data_queue.put(
        (1, estimated_pose.x(), estimated_pose.y(), estimated_pose.theta())
    )  # Update Queue

    # Simulating continuous localization updates

    for i in range(1, m):
        estimated_pose = localize(beacons, fm_map, range_m[i, :], path[i, :])

        # Computing FIM & CRLB
        fim = compute_fim(estimated_pose, beacons, variances)
        crlb = compute_crlb(fim)

        print(f"Position {i+1}: CRLB=\n{crlb}")

        # Store the trajectory for real-time plotting
        update_trajectory(estimated_pose)
        data_queue.put(
            (i + 1, estimated_pose.x(), estimated_pose.y(), estimated_pose.theta())
        )

        time.sleep(0.1)  # Simulate delay between measurements

    plot_localization_live(beacons, fm_map, map, path, map_size)  # Show on plot


if __name__ == "__main__":
    main()
