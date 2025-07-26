#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version Web de l'Optimiseur de Maillage Interne SEO
Utilise Streamlit pour une interface web simple et efficace
"""

import streamlit as st
import os
import json
import time
import pandas as pd
from datetime import datetime
from pathlib import Path
import webbrowser
import threading
import queue
from io import BytesIO

# Import de l'optimiseur principal
from internal_linking_optimizer import InternalLinkingOptimizer

# Configuration de la page
st.set_page_config(
    page_title="🔗 Optimiseur de Maillage Interne SEO",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2c3e50, #3498db);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3498db;
        margin: 0.5rem 0;
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

class WebSEOOptimizer:
    def __init__(self):
        self.optimizer = None
        self.analysis_running = False
        self.progress_queue = queue.Queue()
        
    def setup_session_state(self):
        """Initialise les variables de session Streamlit."""
        if 'api_key' not in st.session_state:
            st.session_state.api_key = ""
        if 'analysis_complete' not in st.session_state:
            st.session_state.analysis_complete = False
        if 'results' not in st.session_state:
            st.session_state.results = None
        if 'logs' not in st.session_state:
            st.session_state.logs = []
            
    def load_api_key(self):
        """Charge la clé API depuis le fichier .env."""
        try:
            if os.path.exists('.env'):
                with open('.env', 'r') as f:
                    for line in f:
                        if line.startswith('OPENAI_API_KEY='):
                            return line.split('=', 1)[1].strip()
        except:
            pass
        return ""
    
    def save_api_key(self, api_key):
        """Sauvegarde la clé API dans le fichier .env."""
        try:
            with open('.env', 'w') as f:
                f.write(f"OPENAI_API_KEY={api_key}\n")
            return True
        except:
            return False
    
    def log_message(self, message, level="INFO"):
        """Ajoute un message au log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        st.session_state.logs.append(log_entry)
        
        # Limiter le nombre de logs
        if len(st.session_state.logs) > 100:
            st.session_state.logs = st.session_state.logs[-100:]
    
    def run_analysis(self, sitemap_url, min_similarity, max_links, embedding_model, use_reduced_dimensions, embedding_dimensions):
        """Lance l'analyse en arrière-plan."""
        try:
            self.log_message("🚀 Démarrage de l'analyse...")
            
            # Initialiser l'optimiseur
            self.optimizer = InternalLinkingOptimizer(
                api_key=st.session_state.api_key,
                model=embedding_model
            )
            
            # Extraire les URLs du sitemap
            self.log_message(f"📋 Extraction des URLs depuis: {sitemap_url}")
            urls = self.optimizer.extract_urls_from_sitemap(sitemap_url)
            self.log_message(f"✅ {len(urls)} URLs trouvées dans le sitemap")
            
            if len(urls) == 0:
                self.log_message("❌ Aucune URL trouvée dans le sitemap", "ERROR")
                return False
            
            # Traiter les URLs
            dimensions = embedding_dimensions if use_reduced_dimensions else None
            self.log_message("🔍 Traitement des pages...")
            self.optimizer.process_urls(urls, dimensions=dimensions)
            
            # Calculer la similarité
            self.log_message("🧮 Calcul de la similarité sémantique...")
            self.optimizer.calculate_similarity_matrix()
            
            # Trouver les liens pertinents
            self.log_message("🔗 Recherche des liens pertinents...")
            recommendations = self.optimizer.find_relevant_links(
                min_similarity=min_similarity,
                max_links=max_links
            )
            
            # Sauvegarder les résultats
            self.log_message("💾 Sauvegarde des résultats...")
            self.optimizer.save_results(recommendations)
            
            # Stocker les résultats dans la session
            st.session_state.results = recommendations
            st.session_state.analysis_complete = True
            
            self.log_message("✅ Analyse terminée avec succès!")
            return True
            
        except Exception as e:
            self.log_message(f"❌ Erreur: {str(e)}", "ERROR")
            return False

def main():
    # Initialisation
    app = WebSEOOptimizer()
    app.setup_session_state()
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🔗 Optimiseur de Maillage Interne SEO</h1>
        <p>Optimisez votre maillage interne avec l'intelligence artificielle</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar pour la configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Clé API
        api_key = st.text_input(
            "Clé API OpenAI",
            value=st.session_state.api_key or app.load_api_key(),
            type="password",
            help="Votre clé API OpenAI (commence par sk-proj-)"
        )
        
        if api_key != st.session_state.api_key:
            st.session_state.api_key = api_key
            if app.save_api_key(api_key):
                st.success("Clé API sauvegardée")
        
        # URL du sitemap
        sitemap_url = st.text_input(
            "URL du sitemap",
            placeholder="https://votre-site.com/sitemap.xml",
            help="URL de votre sitemap XML"
        )
        
        # Paramètres d'analyse
        st.subheader("📊 Paramètres d'analyse")
        
        col1, col2 = st.columns(2)
        with col1:
            min_similarity = st.slider(
                "Score minimum",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Score de similarité minimum (0.0-1.0)"
            )
        
        with col2:
            max_links = st.number_input(
                "Liens par page",
                min_value=1,
                max_value=20,
                value=5,
                help="Nombre de liens à recommander par page"
            )
        
        # Configuration avancée
        with st.expander("🔧 Configuration avancée"):
            embedding_model = st.selectbox(
                "Modèle d'embeddings",
                ["text-embedding-3-small", "text-embedding-3-large"],
                help="Modèle OpenAI à utiliser"
            )
            
            use_reduced_dimensions = st.checkbox(
                "Réduire les dimensions",
                help="Réduire les dimensions pour économiser les coûts"
            )
            
            embedding_dimensions = st.selectbox(
                "Dimensions",
                [256, 512, 768, 1024, 1536],
                index=1,
                disabled=not use_reduced_dimensions
            )
    
    # Zone principale
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎯 Analyse de maillage interne")
        
        # Validation des paramètres
        if not st.session_state.api_key:
            st.error("⚠️ Veuillez configurer votre clé API OpenAI dans la sidebar")
            return
        
        if not sitemap_url:
            st.error("⚠️ Veuillez saisir l'URL de votre sitemap")
            return
        
        # Bouton de lancement
        if st.button("🚀 Lancer l'analyse", type="primary", disabled=app.analysis_running):
            app.analysis_running = True
            st.session_state.analysis_complete = False
            
            # Lancer l'analyse en arrière-plan
            with st.spinner("Analyse en cours..."):
                success = app.run_analysis(
                    sitemap_url=sitemap_url,
                    min_similarity=min_similarity,
                    max_links=max_links,
                    embedding_model=embedding_model,
                    use_reduced_dimensions=use_reduced_dimensions,
                    embedding_dimensions=embedding_dimensions
                )
            
            app.analysis_running = False
            
            if success:
                st.success("✅ Analyse terminée avec succès!")
                st.balloons()
            else:
                st.error("❌ Erreur lors de l'analyse")
        
        # Affichage des résultats
        if st.session_state.analysis_complete and st.session_state.results:
            st.subheader("📊 Résultats de l'analyse")
            
            # Statistiques
            total_pages = len(st.session_state.results)
            total_links = sum(len(data['recommended_links']) for data in st.session_state.results.values())
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Pages analysées", total_pages)
            with col2:
                st.metric("Liens recommandés", total_links)
            with col3:
                avg_links = total_links / total_pages if total_pages > 0 else 0
                st.metric("Liens/page", f"{avg_links:.1f}")
            
            # Tableau des résultats
            st.subheader("🔗 Recommandations de liens")
            
            # Préparer les données pour le tableau
            table_data = []
            for source_url, data in st.session_state.results.items():
                for link in data['recommended_links']:
                    table_data.append({
                        'Page source': data['source_title'] or 'Sans titre',
                        'URL source': source_url,
                        'Ancre suggérée': link['anchor_text'],
                        'URL cible': link['target_url'],
                        'Score (%)': f"{link['similarity_score'] * 100:.1f}%"
                    })
            
            if table_data:
                df = pd.DataFrame(table_data)
                st.dataframe(df, use_container_width=True)
                
                # Boutons d'export
                col1, col2 = st.columns(2)
                with col1:
                    csv = df.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="📥 Télécharger CSV",
                        data=csv,
                        file_name=f"maillage_interne_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    # Export Excel
                    try:
                        output = BytesIO()
                        with pd.ExcelWriter(output, engine='openpyxl') as writer:
                            df.to_excel(writer, sheet_name='Maillage_Interne', index=False)
                        excel_data = output.getvalue()
                        st.download_button(
                            label="📊 Télécharger Excel",
                            data=excel_data,
                            file_name=f"maillage_interne_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    except ImportError:
                        st.warning("Export Excel non disponible (openpyxl non installé)")
    
    with col2:
        st.header("📝 Logs")
        
        # Zone de logs
        log_text = "\n".join(st.session_state.logs[-20:])  # Afficher les 20 derniers logs
        st.text_area("Logs d'exécution", log_text, height=400, disabled=True)
        
        # Bouton pour rafraîchir
        if st.button("🔄 Rafraîchir"):
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8em;">
        🔗 Optimiseur de Maillage Interne SEO - Version Web<br>
        Propulsé par OpenAI et Streamlit
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 