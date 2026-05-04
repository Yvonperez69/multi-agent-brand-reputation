# Multi Agent Brand Reputation

Il s'agit d'un projet personel dans le but d'apprendre à coder. Le projet consiste à éffectuer des analyses sur entreprises et marques concernant leur répution et les potentielles polémiques les concernant, le projet contient (à l'heure actuelle) trois briques : 
- Un système multi-agent qui rédige un rapport pour une entreprise donnée
- Un chat bot avec RAG qui lui permet de discuter en se basant sur les précedents rapports 
- Un historique qui permet de lire les anciens rapports déjà produits par le premier système

## Architecture

### système multi-agent

```markdown
- `graph.py` — définition du pipeline LangGraph
- `nodes.py` — nœuds du pipeline
- `nodes_mock.py` — nœuds fictifs pour le mode dev
- `config.py` — configuration et clients API
- `state.py` — définition du State
- `storage.py` — persistance JSON et ChromaDB
- `app.py` — interface Streamlit
```

structure du graphe (graph.py)

```text
START
  -> collect
  -> sentiment
  -> analyze
  -> detect_crisis
      -> report
      -> or report_crisis
  -> evaluate
      -> END si score > 7
      -> sinon nouvelle génération du rapport
```

## Configuration

Crée un fichier `.env` à la racine :
```text
GROQ_API_KEY=ta_clé
SERPER_API_KEY=ta_clé
````

## Installation 

```code 
pip install -r requirements.txt
```

## Lancement 

```code 
streamlit run app.py
```

### Auteur : Yvon PEREZ