REQUIREMENTS = requirements.txt
VENV_NAME := .venv
PYTHON_VER := python3.10
PYTHON := $(VENV_NAME)/bin/python3.10

venv:
	@echo "Creating virtual environment..."
	@if [ ! -d "$(VENV_NAME)" ]; then \
		sudo apt update -y && \
		sudo apt install -y python3.10-venv python3.10-tk && \
		$(PYTHON_VER) -m venv $(VENV_NAME); \
	else \
		echo "Virtual environment already exists."; \
	fi

install: venv
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r $(REQUIREMENTS)

clean:
	rm -rf $(VENV_NAME) __pycache__ *.pyc