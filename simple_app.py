#!/usr/bin/env python3
"""
Application Streamlit ultra-simplifiée pour test de déploiement
"""

import streamlit as st
import os
import time

# Configuration de base
st.set_page_config(
    page_title="SEO Optimizer - Test",
    page_icon="🔗",
    layout="wide"
)

# Header
st.title("🔗 Optimiseur SEO - Version Test")
st.markdown("---")

# Informations système
st.header("📊 État du système")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Variables d'environnement")
    st.write(f"**Port:** {os.getenv('STREAMLIT_SERVER_PORT', 'Non défini')}")
    st.write(f"**Adresse:** {os.getenv('STREAMLIT_SERVER_ADDRESS', 'Non défini')}")
    st.write(f"**OpenAI Key:** {'✅ Définie' if os.getenv('OPENAI_API_KEY') else '❌ Manquante'}")

with col2:
    st.subheader("Fichiers critiques")
    critical_files = [
        "app.py",
        "internal_linking_optimizer.py",
        "config.yaml",
        "requirements_web.txt"
    ]
    
    for file in critical_files:
        if os.path.exists(file):
            st.write(f"✅ {file}")
        else:
            st.write(f"❌ {file}")

# Test de fonctionnalité
st.header("🧪 Tests de fonctionnalité")

# Test 1: Bouton
if st.button("Test de bouton"):
    st.success("✅ Bouton fonctionnel !")

# Test 2: Saisie
user_input = st.text_input("Test de saisie", placeholder="Tapez quelque chose...")
if user_input:
    st.write(f"📝 Saisie reçue : {user_input}")

# Test 3: Sélecteur
option = st.selectbox("Test de sélecteur", ["Option A", "Option B", "Option C"])
st.write(f"🎯 Option sélectionnée : {option}")

# Test 4: Upload (simulation)
uploaded_file = st.file_uploader("Test d'upload", type=['txt', 'csv'])
if uploaded_file:
    st.write(f"📁 Fichier uploadé : {uploaded_file.name}")

# Test 5: Métriques
st.header("📈 Métriques système")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Status", "🟢 En ligne")
    
with col2:
    st.metric("Temps de réponse", "0.2s")
    
with col3:
    st.metric("Version", "1.0.0")

# Footer
st.markdown("---")
st.markdown("**🎉 Si vous voyez cette page, l'application fonctionne correctement !**")

# Debug info
with st.expander("🔧 Informations de débogage"):
    st.write("**Timestamp:**", time.strftime("%Y-%m-%d %H:%M:%S"))
    st.write("**Working Directory:**", os.getcwd())
    st.write("**Python Version:**", os.sys.version)
    st.write("**Streamlit Version:**", st.__version__) 