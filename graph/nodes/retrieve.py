from typing import Any, Dict

from graph.state import GraphState
from graph.chains import code_extractor

def retrieve(state: GraphState) -> Dict[str, Any]:
    print("--- RETRIEVAL PHASE ---")

    question = input("Enter your query")
    structuredOutput = code_extractor.invoke(input={"query": question})

    return {**state,"question": question, "user_code": structuredOutput.user_code, "language": structuredOutput.code_language, 
            "baseline_code": structuredOutput.baseline_code,
            "failing_tc": structuredOutput.failing_tc}
