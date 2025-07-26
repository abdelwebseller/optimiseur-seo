# 🌐 Version Web - Optimiseur de Maillage Interne SEO

Cette version web utilise **Streamlit** pour transformer votre outil en application web accessible depuis n'importe quel navigateur.

## 🚀 Déploiement Rapide

### Option 1 : Déploiement Local (Développement)

```bash
# 1. Installer les dépendances web
pip install -r requirements_web.txt

# 2. Lancer l'application
streamlit run app.py

# 3. Ouvrir http://localhost:8501
```

### Option 2 : Docker (Production)

```bash
# 1. Construire l'image
docker build -t seo-optimizer .

# 2. Lancer avec Docker Compose
docker-compose up -d

# 3. Ouvrir http://localhost:8501
```

### Option 3 : Déploiement Cloud

#### Heroku
```bash
# 1. Créer un compte Heroku
# 2. Installer Heroku CLI
# 3. Déployer
heroku create votre-app-seo
git push heroku main
```

#### Railway
```bash
# 1. Connecter votre repo GitHub
# 2. Railway détecte automatiquement le Dockerfile
# 3. Déploiement automatique
```

#### Render
```bash
# 1. Connecter votre repo GitHub
# 2. Sélectionner "Web Service"
# 3. Build Command: docker build -t seo-optimizer .
# 4. Start Command: docker run -p 8501:8501 seo-optimizer
```

## 🔧 Configuration

### Variables d'environnement
```bash
# Créer un fichier .env
OPENAI_API_KEY=sk-proj-votre-cle-ici
```

### Configuration Streamlit
Le fichier `.streamlit/config.toml` contient :
- Port : 8501
- Thème personnalisé
- Sécurité activée

## 📊 Fonctionnalités Web

### Interface Utilisateur
- ✅ Interface responsive (mobile/desktop)
- ✅ Sidebar de configuration
- ✅ Logs en temps réel
- ✅ Export CSV/Excel direct
- ✅ Thème moderne

### Sécurité
- ✅ Protection XSRF
- ✅ Variables d'environnement
- ✅ Validation des entrées
- ✅ Logs sécurisés

### Performance
- ✅ Cache des embeddings
- ✅ Traitement asynchrone
- ✅ Optimisation mémoire
- ✅ Health checks

## 🌍 Déploiement Production

### Recommandations
1. **HTTPS obligatoire** : Certificat SSL
2. **Authentification** : Système de login
3. **Rate limiting** : Limiter les requêtes
4. **Monitoring** : Logs et métriques
5. **Backup** : Sauvegarde des données

### Exemple Nginx
```nginx
server {
    listen 80;
    server_name votre-domaine.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name votre-domaine.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 Sécurité Avancée

### Authentification (Optionnel)
```python
# Ajouter dans app.py
import streamlit_authenticator as stauth

# Configuration des utilisateurs
names = ['Admin', 'User1', 'User2']
usernames = ['admin', 'user1', 'user2']
passwords = ['admin123', 'user123', 'user456']

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords,
    'seo_optimizer', 'auth_key', cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login('Login', 'main')
```

### Rate Limiting
```python
# Ajouter dans app.py
from streamlit.runtime.scriptrunner import get_script_run_ctx
import time

def rate_limit():
    ctx = get_script_run_ctx()
    if ctx is None:
        return
    
    # Limiter à 10 requêtes par minute par session
    session_id = ctx.session_id
    current_time = time.time()
    
    if 'last_request' not in st.session_state:
        st.session_state.last_request = {}
    
    if session_id in st.session_state.last_request:
        if current_time - st.session_state.last_request[session_id] < 6:  # 6 secondes
            st.error("Trop de requêtes. Attendez quelques secondes.")
            st.stop()
    
    st.session_state.last_request[session_id] = current_time
```

## 📈 Monitoring

### Logs
```python
# Ajouter dans app.py
import logging
from datetime import datetime

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/web_app_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
```

### Métriques
```python
# Ajouter dans app.py
import psutil

# Afficher les métriques système
with st.sidebar:
    st.subheader("📊 Métriques système")
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    
    st.metric("CPU", f"{cpu_percent}%")
    st.metric("RAM", f"{memory.percent}%")
```

## 🚀 Optimisations

### Cache Redis (Optionnel)
```python
# Ajouter dans app.py
import redis
import pickle

# Configuration Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@st.cache_data(ttl=3600)  # Cache 1 heure
def get_cached_embeddings(url):
    cache_key = f"embedding:{hash(url)}"
    cached = redis_client.get(cache_key)
    if cached:
        return pickle.loads(cached)
    return None
```

### Base de données (Optionnel)
```python
# Ajouter dans app.py
import sqlite3

def save_analysis_results(results, user_id):
    conn = sqlite3.connect('seo_analyses.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO analyses (user_id, results, created_at)
        VALUES (?, ?, ?)
    ''', (user_id, json.dumps(results), datetime.now()))
    
    conn.commit()
    conn.close()
```

## 📞 Support

Pour toute question ou problème :
1. Vérifier les logs dans `/logs`
2. Tester en local d'abord
3. Vérifier les variables d'environnement
4. Consulter la documentation Streamlit

---

**Note** : Cette version web conserve toutes les fonctionnalités de l'application desktop tout en ajoutant l'accessibilité web et la facilité de déploiement. 