import io
import sys

def run_python_code(code_string: str, input_data=None):
    """
    Executes Python code from a string with input_data available as a variable.
    Returns the 'result' variable if defined, otherwise printed output.
    """
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    try:
        local_scope = {"input_data": input_data}
        exec(code_string, {}, local_scope)
        printed_output = sys.stdout.getvalue().strip()
        result = local_scope.get("result", None)
        
        # Prefer result variable, else fallback to printed output
        return result if result is not None else printed_output
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        sys.stdout = old_stdout


def checkValidity(user_code: str, baseline_code: str, test_case: str)->bool:
    """
    Run user_code and baseline_code against the same test_case.
    Return True if outputs differ, else False.
    """
    user_output = run_python_code(user_code, test_case)
    baseline_output = run_python_code(baseline_code, test_case)
    print("The functions ran")
    return user_output != baseline_output