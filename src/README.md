# 2D Localizer Source Code

The folders and files for this project are as follows:
```
├── src/                  # Source code
│   ├── __init__.py
│   ├── accuracy.py       # Computes accuracy matrices
│   ├── gtsam_wrapper.py  # Wrapper around GTSAM functionality
│   ├── input_format.py   # Parses input YAML/CSV files
│   ├── localization.py   # Core localization algorithm
│   ├── main.py           # Entry point; runs the full pipeline
│   ├── output.py         # Tabular output of estimated poses
│   ├── plot.py           # Visualization of paths and estimates
│   ├── simulation.py     # Generates simulated sensor data
│   ├── inputs/           # Sample inputs (CSV, images)
│   │   └── ...           # e.g., trajectories, beacons, maps
│   ├── Makefile          # Environment setup and automation tasks
│   ├── README.md         
│   ├── requirements.txt  # Python dependencies
│   ├── run.sh            # Shell script for quick execution
│   ├── user_input.yaml   # Example YAML input configuration
```
Make sure that your directory is in this folder when running code