from state import State


def analyze(state: State):
    return {"analysis": "Analyse fictive de " + state["brand"]}


def report(state: State):
    return {
        "report": f"Rapport fictif sur la reputation de {state['brand']} : {state.get('analysis', '')}"
    }


def detect_crisis(state: State):
    return {"crisis": "crise"}


def report_crisis(state: State):
    return {
        "report": f"Rapport de crise fictif concernant {state['brand']} : {state.get('analysis', '')}"
    }


def evaluate(state: State):
    return {"score": 8}


def routing_function(state: State):
    if state["crisis"]:
        return "crise"
    else:
        return "normal"


def choice_eval(state: State):
    if state["score"] > 7:
        return "END"
    else:
        return "report"


def collect(state: State):
    return {
        "raw_data": {
            "organic": [
                {
                    "title": f"Avis fictif sur {state['brand']}",
                    "snippet": f"Contenu fictif concernant la reputation de {state['brand']}.",
                },
                {
                    "title": f"Polémique fictive autour de {state['brand']}",
                    "snippet": f"Autre source fictive mentionnant {state['brand']}.",
                },
            ]
        }
    }


def sentiment(state: State):
    return {
        "metrics": {
            "sentiment_score": -0.5,
            "themes": ["test"],
            "tonality": "négatif",
            "key_entities": ["test"],
        }
    }
