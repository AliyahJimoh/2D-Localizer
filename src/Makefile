REQUIREMENTS = requirements.txt
VENV_NAME := .venv
PYTHON_VER_LINUX := python3.10
PYTHON_VER_MAC := python@3.10
PYTHON := $(VENV_NAME)/bin/python3.10

venv:
	@echo "Creating virtual environment..."
	@if [ ! -d "$(VENV_NAME)" ]; then \
		if [ "$$(uname)" = "Darwin" ]; then \
			echo "Detected macOS. Installing dependencies with brew (if needed)..."; \
			brew install $(PYTHON_VER_MAC) || true; \
			$(PYTHON_VER_MAC) -m venv $(VENV_NAME); \
		else \
			echo "Detected Linux. Installing dependencies with apt..."; \
			sudo apt update -y && \
			sudo apt install -y python3.10-venv python3.10-tk && \
			$(PYTHON_VER_LINUX) -m venv $(VENV_NAME); \
		fi \
	else \
		echo "Virtual environment already exists."; \
	fi

install: venv
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r $(REQUIREMENTS)


.PHONY: test

test: 
	$(PYTHON) ../test/unit_tests.py

clean:
	rm -rf $(VENV_NAME) __pycache__ *.pyc