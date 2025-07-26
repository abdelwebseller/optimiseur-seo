#!/usr/bin/env python3
"""
Application de test simple pour diagnostiquer le déploiement Elest.io
"""

import streamlit as st
import os

# Configuration de la page
st.set_page_config(
    page_title="Test App",
    page_icon="🧪",
    layout="wide"
)

# Header
st.title("🧪 Application de Test - Elest.io")
st.markdown("---")

# Informations système
st.header("📊 Informations système")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Variables d'environnement")
    st.write(f"**STREAMLIT_SERVER_PORT:** {os.getenv('STREAMLIT_SERVER_PORT', 'Non défini')}")
    st.write(f"**STREAMLIT_SERVER_ADDRESS:** {os.getenv('STREAMLIT_SERVER_ADDRESS', 'Non défini')}")
    st.write(f"**OPENAI_API_KEY:** {'Défini' if os.getenv('OPENAI_API_KEY') else 'Non défini'}")

with col2:
    st.subheader("Fichiers présents")
    files = [
        "app.py",
        "internal_linking_optimizer.py", 
        "config.yaml",
        "requirements_web.txt",
        "Dockerfile",
        ".streamlit/config.toml"
    ]
    
    for file in files:
        if os.path.exists(file):
            st.write(f"✅ {file}")
        else:
            st.write(f"❌ {file}")

# Test de fonctionnalité
st.header("🔧 Test de fonctionnalité")

if st.button("Test de bouton"):
    st.success("✅ Le bouton fonctionne !")

# Test de saisie
user_input = st.text_input("Test de saisie", placeholder="Tapez quelque chose...")
if user_input:
    st.write(f"Vous avez saisi : {user_input}")

# Test de sélecteur
option = st.selectbox("Test de sélecteur", ["Option 1", "Option 2", "Option 3"])
st.write(f"Option sélectionnée : {option}")

# Footer
st.markdown("---")
st.markdown("**Si vous voyez cette page, l'application Streamlit fonctionne correctement !** 🎉") 