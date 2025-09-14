from typing import Any, Dict, List
from graph.state import GraphState
from graph.chains.failing_tc_extractor import failing_tc_extractor
from graph.helpers import checkValidity
from graph.consts import FAILING_TC_GENERATION

def generate_failing_tc(state: GraphState)->Dict[str, Any]:
    print("__GENERATING_VALID_FAILING_TC__")
    # See if the existing Test case is a valid failing test case if yes then return as is
    if state.get('verified_failing_tc') == True: # If the result has been verified then return the state
        return {**state}
    
    question: str = state.get('question') # Question in english language
    baseline_code: str = state.get('baseline_code')
    user_code: str = state.get('user_code')
    message_stream_for_tc_refinement: str|None = state.get('message_stream_for_tc_refinement') or ""
    
    # Generate a failing test case using question description
    structured_tc_response = failing_tc_extractor.invoke({"question":question,
                                                          "user_code": user_code,
                                                          "baseline_code": baseline_code,
                                                          "all_messages": message_stream_for_tc_refinement})

    message_stream_for_tc_refinement += f"The previous test case generated: {structured_tc_response.edge_case} + Reasoning was: {structured_tc_response.reasoning} but this case is invalid so generate some other edge case."

    return {**state, "failing_tc": structured_tc_response.edge_case if structured_tc_response and structured_tc_response.edge_case else "EMPTY",
            "message_stream_for_tc_refinement": message_stream_for_tc_refinement,
            "verified_failing_tc": False, # As new failing test case generated
            "last_caller": FAILING_TC_GENERATION
            }