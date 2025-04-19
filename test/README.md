# Automated Tests

The folders and files for this folder are as follows:


```
test/                         # Unit test folder
├── __init__.py               
├── README.md                 
├── test_accuracy.py          # Tests FIM, CRLB, and RMSE logic
├── test_input_file.py        # Validates structure of input files
├── test_input.yaml           # Example YAML input used in tests
├── test_inputs.py            # Checks validity of input data
├── test_pose_estimation.py   # Evaluates estimated poses
├── test_visuals.py           # Tests trajectory and visualization
├── unit_tests.py             # Master file to run all other tests
├── inputs/                   # Sample input files for testing
|       └── ...                (e.g., synthetic CSV/YAML)
├── results/                   # Output directory for test results
|       └── ...                (e.g., summary .txt files)

```