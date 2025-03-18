PIP = pip3
SOURCE_DIR = src
MAIN = main.py
SEP=/
REQUIREMENTS = requirements.txt
VENV_NAME := venv

ifeq ($(OS),Windows_NT)
    PYTHON_VER = py
    PYTHON = $(VENV_NAME)/Scripts/python
	set PYTHONPATH=%PYTHONPATH%;src;testing
else
	PYTHON_VER = python3
	PYTHON = $(VENV_NAME)/bin/python3
	PYTHONPATH=$$PYTHONPATH:src:testing
endif

.PHONY: venv install run test flake

venv:
	@echo "Creating virtual environment..."
	$(PYTHON_VER) -m venv $(VENV_NAME)
	$(PYTHON) -m pip install --upgrade pip
ifeq ($(OS),Windows_NT)
	cmd /C "call $(VENV_NAME)/Scripts/activate.bat"
endif

install: venv
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install -r $(REQUIREMENTS)

run: venv install
	@echo "Running Python code..."
	$(PYTHON) src/main.py

flake:
	@echo "Flake 8 testing..."
	$(PYTHON) -m flake8 src/*.py
