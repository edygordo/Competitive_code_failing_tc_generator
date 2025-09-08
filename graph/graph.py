from dotenv import load_dotenv
from langgraph.graph import END, StateGraph, START
from graph.consts import RETRIEVE, FAILING_TC_GENERATION, SIMPLIFY_TC, FAILING_TC_GENERATION
from graph.nodes import retrieve, generate_failing_tc, simplify_failing_tc
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



workflow = StateGraph(GraphState)

# Add Node to Graph
workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(FAILING_TC_GENERATION, generate_failing_tc)
workflow.add_node(SIMPLIFY_TC, simplify_failing_tc)

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
workflow.add_edge(SIMPLIFY_TC, END)
workflow.add_edge(FAILING_TC_GENERATION, END)

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
