import os, sys
import json
import requests
from groq import Groq, APIError
from langgraph.graph import START, StateGraph, END
from typing_extensions import TypedDict

if os.environ.get("GROQ_API_KEY") is None :
    print('Erreur dans la clé api')
    sys.exit()
if os.environ.get("SERPER_API_KEY") is None :
    print('Erreur dans la clé api SERPER')
    sys.exit()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
model = "llama-3.3-70b-versatile"

url = "https://google.serper.dev/search"

class State(TypedDict):
    brand: str
    analysis: str
    crisis: str
    report: str
    score: int
    raw_data: str
    metrics: dict

def analyze(state: State):
    sources = [
    {"title": r["title"], "snippet": r["snippet"]}
    for r in state["raw_data"]["organic"]
]
    
    message = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": "Tu es un expert en analyse de réputation de marque."},
                  {"role": "user", "content": f"Analyse la réputation de cette marque : {state['brand']} en te basant uniquement sur les infos suivantes : {sources}"}]
    )
    return {"analysis": message.choices[0].message.content}

def report(state: State):
    message = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": "Tu es un expert dans la rédaction de rapport d'analyse de réputation d'entreprise"},
                  {"role": "user", "content": f"formalise l'analyse de la réputation suivant : {state['analysis']}"}]
    )
    return {"report": message.choices[0].message.content}

def detect_crisis(state: State):
    message= client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": "Tu es un expert dans la détéction de crise ou de polémique dans une analyse de réputation"},
                   {"role": "user", "content": f"Détecte s'il y a une crise ou une polémique dans cette analyse de réputation : {state['analysis']} et renvoie 'crise' si tu en detecte une et un string vide sinon."}]
    )
    return {"crisis": message.choices[0].message.content}

def report_crisis(state: State):
    message = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": "Tu es un expert dans la rédaction de rapport d'analyse de réputation d'entreprise"},
                  {"role": "user", "content": f"rédige un rapport de crise concernant la polémique autour de {state['brand']} et l'analyse : {state['analysis']}"}]
    )
    return {"report": message.choices[0].message.content}

def evaluate(state: State):
    message = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": "Ton unique objectif est de lire un rapport et d'en évaluer la qualité avec une note sur 10"},
                  {"role": "user", "content": f"""lit le rapport {state['report']} et renvoie une note sur 10 en format JSON valide de la forme suivante {{"score": 7}} """ }]
    )
    try:
        return {"score": json.loads(message.choices[0].message.content)["score"]}
    except json.JSONDecodeError:
        return {"score": 5}
    

def ronting_function(state: State):
    if state["crisis"]:
        return "crise"
    else:
        return "normal"
def choice_eval(state: State):
    if state["score"] > 7:
        return "END"
    else :
        return "report"
    
def collect(state: State):
    payload = {
    "q": f"{state['brand']} Réputation polémique 2024",
    "gl": "fr",
    "hl": "fr"
    }
    headers = {
    'X-API-KEY': os.environ.get("SERPER_API_KEY"),
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    return {"raw_data": response.json()}

def sentiment(state: State):
    sources = [
    {"title": r["title"], "snippet": r["snippet"]}
    for r in state["raw_data"]["organic"]
]
    
    message = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": """Réponds UNIQUEMENT avec le JSON, sans texte supplémentaire, sans balises markdown. Ton objectif est de construire des métriques à partir de données suivant l'exemple : 
                {"sentiment_score": 0.3,
                "themes": ["sexisme", "performance", "design"],
                "tonality": "négatif",
                "key_entities": ["Colleen Quigley", "JO Paris 2024"]}
                
                "sentiment_score" est un float entre -1 (très négatif) et 1 (très positif)"""},
                  {"role": "user", "content": f'Produit un JSON avec les métriques pour les données suivantes : {sources}'}]
    )
    raw = message.choices[0].message.content
    print(repr(raw))
    try:
        return {"metrics": json.loads(message.choices[0].message.content)}
    except json.JSONDecodeError:
        return {"metrics": {
        "sentiment_score": 0,
        "themes": [],
        "tonality": "inconnu",
        "key_entities": []
    }}
    
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
graph.add_conditional_edges("detect_crisis", ronting_function, {"crise": "report_crisis", "normal": "report" })
graph.add_edge("report", "evaluate")
graph.add_edge("report_crisis", "evaluate_crisis")
graph.add_conditional_edges("evaluate", choice_eval, {"END": END, "report": "report"})
graph.add_conditional_edges("evaluate_crisis", choice_eval, {"END": END, "report": "report_crisis"})


brand = "Nike"
result = graph.compile().invoke({"brand": brand})

print(result["metrics"])