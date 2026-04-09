from nodes import collect, sentiment, analyze, detect_crisis, report, report_crisis, evaluate, routing_function, choice_eval
from state import State
from langgraph.graph import START, StateGraph, END
from storage import save_result

graph = StateGraph(State)

# Nodes
graph.add_node("collect", collect)
graph.add_node("sentiment", sentiment)
graph.add_node("analyze", analyze)
graph.add_node("detect_crisis", detect_crisis)
graph.add_node("report", report)
graph.add_node("report_crisis", report_crisis)
graph.add_node("evaluate", evaluate)
graph.add_node("evaluate_crisis", evaluate)
# EDGES
graph.add_edge(START, "collect")
graph.add_edge("collect", "sentiment")
graph.add_edge("sentiment", "analyze")
graph.add_edge("analyze", "detect_crisis")
graph.add_conditional_edges("detect_crisis", routing_function, {"crise": "report_crisis", "normal": "report" })
graph.add_edge("report", "evaluate")
graph.add_edge("report_crisis", "evaluate_crisis")
graph.add_conditional_edges("evaluate", choice_eval, {"END": END, "report": "report"})
graph.add_conditional_edges("evaluate_crisis", choice_eval, {"END": END, "report": "report_crisis"})


brand = input("Nom de la marque : ",)
result = graph.compile().invoke({"brand": brand})

save_result(brand=brand, result=result)