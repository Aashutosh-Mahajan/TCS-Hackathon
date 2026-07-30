"""
LangGraph Pipeline — assembles all 6 agents into a directed graph.

Pipeline flow:
  language → retriever → answer → grounding → confidence → explainer

Each node receives the full PipelineState and returns updates to merge back.
The graph is compiled once and reused for all queries.
"""

from langgraph.graph import StateGraph, START, END

from app.agents.state import PipelineState
from app.agents.language_agent import language_agent
from app.agents.retriever_agent import retriever_agent
from app.agents.answer_agent import answer_agent
from app.agents.grounding_agent import grounding_agent
from app.agents.confidence_agent import confidence_agent
from app.agents.explainer_agent import explainer_agent


def build_graph():
    """Build and compile the LangGraph agent pipeline."""

    # Create the state graph
    graph = StateGraph(PipelineState)

    # Add all agent nodes
    graph.add_node("language", language_agent)
    graph.add_node("retriever", retriever_agent)
    graph.add_node("answer", answer_agent)
    graph.add_node("grounding", grounding_agent)
    graph.add_node("confidence", confidence_agent)
    graph.add_node("explainer", explainer_agent)

    # Define the linear pipeline flow
    graph.add_edge(START, "language")
    graph.add_edge("language", "retriever")
    graph.add_edge("retriever", "answer")
    graph.add_edge("answer", "grounding")
    graph.add_edge("grounding", "confidence")
    graph.add_edge("confidence", "explainer")
    graph.add_edge("explainer", END)

    # Compile into a runnable
    compiled = graph.compile()
    return compiled


# Module-level compiled graph (built once, reused)
_compiled_graph = None


def get_graph():
    """Get the compiled graph (lazy initialization)."""
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph


async def run_pipeline(query: str) -> PipelineState:
    """
    Execute the full agent pipeline for a query.

    Args:
        query: User question in any supported language.

    Returns:
        Complete PipelineState with all agent outputs.
    """
    graph = get_graph()

    # Initialize state with the query and empty trace
    initial_state: PipelineState = {
        "query": query,
        "agent_trace": [],
    }

    # Run the graph — LangGraph handles state merging across nodes
    result = await graph.ainvoke(initial_state)
    return result
