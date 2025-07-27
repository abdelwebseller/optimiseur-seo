# Utiliser une image Python officielle optimisée
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système minimales
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copier les fichiers de requirements
COPY requirements_web.txt .

# Installer les dépendances Python avec cache optimisé
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements_web.txt

# Copier le code de l'application
COPY . .

# Créer les dossiers nécessaires
RUN mkdir -p logs output

# Exposer le port Streamlit
EXPOSE 8501

# Variables d'environnement pour Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=true
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Health check simplifié - désactivé temporairement pour éviter les erreurs 502
# HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
#     CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Commande de démarrage simplifiée
CMD ["streamlit", "run", "app.py"] 