import os
import pytest
import subprocess
import datetime

# Set up folders
results_dir = "../test/results"
os.makedirs(results_dir, exist_ok=True)

# Timestamp for run
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
session_dir = os.path.join(results_dir, timestamp)
os.makedirs(session_dir)

# Gather all test files
test_dir = "../test"
test_files = sorted([f for f in os.listdir(test_dir) if f.startswith("test_") and f.endswith(".py")])

# Track results
summary = []
print("Running tests...\n")

for test_file in test_files:
    test_path = os.path.join(test_dir, test_file)
    result_file = os.path.join(session_dir, f"{test_file[:-3]}_results.txt")

    try:
        with open(result_file, "w") as f:
            proc = subprocess.run(["pytest", test_path, "-v"], stdout=f, stderr=subprocess.STDOUT)
            passed = proc.returncode == 0
            result = "PASSED" if passed else "FAILED"
    except Exception as e:
        result = f"ERROR: {e}"

    summary.append((test_file, result, result_file))

# Print summary
print("\n--- Test Summary ---")
for file, status, path in summary:
    print(f"{file}: {status} (results saved to: {path})")
    

