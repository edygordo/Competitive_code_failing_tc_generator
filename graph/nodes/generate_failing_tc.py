from typing import Any, Dict, List
from graph.state import GraphState
from graph.chains.failing_tc_extractor import failing_tc_extractor
from graph.helpers import checkValidity


def generate_failing_tc(state: GraphState)->Dict[str, Any]:
    print("__GENERATING_VALID_FAILING_TC__")

    question: str = state.get('question') # Question in english language
    baseline_code: str = state.get('baseline_code')
    user_code: str = state.get('user_code')
    message_stream_for_tc_refinement: str = ""
    
    # Append question to begin with
    message_stream_for_tc_refinement += question
    counter=0
    while True:
        # Printing Message stream
        print("The message stream for retrying is", message_stream_for_tc_refinement)

        # Logic the user_code and baseline code output should differ
        structured_tc_response = failing_tc_extractor.invoke({"all_messages": message_stream_for_tc_refinement})

        # Append response of LLM to message_stream for further refinement
        message_stream_for_tc_refinement += f"""
        Try generating another test case as this is not valid:- {structured_tc_response.edge_case}
        The reasoning you applied before:- {structured_tc_response.reasoning}.
        Try some other reasoning
        """

        # Check wether this test case is VALID or NOT
        differ: bool = checkValidity(user_code=user_code, baseline_code=baseline_code,test_case=structured_tc_response.edge_case)
        
        counter = counter+1
        
        if differ:
            break
        elif counter ==5:
            print("__MAXIMUM_TRIES_ACHIEVED__")
            break
        else:
            continue

    return {**state, "failing_tc": structured_tc_response.edge_case if structured_tc_response and structured_tc_response.edge_case else "EMPTY"}