#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version Web de l'Optimiseur de Maillage Interne SEO
Utilise Streamlit pour une interface web simple et efficace
"""

import streamlit as st
import pandas as pd
import queue
import threading
import time
from datetime import datetime
from io import BytesIO
from internal_linking_optimizer import InternalLinkingOptimizer

# Configuration de la page
st.set_page_config(
    page_title="Optimiseur SEO - Maillage Interne",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1f77b4, #ff7f0e);
    padding: 2rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.main-header h1 {
    margin: 0;
    font-size: 2.5rem;
    font-weight: bold;
}

.main-header p {
    margin: 0.5rem 0 0 0;
    font-size: 1.2rem;
    opacity: 0.9;
}

.stProgress > div > div > div > div {
    background-color: #1f77b4;
}

.metric-container {
    background: #f0f2f6;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #1f77b4;
}

.log-entry {
    padding: 0.5rem;
    margin: 0.25rem 0;
    border-radius: 4px;
    font-family: monospace;
    font-size: 0.9rem;
}

.log-success {
    background: #d4edda;
    border-left: 4px solid #28a745;
}

.log-error {
    background: #f8d7da;
    border-left: 4px solid #dc3545;
}

.log-warning {
    background: #fff3cd;
    border-left: 4px solid #ffc107;
}

.log-info {
    background: #d1ecf1;
    border-left: 4px solid #17a2b8;
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
        if 'progress' not in st.session_state:
            st.session_state.progress = 0
        if 'total_urls' not in st.session_state:
            st.session_state.total_urls = 0
        if 'current_step' not in st.session_state:
            st.session_state.current_step = ""
            
    def load_api_key(self):
        """Charge la clé API depuis le fichier .env."""
        try:
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
        icon = "ℹ️" if level == "INFO" else "⚠️" if level == "WARNING" else "❌" if level == "ERROR" else "✅"
        log_entry = f"[{timestamp}] {icon} {message}"
        st.session_state.logs.append(log_entry)
        
        # Limiter le nombre de logs
        if len(st.session_state.logs) > 100:
            st.session_state.logs = st.session_state.logs[-100:]
    
    def update_progress(self, current, total, step=""):
        """Met à jour la progression."""
        if total > 0:
            st.session_state.progress = int((current / total) * 100)
        st.session_state.current_step = step
    
    def diagnose_errors(self):
        """Diagnostique les erreurs courantes avec test d'authentification OpenAI."""
        errors = []
        
        # Vérifier la clé API
        if not st.session_state.api_key:
            errors.append("❌ Clé API OpenAI manquante")
        elif not st.session_state.api_key.startswith("sk-"):
            errors.append("❌ Format de clé API invalide")
        else:
            # Tester l'authentification OpenAI avec un petit embedding
            try:
                import openai
                client = openai.OpenAI(api_key=st.session_state.api_key)
                
                # Test simple avec un petit texte
                response = client.embeddings.create(
                    model="text-embedding-3-small",
                    input="test"
                )
                
                if response and response.data:
                    # Test réussi
                    pass
                else:
                    errors.append("⚠️ Problème de connexion à OpenAI")
                    
            except openai.AuthenticationError:
                errors.append("❌ Clé API OpenAI invalide ou expirée")
            except openai.RateLimitError:
                errors.append("⚠️ Rate limit OpenAI atteint - Attendez quelques minutes")
            except openai.APIError as e:
                errors.append(f"⚠️ Erreur API OpenAI: {str(e)}")
            except Exception as e:
                errors.append(f"⚠️ Problème de connexion à OpenAI: {str(e)}")
        
        # Vérifier la connexion internet
        try:
            import requests
            response = requests.get("https://api.openai.com", timeout=10)  # Timeout augmenté
            if response.status_code != 200:
                errors.append("⚠️ Problème de connexion réseau à OpenAI")
        except:
            errors.append("❌ Pas de connexion internet")
        
        # Vérifier les ressources système
        try:
            import psutil
            memory = psutil.virtual_memory()
            if memory.percent > 90:
                errors.append("⚠️ Mémoire système faible")
        except:
            pass
        
        return errors
    
    def run_analysis(self, sitemap_url, min_similarity, max_links, embedding_model, use_reduced_dimensions, 
                    embedding_dimensions, max_concurrent_requests, max_concurrent_embeddings, 
                    batch_size, processing_mode):
        """Lance l'analyse en arrière-plan."""
        try:
            # Réinitialiser la progression
            st.session_state.progress = 0
            st.session_state.total_urls = 0
            st.session_state.current_step = ""
            
            self.log_message("🚀 Démarrage de l'analyse...")
            self.update_progress(0, 100, "Initialisation...")
            
            # Configurer les paramètres selon le mode
            if processing_mode == "Rapide":
                max_concurrent_requests = min(20, max_concurrent_requests + 5)
                max_concurrent_embeddings = min(8, max_concurrent_embeddings + 2)  # Limité à 8 pour éviter les rate limits
                batch_size = min(100, batch_size + 25)
            elif processing_mode == "Prudent":
                max_concurrent_requests = max(5, max_concurrent_requests - 5)
                max_concurrent_embeddings = max(2, max_concurrent_embeddings - 2)  # Minimum 2
                batch_size = max(25, batch_size - 25)
            
            # Initialiser l'optimiseur avec les paramètres de parallélisation
            self.optimizer = InternalLinkingOptimizer(
                api_key=st.session_state.api_key,
                model=embedding_model,
                max_concurrent_requests=max_concurrent_requests,
                max_concurrent_embeddings=max_concurrent_embeddings,
                batch_size=batch_size
            )
            
            # Tester la connexion OpenAI avant de commencer
            self.log_message("🔍 Test de connexion OpenAI...")
            if not self.optimizer.test_openai_connection():
                self.log_message("❌ Impossible de se connecter à OpenAI. Vérifiez votre clé API.", "ERROR")
                return False
            
            # Extraire les URLs du sitemap
            self.log_message(f"📋 Extraction des URLs depuis: {sitemap_url}")
            self.update_progress(5, 100, "Extraction des URLs...")
            
            try:
                urls = self.optimizer.extract_urls_from_sitemap(sitemap_url)
                self.log_message(f"✅ {len(urls)} URLs trouvées dans le sitemap")
            except Exception as e:
                self.log_message(f"❌ Erreur lors de l'extraction du sitemap: {str(e)}", "ERROR")
                return False
            
            if len(urls) == 0:
                self.log_message("❌ Aucune URL trouvée dans le sitemap", "ERROR")
                return False
            
            # Ajuster les paramètres selon le volume d'URLs pour le mode Auto
            if processing_mode == "Auto":
                if len(urls) > 500:
                    max_concurrent_embeddings = min(5, max_concurrent_embeddings)  # Limiter pour les gros volumes
                    batch_size = min(50, batch_size)
                elif len(urls) > 200:
                    max_concurrent_embeddings = min(6, max_concurrent_embeddings)
                    batch_size = min(75, batch_size)
                else:
                    max_concurrent_embeddings = min(7, max_concurrent_embeddings)
                
                # Mettre à jour l'optimiseur avec les nouveaux paramètres
                self.optimizer.max_concurrent_embeddings = max_concurrent_embeddings
                self.optimizer.batch_size = batch_size
            
            # Afficher les informations de performance
            time_estimate = self.optimizer.estimate_processing_time(len(urls))
            memory_info = self.optimizer.check_memory_usage()
            
            # Stocker les informations de performance
            st.session_state.performance_info = {
                'estimated_time': time_estimate['formatted'],
                'memory_available': memory_info.get('available_mb', 'N/A'),
                'concurrent_requests': max_concurrent_requests,
                'concurrent_embeddings': max_concurrent_embeddings,
                'batch_size': batch_size,
                'processing_mode': processing_mode
            }
            
            self.log_message(f"⏱️ Temps estimé: {time_estimate['formatted']}")
            self.log_message(f"💾 Mémoire disponible: {memory_info.get('available_mb', 'N/A')} MB")
            
            # Avertissement pour les gros volumes
            if len(urls) > 500:
                self.log_message(f"⚠️ Gros volume détecté ({len(urls)} URLs). Le traitement peut prendre du temps.", "WARNING")
            elif len(urls) > 1000:
                self.log_message(f"⚠️ Très gros volume ({len(urls)} URLs). Considérez traiter par sections.", "WARNING")
            
            # Stocker le nombre total d'URLs
            st.session_state.total_urls = len(urls)
            
            # Traiter les URLs
            dimensions = embedding_dimensions if use_reduced_dimensions else None
            self.log_message("🔍 Traitement des pages...")
            self.update_progress(10, 100, f"Traitement des pages (0/{len(urls)})")
            
            try:
                # Utiliser la nouvelle méthode optimisée
                df = self.optimizer.process_urls_with_progress(urls, dimensions=dimensions, progress_callback=self.update_progress)
                
                if df.empty:
                    self.log_message("❌ Aucune page n'a pu être traitée", "ERROR")
                    return False
                    
            except Exception as e:
                self.log_message(f"❌ Erreur lors du traitement des pages: {str(e)}", "ERROR")
                return False
            
            # Calculer la similarité
            self.log_message("🧮 Calcul de la similarité sémantique...")
            self.update_progress(80, 100, "Calcul de la similarité...")
            
            try:
                self.optimizer.calculate_similarity_matrix()
            except Exception as e:
                self.log_message(f"❌ Erreur lors du calcul de similarité: {str(e)}", "ERROR")
                return False
            
            # Trouver les liens pertinents
            self.log_message("🔗 Recherche des liens pertinents...")
            self.update_progress(90, 100, "Recherche des liens...")
            
            try:
                recommendations = self.optimizer.find_relevant_links(
                    min_similarity=min_similarity,
                    max_links=max_links
                )
            except Exception as e:
                self.log_message(f"❌ Erreur lors de la recherche de liens: {str(e)}", "ERROR")
                return False
            
            # Sauvegarder les résultats
            self.log_message("💾 Sauvegarde des résultats...")
            self.update_progress(95, 100, "Sauvegarde...")
            
            try:
                self.optimizer.save_results(recommendations)
            except Exception as e:
                self.log_message(f"⚠️ Erreur lors de la sauvegarde: {str(e)}", "WARNING")
                # Ne pas échouer complètement si la sauvegarde échoue
            
            # Stocker les résultats dans la session
            st.session_state.results = recommendations
            st.session_state.analysis_complete = True
            
            self.log_message("✅ Analyse terminée avec succès!")
            self.update_progress(100, 100, "Terminé!")
            return True
            
        except Exception as e:
            self.log_message(f"❌ Erreur générale: {str(e)}", "ERROR")
            return False

def main():
    # Initialisation
    app = WebSEOOptimizer()
    app.setup_session_state()
    
    # Sidebar avec menu de navigation
    with st.sidebar:
        # Logo et titre
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h2>🔗 SEO Optimizer</h2>
            <p style="font-size: 14px; color: #666;">Maillage Interne IA</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Menu de navigation
        st.markdown("### 📋 Navigation")
        
        # Onglets de navigation
        selected_page = st.selectbox(
            "Menu",
            ["🏠 Accueil", "📊 Mes Projets", "✅ Réalisé", "🔄 En Cours", "⚙️ Configuration", "👤 Mon Compte", "📈 Statistiques", "❓ Aide"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Configuration (toujours visible)
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
        st.header("📊 Paramètres d'analyse")
        
        min_similarity = st.slider(
            "Score minimum",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.1,
            help="Score de similarité minimum pour recommander un lien"
        )
        
        max_links = st.number_input(
            "Liens par page",
            min_value=1,
            max_value=10,
            value=5,
            help="Nombre maximum de liens à recommander par page"
        )
        
        # Configuration avancée
        with st.expander("⚙️ Configuration avancée"):
            col1, col2 = st.columns(2)
            
            with col1:
                embedding_model = st.selectbox(
                    "Modèle d'embedding",
                    ["text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"],
                    index=0,
                    help="Modèle OpenAI pour générer les embeddings"
                )
                
                use_reduced_dimensions = st.checkbox(
                    "Utiliser des dimensions réduites",
                    value=False,
                    help="Réduire la taille des embeddings pour économiser les tokens"
                )
                
                if use_reduced_dimensions:
                    embedding_dimensions = st.slider(
                        "Dimensions d'embedding",
                        min_value=256,
                        max_value=1536,
                        value=512,
                        step=256,
                        help="Nombre de dimensions pour les embeddings (plus = plus précis mais plus cher)"
                    )
                else:
                    embedding_dimensions = None
                
            with col2:
                # Nouveaux paramètres de parallélisation
                max_concurrent_requests = st.slider(
                    "Requêtes HTTP simultanées",
                    min_value=5,
                    max_value=20,
                    value=10,
                    help="Nombre de requêtes HTTP simultanées (plus = plus rapide mais risque de surcharge)"
                )
                
                max_concurrent_embeddings = st.slider(
                    "Embeddings simultanés",
                    min_value=3,
                    max_value=10,
                    value=5,
                    help="Nombre d'embeddings OpenAI simultanés (attention aux rate limits)"
                )
                
                batch_size = st.slider(
                    "Taille des batches",
                    min_value=25,
                    max_value=100,
                    value=50,
                    help="Nombre d'URLs traitées par batch (plus = plus efficace mais plus de mémoire)"
                )
                
                # Mode de traitement
                processing_mode = st.selectbox(
                    "Mode de traitement",
                    ["Auto", "Rapide", "Standard", "Prudent"],
                    index=0,
                    help="Auto: détection automatique, Rapide: parallélisation maximale, Standard: équilibré, Prudent: séquentiel"
                )
    
    # Contenu principal selon la page sélectionnée
    if selected_page == "🏠 Accueil":
        # Header principal
        st.markdown("""
        <div class="main-header">
            <h1>🔗 Optimiseur de Maillage Interne SEO</h1>
            <p>Optimisez votre maillage interne avec l'intelligence artificielle</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Barre de progression
        if st.session_state.progress > 0:
            st.subheader("📊 Progression")
            progress_col1, progress_col2 = st.columns([3, 1])
            
            with progress_col1:
                st.progress(st.session_state.progress / 100)
            
            with progress_col2:
                st.metric("Progression", f"{st.session_state.progress}%")
            
            if st.session_state.current_step:
                st.info(f"🔄 {st.session_state.current_step}")
        
        # Section d'analyse
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
            
            # Bouton de diagnostic
            if st.button("🔍 Diagnostiquer les problèmes", type="secondary"):
                errors = app.diagnose_errors()
                if errors:
                    st.error("Problèmes détectés:")
                    for error in errors:
                        st.write(f"• {error}")
                else:
                    st.success("✅ Aucun problème détecté")
            
            # Bouton de lancement
            if st.button("🚀 Lancer l'analyse", type="primary", disabled=app.analysis_running):
                app.analysis_running = True
                st.session_state.analysis_complete = False
                
                # Lancer l'analyse
                success = app.run_analysis(
                    sitemap_url=sitemap_url,
                    min_similarity=min_similarity,
                    max_links=max_links,
                    embedding_model=embedding_model,
                    use_reduced_dimensions=use_reduced_dimensions,
                    embedding_dimensions=embedding_dimensions,
                    max_concurrent_requests=max_concurrent_requests,
                    max_concurrent_embeddings=max_concurrent_embeddings,
                    batch_size=batch_size,
                    processing_mode=processing_mode
                )
                
                app.analysis_running = False
                
                if success:
                    st.success("✅ Analyse terminée avec succès!")
                    st.balloons()
                else:
                    st.error("❌ Erreur lors de l'analyse")
                    st.info("💡 Conseil: Utilisez le bouton 'Diagnostiquer les problèmes' pour identifier la cause")
            
            # Affichage des résultats
            if st.session_state.analysis_complete and st.session_state.results:
                st.subheader("📊 Résultats de l'analyse")
                
                # Métriques de performance
                if st.session_state.get('analysis_complete', False):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(
                            label="Pages analysées",
                            value=len(st.session_state.results) if st.session_state.results else 0,
                            help="Nombre total de pages traitées avec succès"
                        )
                    
                    with col2:
                        total_links = sum(len(data['recommended_links']) for data in st.session_state.results.values()) if st.session_state.results else 0
                        st.metric(
                            label="Liens recommandés",
                            value=total_links,
                            help="Nombre total de liens internes recommandés"
                        )
                    
                    with col3:
                        avg_links = total_links / len(st.session_state.results) if st.session_state.results else 0
                        st.metric(
                            label="Liens/page",
                            value=f"{avg_links:.1f}",
                            help="Nombre moyen de liens recommandés par page"
                        )
                    
                    with col4:
                        # Afficher le mode de traitement utilisé
                        mode_used = st.session_state.get('processing_mode', 'Standard')
                        st.metric(
                            label="Mode utilisé",
                            value=mode_used,
                            help="Mode de traitement utilisé pour l'analyse"
                        )
                    
                    # Informations supplémentaires sur les performances
                    if st.session_state.get('performance_info'):
                        with st.expander("📊 Informations de performance"):
                            perf_info = st.session_state.performance_info
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**Temps estimé initial:** {perf_info.get('estimated_time', 'N/A')}")
                                st.write(f"**Mémoire disponible:** {perf_info.get('memory_available', 'N/A')} MB")
                            
                            with col2:
                                st.write(f"**Requêtes simultanées:** {perf_info.get('concurrent_requests', 'N/A')}")
                                st.write(f"**Embeddings simultanés:** {perf_info.get('concurrent_embeddings', 'N/A')}")
                
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
            st.header("📝 Logs d'exécution")
            
            # Affichage des logs avec style amélioré
            if st.session_state.logs:
                # Créer un conteneur pour les logs avec style
                log_container = st.container()
                with log_container:
                    for log_entry in st.session_state.logs[-20:]:  # Afficher les 20 derniers logs
                        # Détecter le type de log par l'icône
                        if "✅" in log_entry:
                            st.success(log_entry)
                        elif "❌" in log_entry:
                            st.error(log_entry)
                        elif "⚠️" in log_entry:
                            st.warning(log_entry)
                        else:
                            st.info(log_entry)
            else:
                st.info("📋 Aucun log disponible - Lancez une analyse pour voir les logs")
            
            # Bouton de rafraîchissement
            if st.button("🔄 Rafraîchir les logs"):
                st.rerun()
    
    elif selected_page == "📊 Mes Projets":
        st.header("📊 Mes Projets")
        st.info("🚧 Cette fonctionnalité sera disponible prochainement")
        st.markdown("""
        - **Projets en cours** : 0
        - **Projets terminés** : 0
        - **Projets archivés** : 0
        """)
    
    elif selected_page == "✅ Réalisé":
        st.header("✅ Projets Réalisés")
        st.info("🚧 Cette fonctionnalité sera disponible prochainement")
        st.markdown("Aucun projet réalisé pour le moment")
    
    elif selected_page == "🔄 En Cours":
        st.header("🔄 Projets En Cours")
        st.info("🚧 Cette fonctionnalité sera disponible prochainement")
        st.markdown("Aucun projet en cours pour le moment")
    
    elif selected_page == "⚙️ Configuration":
        st.header("⚙️ Configuration Avancée")
        st.info("🚧 Cette fonctionnalité sera disponible prochainement")
        st.markdown("""
        - **Paramètres utilisateur**
        - **Préférences d'export**
        - **Configuration des modèles**
        - **Gestion des API keys**
        """)
    
    elif selected_page == "👤 Mon Compte":
        st.header("👤 Mon Compte")
        st.info("🚧 Cette fonctionnalité sera disponible prochainement")
        st.markdown("""
        - **Profil utilisateur**
        - **Historique des analyses**
        - **Statistiques d'usage**
        - **Paramètres de compte**
        """)
    
    elif selected_page == "📈 Statistiques":
        st.header("📈 Statistiques")
        st.info("🚧 Cette fonctionnalité sera disponible prochainement")
        st.markdown("""
        - **Analyses effectuées** : 0
        - **Pages traitées** : 0
        - **Liens générés** : 0
        - **Temps d'utilisation** : 0h
        """)
    
    elif selected_page == "❓ Aide":
        st.header("❓ Centre d'Aide")
        st.markdown("""
        ### 📖 Guide d'utilisation
        
        **1. Configuration**
        - Ajoutez votre clé API OpenAI dans la sidebar
        - Saisissez l'URL de votre sitemap XML
        
        **2. Paramètres d'analyse**
        - **Score minimum** : Seuil de similarité (0.0 à 1.0)
        - **Liens par page** : Nombre de recommandations par page
        
        **3. Lancement**
        - Cliquez sur "Lancer l'analyse"
        - Suivez la progression en temps réel
        - Téléchargez les résultats en CSV/Excel
        
        ### 🔧 Dépannage
        
        **Erreur de clé API** : Vérifiez que votre clé OpenAI est valide
        **Erreur de sitemap** : Vérifiez que l'URL du sitemap est accessible
        **Analyse lente** : Le traitement dépend du nombre de pages
        """)
    
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