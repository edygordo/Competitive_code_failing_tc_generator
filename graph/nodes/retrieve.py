from typing import Any, Dict

from graph.state import GraphState
from graph.consts import RETRIEVE

def retrieve(state: GraphState) -> Dict[str, Any]:
    print("--- RETRIEVAL PHASE ---")

    return {**state,"question": state.get("question"), "user_code": state.get("user_code"), "language": state.get("language"), 
            "baseline_code": state.get("baseline_code"),
            "failing_tc": state.get("failing_tc"),
            "last_caller": RETRIEVE}
