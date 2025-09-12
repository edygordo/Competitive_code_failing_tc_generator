from graph.state import GraphState
from typing import Dict, Any
from graph.chains import explaning_failing_tc
from graph.consts import EXPLAIN_TEST_CASE

def final_explanation(state:GraphState)->Dict[str, Any]:
    "Generate a simple dry run explaination of the failing test case provided"

    failing_tc = state.get("failing_tc")
    question = state.get("question")
    user_code = state.get("user_code")

    # Make a chain which finds an explanation and feeds to the state
    structured_response = explaning_failing_tc.invoke({"code_string": user_code,"test_case": failing_tc,"question": question})
    return {**state, "final_explanation": structured_response.explanation, "last_caller": EXPLAIN_TEST_CASE}