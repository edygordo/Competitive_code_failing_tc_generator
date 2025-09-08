from graph.state import GraphState
from graph.chains import simplify_tc_system, simplify_tc_explanation
from graph.helpers import checkValidity

def simplify_failing_tc(state:GraphState)->str:
    print("__SIMPLIFYING_FAILING_TC__")
    
    failing_tc = state.get('failing_tc')
    user_code = state.get('user_code')
    question = state.get('question')

    if failing_tc is None:
        raise ValueError("Failing Test Case not present!")
    
    counter = 0
    message_stream_for_tc_simplification: str = failing_tc # Since failing_tc is string(immutable so it wont change)

    while True:
        # Call the LLM to simplify the test case.
        structured_response = simplify_tc_system.invoke({"question": question, "user_code": user_code, "failing_tc": message_stream_for_tc_simplification})

        differ: bool = checkValidity(user_code=user_code, baseline_code=state.get('baseline_code'),test_case=structured_response.simplified_tc)

        message_stream_for_tc_simplification += f"""
        Try another simplification example as this simplification is not valid.
        Simplified test case:{message_stream_for_tc_simplification.simplified_tc}
        You applied this reasoning earlier:- {message_stream_for_tc_simplification.reasoning}
        """

        if differ:

            # Provide a dry run example of the test case to user
            explanation = simplify_tc_explanation.invoke({"question": question, "user_code": user_code, "simplified_failing_tc": structured_response.simplified_tc})
            break
        elif counter == 5:
            print("__MAX_TRIES_TO_SIMPLIFY_REACHED__")
            break
        else:
            continue


    return {**state, "simplified_tc": structured_response.simplified_tc,"simplified_tc_explanation": explanation}