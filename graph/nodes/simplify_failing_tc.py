from graph.state import GraphState
from graph.chains import simplify_tc_system
from graph.consts import SIMPLIFY_TC

def simplify_failing_tc(state:GraphState)->str:
    print("__SIMPLIFYING_FAILING_TC__")
    if state.get("verified_simplified_tc") == True:
        return {**state}
    
    failing_tc = state.get('failing_tc')
    user_code = state.get('user_code')
    question = state.get('question')

    if failing_tc is None:
        raise ValueError("Failing Test Case not present!")
    
    structured_response = simplify_tc_system.invoke({"question": question, "user_code": user_code, "failing_tc": failing_tc})

    return {**state, "failing_tc": structured_response.simplified_tc,"simplified_tc_explanation": structured_response.reasoning,
            "verified_simplified_tc": False,
            "last_caller": SIMPLIFY_TC}