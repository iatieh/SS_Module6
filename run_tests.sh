# run_tests.sh
#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run flake8 for linting
echo "Running flake8..."
flake8 .

# Run bandit for security checks
echo "Running bandit..."
bandit -r .

# Run unit tests
echo "Running unit tests..."
python -m unittest discover -s tests

# Deactivate virtual environment
deactivate
