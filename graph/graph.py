from dotenv import load_dotenv
from langgraph.graph import END, StateGraph
from graph.consts import RETRIEVE, SIMPLIFY_TC, FAILING_TC_GENERATION, REPHRASER_CODE_STRING, CHECK_VALIDITY, EXPLAIN_TEST_CASE
from graph.nodes import retrieve, generate_failing_tc, simplify_failing_tc, rephraser_tc_for_subprocess, validate_test_case, final_explanation
from graph.state import GraphState

load_dotenv()


def decide_if_failing_tc_provided(state)->str:
    print("---FAILING TEST CASE PROVIDED?---")

    if state.get("failing_tc"):
        print("Failing test case found! Proceeding to Simplify it")
        return SIMPLIFY_TC
    else:
        print("Failing Test case not provided. Generating a Failing test case")
        return FAILING_TC_GENERATION

def decide_to_verify_or_simplify_or_regenerate(state:GraphState)->str:
    print("---SHOULD WE VERIFY OR SIMPLIFY OR REGENERATE---")
    if state.get("failing_tc") == "EMPTY" or (state.get("valid_tc") == False and state.get("verified_failing_tc") == True):
        print("--REGENERATING TEST CASE AS TEST CASE PRODUCED NOT VALID OR EMPTY!--")
        return FAILING_TC_GENERATION
    elif state.get("verified_failing_tc") == False:
        print("--VERIFYING FAILING TEST CASE--")
        return CHECK_VALIDITY
    else:
        print("--PROCEED TO SIMPLIFY TEST CASE--")
        return SIMPLIFY_TC

def decide_to_verify_explain_regenerate(state:GraphState)->str:
    print("---SHOULD WE REGENERATE OR VERIFY OR PROCEED WITH EXPLAINATION---")
    if state.get("failing_tc") == "EMPTY" or (state.get("valid_tc") == False and state.get("verified_simplified_tc") == True):
        print("--REGENERATING TEST CASE AS TEST CASE PRODUCED NOT VALID OR EMPTY!--")
        return SIMPLIFY_TC
    elif state.get("verified_simplified_tc") == False:
        print("--VERIFYING FAILING TEST CASE--")
        return CHECK_VALIDITY
    else:
        print("--PROCEED TO EXPLAIN THE SIMPLIFIED TEST CASE--")
        return EXPLAIN_TEST_CASE

def back_to_caller(state:GraphState)->str:
    return state.get("last_caller")

workflow = StateGraph(GraphState)

# Add Node to Graph
workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(FAILING_TC_GENERATION, generate_failing_tc)
workflow.add_node(SIMPLIFY_TC, simplify_failing_tc)
workflow.add_node(CHECK_VALIDITY, validate_test_case)
workflow.add_node(EXPLAIN_TEST_CASE, final_explanation)

# Add connections between nodes in the Graph
workflow.set_entry_point(RETRIEVE) # Set entry point in graph
workflow.add_conditional_edges(
    RETRIEVE,
    decide_if_failing_tc_provided,
    {
        SIMPLIFY_TC: SIMPLIFY_TC,
        FAILING_TC_GENERATION: FAILING_TC_GENERATION,
    }
)

workflow.add_conditional_edges(
    FAILING_TC_GENERATION,
    decide_to_verify_or_simplify_or_regenerate,
    {
        FAILING_TC_GENERATION: FAILING_TC_GENERATION,
        CHECK_VALIDITY: CHECK_VALIDITY,
        SIMPLIFY_TC: SIMPLIFY_TC
    }    
)


workflow.add_conditional_edges(
    SIMPLIFY_TC,
    decide_to_verify_explain_regenerate,
    {
        SIMPLIFY_TC: SIMPLIFY_TC,
        CHECK_VALIDITY: CHECK_VALIDITY,
        EXPLAIN_TEST_CASE: EXPLAIN_TEST_CASE
    }
)

# Trampoline edge
workflow.add_conditional_edges(
    CHECK_VALIDITY,
    back_to_caller,
    {
        FAILING_TC_GENERATION: FAILING_TC_GENERATION,
        SIMPLIFY_TC: SIMPLIFY_TC,
    }
)

workflow.add_edge(EXPLAIN_TEST_CASE, END)

app = workflow.compile()

# Generate a diagram
app.get_graph().draw_mermaid_png(output_file_path="graph.png")










# workflow.add_node(RETRIEVE, retrieve)
# workflow.add_node(GRADE_DOCUMENTS, grade_documents)
# workflow.add_node(GENERATE, generate)
# workflow.add_node(WEBSEARCH, web_search)

# workflow.set_conditional_entry_point(
#     route_question,
#     {
#         WEBSEARCH: WEBSEARCH,
#         RETRIEVE: RETRIEVE,
#     },
# )
# workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
# workflow.add_conditional_edges(
#     GRADE_DOCUMENTS,
#     decide_to_generate,
#     {
#         WEBSEARCH: WEBSEARCH,
#         GENERATE: GENERATE,
#     },
# )

# workflow.add_conditional_edges(
#     GENERATE,
#     grade_generation_grounded_in_documents_and_question,
#     {
#         "not supported": GENERATE,
#         "useful": END,
#         "not useful": WEBSEARCH,
#     },
# )
# workflow.add_edge(WEBSEARCH, GENERATE)
# workflow.add_edge(GENERATE, END)

# app = workflow.compile()

# app.get_graph().draw_mermaid_png(output_file_path="graph.png")
