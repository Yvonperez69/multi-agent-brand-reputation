import json
from config import collection
from datetime import datetime
import os

def save_result(brand, result):
    date = datetime.now().strftime("%Y-%m-%d")
    fichier = f"{brand}_{date}.json"
    path = os.path.join("report", fichier)
    os.makedirs("report", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    n = collection.count()
    collection.add(
	ids=[f"id{n}"],
	documents=[result["report"]],
    metadatas= [{"brand":brand, "date":date, "metrics": json.dumps(result["metrics"]), "score":result["score"]}]
    )
    print(collection.count())
    print(f"Rapport sauvegardé dans : {path}")
