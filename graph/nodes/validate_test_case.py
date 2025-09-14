from graph.helpers import checkValidity
from graph.state import GraphState
from graph.chains import rephrasing_tc
from typing import Dict, Any
from graph.consts import CHECK_VALIDITY


def validate_test_case(state: GraphState)->Dict[str,Any]:
    " This should be a trampoline node the state valid_tc and verified_failing_tc is updated by this node"
    user_code = state.get('user_code')
    baseline_code = state.get('baseline_code')
    failing_tc = state.get('failing_tc')

    user_rephrased_code_with_tc = rephrasing_tc.invoke({"code_string": user_code, "test_case": failing_tc})
    baseline_rephrased_code_with_tc = rephrasing_tc.invoke({"code_string": baseline_code, "test_case": failing_tc})
    valid_failing_tc = False
    
    if checkValidity(user_rephrased_code_with_tc.rephrased_tc, baseline_rephrased_code_with_tc.rephrased_tc):
        valid_failing_tc = True
    else:
        valid_failing_tc = False

    return {**state, 'valid_tc': valid_failing_tc, 'verified_failing_tc': True, 'verified_simplified_tc': True} # Always make the verified True