import streamlit as st
import requests
import os
import PyPDF2
from pathlib import Path
import base64

# Configuration de l'interface
st.set_page_config(
    page_title="Moteur de Recherche en Droit Commercial",
    page_icon="⚖️",
    layout="wide"
)

# URL de l'API
API_URL = "http://localhost:8000"

def main():
    st.title("⚖️ Moteur de Recherche en Droit Commercial")
    
    # Sidebar pour les options
    with st.sidebar:
        st.header("Options de recherche")
        search_type = st.selectbox(
            "Type de recherche",
            ["hybrid", "keyword", "semantic"],
            help="Choisissez la méthode de recherche"
        )
        
        limit = st.slider(
            "Nombre de résultats",
            min_value=1,
            max_value=20,
            value=10
        )
        
        if st.button("Réindexer les documents"):
            with st.spinner("Indexation en cours..."):
                response = requests.post(f"{API_URL}/index")
                if response.status_code == 200:
                    st.success("Indexation terminée avec succès!")
                else:
                    st.error("Erreur lors de l'indexation")
    
    # Zone de recherche principale
    query = st.text_input("Entrez votre requête juridique")
    
    if query:
        with st.spinner("Recherche en cours..."):
            try:
                response = requests.get(
                    f"{API_URL}/search",
                    params={
                        "query": query,
                        "search_type": search_type,
                        "limit": limit
                    }
                )
                
                if response.status_code == 200:
                    results = response.json()
                    
                    if results:
                        for i, result in enumerate(results, 1):
                            with st.expander(f"{i}. {result['title']} (Score: {result['score']:.4f})"):
                                with open(result['path'],"rb") as f:
                                    base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
                                    st.markdown(pdf_display, unsafe_allow_html=True)
                                
                    else:
                        st.info("Aucun résultat trouvé")
                        
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur de connexion à l'API: {e}")

if __name__ == "__main__":
    main()