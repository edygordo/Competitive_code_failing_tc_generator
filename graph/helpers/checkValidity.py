import subprocess


def checkValidity(user_code: str, baseline_code: str)->bool:
    """
    Run user_code and baseline_code against the embedded test case.
    Return True if outputs differ, else False.
    """
    print("___CHECKING VALIDITY OF USER VS BASELINE CODE AGAINST THE GENERATED TEST CASE___")

    # Run user code in a subprocess
    user_process = subprocess.run(
        ["python3", "-c", user_code],
        text=True,
        capture_output=True
    )

    # Run baseline code in a subprocess and capture it's output stream
    baseline_process = subprocess.run(
        ["python3", "-c", baseline_code],
        text=True,
        capture_output=True
    )
    
    # Print output of both the process
    if user_process.stderr is None:    
        print("User code output", user_process.stdout)
    else:
        print(user_process.stderr)

    
    if baseline_process.stderr is None:
        print("Baseline code output", baseline_process.stdout)
    else:
        print(baseline_process.stderr)

    return user_process.stdout != baseline_process.stdout