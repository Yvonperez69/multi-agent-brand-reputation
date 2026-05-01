import requests
import time
import json
import os
from state import State
from config import url, model, client

def analyze(state: State):
    sources = [
    {"title": r["title"], "snippet": r["snippet"]}
    for r in state["raw_data"]["organic"]
]
    time.sleep(10)
    message = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": "Tu es un expert en analyse de réputation de marque."},
                  {"role": "user", "content": f"""Voici les métriques de sentiment :{state['metrics']}, 
                                                  Voici les sources : {sources}.
                                                  Analyse la réputation de cette marque : {state['brand']}"""}]
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
        return {"score": json.loads(message.choices[0].message.content)["score"], "steps": state["steps"] + 1}
    except json.JSONDecodeError:
        return {"score": 5, "steps": state["steps"] + 1}
    

def routing_function(state: State):
    if state["crisis"]:
        return "crise"
    else:
        return "normal"
def choice_eval(state: State):
    
    if state["score"] > 7 or state["steps"] >= 1:
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
    try:
        return {"metrics": json.loads(message.choices[0].message.content)}
    except json.JSONDecodeError:
        return {"metrics": {
        "sentiment_score": 0,
        "themes": [],
        "tonality": "inconnu",
        "key_entities": []
    }}