# Competitive_code_failing_tc_generator
An agentic workflow to generate a simplified failing test case for a given question given the correct(Baseline Code), User code and Failing Test Case(Optional)


## Steps to activate and run main file

1. Install poetry in the system.
2. Activate poetry virtual environment using: poetry env activate( previously poetry shell) and copy the location for later activation of this environment.
3. Add all the dependencies in the poetry environment just created using: poetry install
4. (Optional) Set your editors path to the python executables for correct suggesstions and type hints using: poetry env info- copy & paste Executable location in the interpreters path.
5. Then Activate the setted up environment in terminal using: source <environment_activate_path>


## To run Docker image

1. Install langgraph-cli.
2. Run langgraph up
