from typing import List, TypedDict


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        web_search: whether to add search
        documents: list of documents
    """

    question: str # Question description in English language
    user_code: str # User provided code
    language: str # Language of code(Python, java, c++,c)
    baseline_code: str # Correct version of code
    generation: str
    web_search: bool
    documents: List[str]
    failing_tc: str # Failing test case (where output of baseline code and user code differs)
    simplified_tc_explanation: str # Dry run of simplified failing test case
    user_reframed_code_with_tc: str # code string ready to go to subprocess module
    baseline_reframed_code_with_tc: str # code string ready to go to subprocess module
    message_stream_for_tc_refinement: str # Message stream for finding correct failing test case    
    message_stream_for_tc_simplification: str # Message stream for simplifying failing test case
    verified_failing_tc: bool # Has the system verified the failing test case?
    valid_tc: bool # Is the test case a valid one ?
    final_explanation: str # Final Dry run example over the failing test case for the provided question
    last_caller: str # Keeps a track of who is the last caller in graph