#!/bin/bash
# Script de déploiement simple pour Elest.io
# Alternative au CI/CD GitHub

echo "🚀 Déploiement simple sur Elest.io"

# 1. Build de l'image Docker
echo "📦 Construction de l'image Docker..."
docker build -t optimiseur-seo .

# 2. Test local
echo "🧪 Test local de l'application..."
docker run -d --name test-optimiseur -p 8501:8501 \
  -e OPENAI_API_KEY="$OPENAI_API_KEY" \
  -e STREAMLIT_SERVER_PORT=8501 \
  -e STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
  optimiseur-seo

# 3. Attendre le démarrage
echo "⏳ Attente du démarrage..."
sleep 10

# 4. Test de santé
echo "🏥 Test de santé..."
curl -f http://localhost:8501/_stcore/health && echo "✅ Application fonctionnelle" || echo "❌ Problème de santé"

# 5. Nettoyage
echo "🧹 Nettoyage..."
docker stop test-optimiseur
docker rm test-optimiseur

echo "✅ Prêt pour le déploiement sur Elest.io"
echo "📋 Instructions :"
echo "1. Uploadez cette image sur Elest.io"
echo "2. Configurez les variables d'environnement"
echo "3. Démarrez le service" 