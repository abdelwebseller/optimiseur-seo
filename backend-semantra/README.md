# Semantra API Backend

API backend pour l'optimisation SEO et le maillage interne automatique.

## 🚀 Fonctionnalités

- **Analyse de sitemaps** : Détection automatique et parsing de différents types de sitemaps
- **Crawling intelligent** : Gestion des blocages, rotation d'user agents, filtres avancés
- **Embeddings IA** : Génération d'embeddings avec OpenAI et Gemini
- **Suggestions de maillage** : Analyse de similarité et génération de suggestions
- **Optimisation d'ancres** : Réécriture automatique des ancres avec IA
- **Export multi-format** : CSV, JSON, Excel, Google Sheets
- **Traitement asynchrone** : Celery pour les tâches longues
- **API REST complète** : Documentation automatique avec FastAPI

## 🛠️ Technologies

- **FastAPI** : Framework web moderne et rapide
- **PostgreSQL** : Base de données relationnelle
- **Redis** : Cache et broker pour Celery
- **Celery** : Traitement asynchrone des tâches
- **OpenAI/Gemini** : APIs d'IA pour embeddings et optimisation
- **Docker** : Containerisation complète

## 📋 Prérequis

- Python 3.11+
- Docker et Docker Compose
- PostgreSQL
- Redis

## 🚀 Installation

### Option 1 : Docker (Recommandé)

1. **Cloner le projet**
```bash
git clone <repository-url>
cd backend-semantra
```

2. **Configurer l'environnement**
```bash
cp env.example .env
# Éditer .env avec vos configurations
```

3. **Lancer avec Docker Compose**
```bash
docker-compose up -d
```

### Option 2 : Installation locale

1. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurer la base de données**
```bash
# Créer la base PostgreSQL
createdb semantra

# Appliquer les migrations (à implémenter)
# alembic upgrade head
```

4. **Lancer l'API**
```bash
uvicorn app:app --reload
```

## 🔧 Configuration

### Variables d'environnement

Copiez `env.example` vers `.env` et configurez :

```env
# Base de données
DATABASE_URL=postgresql://user:password@localhost/semantra

# APIs externes
OPENAI_API_KEY=sk-your-key-here
GEMINI_API_KEY=your-gemini-key-here

# Sécurité
SECRET_KEY=your-secret-key-here

# Redis
REDIS_URL=redis://localhost:6379/0
```

## 📚 API Documentation

Une fois l'API lancée, accédez à :

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 🔌 Endpoints Principaux

### Analyses
- `POST /api/v1/analyze/` : Créer une nouvelle analyse
- `GET /api/v1/analyze/{analysis_id}` : Récupérer une analyse
- `GET /api/v1/analyze/{analysis_id}/status` : Statut en temps réel
- `GET /api/v1/analyze/{analysis_id}/results` : Résultats de l'analyse

### Suggestions
- `GET /api/v1/suggestions/` : Lister les suggestions
- `PUT /api/v1/suggestions/{suggestion_id}` : Mettre à jour une suggestion
- `POST /api/v1/suggestions/{suggestion_id}/optimize-anchor` : Optimiser une ancre

### Export
- `POST /api/v1/export/csv` : Exporter en CSV
- `POST /api/v1/export/json` : Exporter en JSON
- `POST /api/v1/export/excel` : Exporter en Excel
- `POST /api/v1/export/google-sheets` : Exporter vers Google Sheets

### Paramètres
- `GET /api/v1/settings/` : Récupérer les paramètres
- `PUT /api/v1/settings/` : Mettre à jour les paramètres

## 🏗️ Architecture

```
backend-semantra/
├── app/
│   ├── api/v1/endpoints/     # Endpoints API
│   ├── core/                 # Configuration et base de données
│   ├── models/               # Modèles SQLAlchemy
│   ├── schemas/              # Schémas Pydantic
│   ├── services/             # Logique métier
│   └── tasks/                # Tâches Celery
├── logs/                     # Fichiers de logs
├── requirements.txt          # Dépendances Python
├── Dockerfile               # Configuration Docker
├── docker-compose.yml       # Orchestration Docker
└── README.md               # Documentation
```

## 🔄 Workflow d'Analyse

1. **Création d'analyse** : L'utilisateur soumet une URL de sitemap
2. **Détection de sitemap** : Auto-détection du type (XML, TXT, HTML)
3. **Crawling** : Extraction des URLs avec filtres avancés
4. **Traitement des pages** : Crawling du contenu avec anti-blocage
5. **Génération d'embeddings** : Création d'embeddings avec IA
6. **Analyse de similarité** : Calcul des similarités entre pages
7. **Génération de suggestions** : Création des suggestions de maillage
8. **Optimisation d'ancres** : Réécriture automatique des ancres

## 🚀 Déploiement

### Vercel (Recommandé pour API simple)

1. **Configurer Vercel**
```bash
npm i -g vercel
vercel login
```

2. **Déployer**
```bash
vercel --prod
```

### Elestio + Hetzner (Recommandé pour traitement lourd)

1. **Préparer l'image Docker**
```bash
docker build -t semantra-api .
```

2. **Déployer sur Elestio**
- Créer un projet sur Elestio
- Connecter le repository GitHub
- Configurer les variables d'environnement
- Déployer automatiquement

## 🔍 Monitoring

### Logs
```bash
# Logs de l'API
docker-compose logs api

# Logs des workers Celery
docker-compose logs celery_worker

# Logs de la base de données
docker-compose logs postgres
```

### Santé de l'API
```bash
curl http://localhost:8000/health
```

## 🧪 Tests

```bash
# Lancer les tests
pytest

# Tests avec couverture
pytest --cov=app

# Tests d'intégration
pytest tests/integration/
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

Pour toute question ou problème :

1. Consulter la documentation API : http://localhost:8000/docs
2. Vérifier les logs : `docker-compose logs`
3. Ouvrir une issue sur GitHub

## 🔮 Roadmap

- [ ] Intégration de nouveaux modèles d'embedding
- [ ] Support de plus de formats d'export
- [ ] Interface d'administration
- [ ] Métriques avancées
- [ ] Intégration CMS (WordPress, etc.)
- [ ] API GraphQL
- [ ] Webhooks en temps réel 