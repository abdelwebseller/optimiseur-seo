# 🔗 Optimiseur de Maillage Interne SEO - Version Web

Application web Streamlit pour optimiser le maillage interne de sites web en utilisant l'intelligence artificielle OpenAI.

## 🚀 Déploiement Rapide

### **Déploiement sur Elest.io (Recommandé)**
1. Connecter ce repository à Elest.io
2. Configurer les variables d'environnement
3. Déploiement automatique en 5 minutes

### **Variables d'environnement requises**
```bash
OPENAI_API_KEY=sk-proj-votre-cle-openai-ici
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## 📁 Structure du projet

```
optimiseur-seo/
├── app.py                          # Application Streamlit
├── internal_linking_optimizer.py   # Logique métier
├── config.yaml                     # Configuration
├── requirements_web.txt            # Dépendances Python
├── Dockerfile                      # Configuration Docker
├── .dockerignore                   # Optimisation Docker
├── .gitignore                      # Exclusion Git
├── .streamlit/config.toml          # Configuration Streamlit
└── README.md                       # Ce fichier
```

## 🔧 Fonctionnalités

- ✅ Analyse sémantique avec OpenAI embeddings
- ✅ Import depuis sitemap XML
- ✅ Génération d'ancres optimisées
- ✅ Export CSV/Excel
- ✅ Interface web responsive
- ✅ Logs en temps réel

## 🌐 Accès

Une fois déployé, l'application sera accessible sur :
```
https://votre-app.elest.io
```

## 📞 Support

- Documentation : `GUIDE_DEPLOIEMENT_RAPIDE.md`
- Support Elest.io : Dashboard intégré
- Logs : Disponibles en temps réel

---

**Note** : Cette version est optimisée pour le déploiement cloud sur Elest.io. 