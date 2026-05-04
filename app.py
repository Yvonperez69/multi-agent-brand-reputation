import streamlit as st
from graph import compiled_graph
from storage import save_result
from config import client, model, collection
import os
import json
import time

st.set_page_config(page_title="Brand Reputation", page_icon="📊", layout="centered")
st.title("Analyse de réputation")
st.caption("Interface minimale pour lancer une analyse de marque.")
tab1, tab2, tab3 = st.tabs(["Analyse", "Chatbot", "historique"])

def chat_bot(prompt,hist):
    
    key_words = ["marque", "réputation", "rapport", "analyse", "crise", "polémique",'tonalité', "score","métrique", "métriques", "sentiment", "sources", "contexte"]
    contexte = ""
    
    if any(kw in prompt.lower() for kw in key_words):
        results = collection.query(
            query_texts=[prompt],
            n_results=2
        )
        contexte = "\n\n".join(results["documents"][0])
        metadatas = results["metadatas"][0]
    
    stream = client.chat.completions.create(
    messages=[{"role":"system", "content":f"Tu es un Chat Bot dans une app d'analyse et rédaction de rapport sur la réputation de marques. Reponds en te basant sur ces rapports :{contexte} et les métadonnées : {metadatas}"},
              *hist,
              {"role":"user", "content":prompt}],
    model=model,
    stream=True
)
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

def run_analysis(brand: str):
    node_labels = {
        "collect": "🔍 Collecte des données...",
        "sentiment": "📊 Analyse du sentiment...",
        "analyze": "🧠 Analyse de la réputation...",
        "detect_crisis": "⚠️ Détection de crise...",
        "report": "📝 Rédaction du rapport...",
        "report_crisis": "🚨 Rédaction du rapport de crise...",
        "evaluate": "⭐ Évaluation du rapport...",
        "evaluate_crisis": "⭐ Évaluation du rapport de crise...",
    }
    try:
        result = {}
        with st.status("Analyse en cours...") as status:
            for update in compiled_graph.stream({"brand": brand, "steps": 0}, stream_mode="updates"):
                node_name = list(update.keys())[0]
                status.update(label=node_labels.get(node_name, node_name))
                result.update(update[node_name])
            status.update(label="✅ Analyse terminée !", state="complete")
        return result, None
    except SystemExit:
        return None, "Définis `GROQ_API_KEY` et `SERPER_API_KEY` avant de lancer l'analyse."
    except Exception as exc:
        return None, str(exc)

with tab1:
    with st.form("analysis_form"):
        brand = st.text_input("Nom de la marque", placeholder="Apple")
        save_to_file = st.checkbox("Sauvegarder le résultat", value=True)
        submitted = st.form_submit_button("Lancer l'analyse", type="primary")

    if submitted:
        brand = brand.strip()
        t1 = time.time()
        
        if not brand:
            st.warning("Saisis un nom de marque.")
        else:
            result, error = run_analysis(brand)

            if error:
                st.error(error)
            else:
                t2 = time.time()
                if save_to_file:
                    save_result(brand=brand, result=result)

                metrics = result.get("metrics", {})
                score = result.get("score", "-")
                tonality = metrics.get("tonality", "-")
                st.metric(label="Durée de l'analyse", value=f"{t2 - t1:.1f}s")

                st.success("Analyse terminée.")
                col1, col2 = st.columns(2)
                col1.metric("Score", score)
                col2.metric("Tonalité", tonality)

                if result.get("report"):
                    st.subheader("Rapport")
                    st.write(result["report"])

                if result.get("analysis"):
                    with st.expander("Analyse détaillée"):
                        st.write(result["analysis"])

                with st.expander("Résultat complet"):
                    st.json(result)

with tab2:
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])    
        
    if prompt := st.chat_input( ):
            # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = st.write_stream(chat_bot(prompt, st.session_state.messages[-3:]))
            st.session_state.messages.append({"role": "assistant", "content": response})


with tab3:
    option = st.selectbox(
    "Choisissez parmis les rapports suivants",
    (os.listdir("report")),
)

    st.write("You selected:", option)
    with open(os.path.join("report",option), "r") as f:
        result = json.load(f)
        
        metrics = result.get("metrics", {})
        score = result.get("score", "-")
        tonality = metrics.get("tonality", "-")
        
        col1, col2 = st.columns(2)
        col1.metric('score', score)
        col2.metric("tonalité", tonality)
        
        if result.get("report"):
            st.subheader("Rapport")
            st.write(result["report"])
            
        if result.get("analysis"):
            with st.expander("Analyse détaillée"):
                st.write(result["analysis"])
                
        with st.expander("Résultat complet"):
            st.json(result)