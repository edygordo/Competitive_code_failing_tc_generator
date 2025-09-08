from typing import List, TypedDict, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


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
    simplified_tc: str # Simplified version of failing test case
    simplified_tc_explanation: str # Dry run of simplified failing test case
