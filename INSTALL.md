Instructions for installing 2D-Localizer.  
----------------------------------------------- 

User of this program can install the software in the src folder on Linux/macOS

1. Clone this repository
2. `cd src`- to direct your terminal to the src/ folder
3. `make install` - to set up the virtual environment and dependencies using the Makefile
4. `source .venv/bin/activate` - to activate the environment
4. Modify the `user_input.yaml` file to desired values
5. `chmod +x ./run.sh` - to grant permission to execute the run.sh file
6. `./run.sh` - to execute the program (make sure you are in the src folder)

To test if the program is working:

run `make test` while still in the src folder to run all unit tests

