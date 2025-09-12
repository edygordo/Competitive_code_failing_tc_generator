from typing import Any, Dict
from graph.state import GraphState
from graph.chains import rephrasing_tc
from graph.consts import REPHRASER_CODE_STRING

def rephraser_tc_for_subprocess(state: GraphState) -> Dict[str, Any]:

    failing_tc = state['failing_tc']
    user_code = state['user_code']
    baseline_code = state['baseline_code']

    user_rephrased_code_with_tc = rephrasing_tc.invoke({"code_string": user_code, "test_case": failing_tc})

    baseline_rephrased_code_with_tc = rephrasing_tc.invoke({"code_string": baseline_code, "test_case": failing_tc})

    return {**state, "user_reframed_code_with_tc": user_rephrased_code_with_tc.rephrased_tc, 
            "baseline_reframed_code_with_tc": baseline_rephrased_code_with_tc.rephrased_tc,
            "last_caller": REPHRASER_CODE_STRING}