# Multi-Agent Brand Reputation

Projet expérimental autour des agents LLM en Python, avec un focus sur l'analyse de réputation de marque via un graphe d'agents construit avec LangGraph.

Le dépôt contient deux démonstrations :

- `graph.py` : pipeline principal d'analyse de réputation de marque.
- `main.py` : exemple simple de tool calling avec une fausse fonction météo.

## Objectif

L'objectif principal du projet est d'automatiser une analyse de réputation de marque à partir de résultats de recherche web, puis de produire un rapport adapté au contexte :

- rapport standard si aucun signal de crise n'est détecté ;
- rapport de crise si une polémique ou un risque réputationnel est identifié.

## Focus sur `graph.py`

`graph.py` implémente un workflow de type multi-agent avec LangGraph. Chaque noeud du graphe remplit une tâche précise :

1. `collect`
   Récupère des résultats web via l'API Serper à partir d'une requête sur la marque.
2. `analyze`
   Demande au modèle d'analyser la réputation de la marque à partir des snippets collectés.
3. `detect_crisis`
   Vérifie si l'analyse fait apparaître une crise ou une polémique.
4. `report` / `report_crisis`
   Génère soit un rapport standard, soit un rapport orienté gestion de crise.
5. `evaluate`
   Évalue la qualité du rapport produit avec une note sur 10.
6. boucle d'amélioration
   Si la note est insuffisante, le graphe relance la génération du rapport jusqu'à dépasser le seuil attendu.

### Logique du graphe

```text
START
  -> collect
  -> analyze
  -> detect_crisis
      -> report
      -> or report_crisis
  -> evaluate
      -> END si score > 7
      -> sinon nouvelle génération du rapport
```

### Ce que fait concrètement le script

- charge `GROQ_API_KEY` et `SERPER_API_KEY` depuis l'environnement ;
- interroge Serper pour obtenir des résultats de recherche ;
- utilise un modèle Groq pour produire une analyse de réputation ;
- choisit dynamiquement le type de rapport ;
- note automatiquement la sortie finale.

À l'heure actuelle, la marque analysée est définie en dur dans `graph.py` avec `brand = "Nike"`.

## Structure du dépôt

```text
.
├── graph.py      # graphe multi-agent d'analyse de réputation
├── main.py       # exemple de conversation avec tool calling
├── weather.py    # outil météo fictif utilisé par main.py
└── Untitled.ipynb
```

## Prérequis

- Python 3.10+
- un compte ou accès API Groq
- une clé API Serper

## Installation

Installe les dépendances Python nécessaires :

```bash
pip install groq langgraph requests typing_extensions
```

Définis ensuite les variables d'environnement :

```bash
export GROQ_API_KEY="..."
export SERPER_API_KEY="..."
```

## Exécution

### Analyse de réputation

```bash
python3 graph.py
```

Le script compile le graphe puis exécute l'analyse complète pour la marque définie dans le fichier.

### Démo tool calling

```bash
python3 main.py
```

Cette seconde démo lance une boucle interactive où le modèle peut appeler un outil météo fictif défini dans `weather.py`


## Technologies utilisées

- Python
- Groq API
- LangGraph
- Requests
- TypedDict

## Auteur

Yvon Perez
