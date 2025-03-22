REQUIREMENTS = requirements.txt
VENV_NAME := .venv

ifeq ($(OS),Windows_NT)
    PYTHON_VER = py
    PYTHON = $(VENV_NAME)/Scripts/python
else
	PYTHON_VER = python3
	PYTHON = $(VENV_NAME)/bin/python3
endif

venv:
	@echo "Creating virtual environment..."
	$(PYTHON_VER) -m venv $(VENV_NAME)
ifeq ($(OS),Windows_NT)
	cmd /C "call $(VENV_NAME)/Scripts/activate.bat"
endif

install: venv
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r $(REQUIREMENTS)
