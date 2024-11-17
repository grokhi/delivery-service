#!/bin/bash

# Define the directory where test files are located
TEST_DIR="./tests/parcels"

# Check if the directory exists
if [ ! -d "$TEST_DIR" ]; then
  echo "Test directory '$TEST_DIR' does not exist."
  exit 1
fi

# Loop through all the .py files in the test directory, excluding __init__.py
for test_file in "$TEST_DIR"/*.py; do
  # Skip __init__.py file
  if [[ "$(basename "$test_file")" == "__init__.py" ]]; then
    echo "Skipping __init__.py"
    continue
  fi

  # Check if it's a valid file and run pytest
  if [ -f "$test_file" ]; then
    echo "Running pytest on $test_file"
    pytest "$test_file" || { echo "Test failed for $test_file"; exit 1; }
  fi
done

echo "All tests completed."
