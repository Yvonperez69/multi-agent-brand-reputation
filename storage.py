import json
from datetime import datetime
import os

def save_result(brand, result):
    date = datetime.now().strftime("%Y-%m-%d")
    fichier = f"{brand}_{date}.json"
    path = os.path.join("report", fichier)
    os.makedirs("report", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
        
    print(f"Rapport sauvegardé dans : {path}")