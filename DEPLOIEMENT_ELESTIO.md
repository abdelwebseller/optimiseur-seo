# 🚀 Déploiement sur Elest.io + Hetzner

Guide complet pour déployer votre optimiseur SEO sur Elest.io avec un serveur Hetzner.

## 📋 Prérequis

### **Comptes requis**
- ✅ [Compte Elest.io](https://elest.io/) (gratuit pour commencer)
- ✅ [Compte Hetzner Cloud](https://console.hetzner.cloud/) (payant)
- ✅ [Compte GitHub](https://github.com/) (gratuit)
- ✅ [Compte OpenAI](https://platform.openai.com/) (payant)

### **Clés API nécessaires**
- 🔑 **Hetzner API Token** : Pour connecter Elest.io à Hetzner
- 🔑 **OpenAI API Key** : Pour les embeddings IA

## 🔧 Configuration Hetzner

### **1. Créer un projet Hetzner**
```bash
# 1. Aller sur https://console.hetzner.cloud/
# 2. Créer un nouveau projet
# 3. Nommer le projet : "SEO Optimizer"
```

### **2. Obtenir la clé API Hetzner**
```bash
# 1. Dans le dashboard Hetzner
# 2. Aller dans "Security" > "API Tokens"
# 3. Cliquer "Generate API Token"
# 4. Permissions requises :
#    - Read & Write (Cloud Servers)
#    - Read & Write (Networks)
#    - Read & Write (SSH Keys)
# 5. Copier et sauvegarder le token
```

## 🌐 Configuration Elest.io

### **1. Créer un compte Elest.io**
```bash
# 1. Aller sur https://elest.io/
# 2. Cliquer "Get Started"
# 3. Créer un compte avec votre email
# 4. Vérifier votre email
```

### **2. Connecter Hetzner à Elest.io**
```bash
# 1. Dans Elest.io dashboard
# 2. Aller dans "Cloud Providers"
# 3. Cliquer "Add Cloud Provider"
# 4. Sélectionner "Hetzner"
# 5. Coller votre clé API Hetzner
# 6. Tester la connexion
```

### **3. Créer un nouveau projet**
```bash
# 1. Dans Elest.io dashboard
# 2. Cliquer "New Project"
# 3. Nom : "seo-optimizer"
# 4. Description : "Optimiseur de maillage interne SEO"
# 5. Cloud Provider : Hetzner
# 6. Région : Francfort (FSN1) ou Nuremberg (NBG1)
```

## 📦 Préparation du code

### **1. Créer un repository GitHub**
```bash
# 1. Aller sur https://github.com/
# 2. Créer un nouveau repository
# 3. Nom : "seo-optimizer"
# 4. Public ou Private (votre choix)
```

### **2. Pousser votre code**
```bash
# Dans votre dossier optimiseur-seo
git init
git add .
git commit -m "Initial commit - SEO Optimizer for Elest.io"
git branch -M main
git remote add origin https://github.com/votre-username/seo-optimizer.git
git push -u origin main
```

## 🔄 Configuration CI/CD

### **1. Connecter GitHub à Elest.io**
```bash
# 1. Dans votre projet Elest.io
# 2. Aller dans "CI/CD" > "Connect Repository"
# 3. Sélectionner votre repo GitHub
# 4. Autoriser l'accès
```

### **2. Configurer le pipeline**
```bash
# 1. Créer un nouveau pipeline
# 2. Source : Votre repo GitHub
# 3. Branch : main
# 4. Build Command : docker build -t seo-optimizer .
# 5. Start Command : docker run -p 8501:8501 seo-optimizer
# 6. Port : 8501
```

### **3. Variables d'environnement**
```bash
# Dans Elest.io > Votre projet > Environment Variables
OPENAI_API_KEY=sk-proj-votre-cle-openai-ici
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true
```

## 🚀 Déploiement

### **Option A : Déploiement automatique**
```bash
# 1. Configurer le webhook GitHub
# 2. Chaque push sur main déclenche un déploiement
# 3. Elest.io gère automatiquement :
#    - Build de l'image Docker
#    - Déploiement sur Hetzner
#    - Configuration SSL
#    - Monitoring
```

### **Option B : Déploiement manuel**
```bash
# 1. Dans Elest.io dashboard
# 2. Aller dans "CI/CD" > "Deployments"
# 3. Cliquer "Deploy Now"
# 4. Attendre la fin du build (2-5 minutes)
```

## 🌍 Configuration du domaine

### **1. Domaine Elest.io (Gratuit)**
```bash
# 1. Dans votre service Elest.io
# 2. Aller dans "Domains"
# 3. Utiliser l'URL fournie : https://votre-app.elest.io
# 4. SSL automatique inclus
```

### **2. Domaine personnalisé (Optionnel)**
```bash
# 1. Acheter un domaine (OVH, Namecheap, etc.)
# 2. Dans Elest.io > Domains > "Add Custom Domain"
# 3. Configurer les DNS :
#    Type: CNAME
#    Name: @
#    Value: votre-app.elest.io
# 4. SSL automatique avec Let's Encrypt
```

## 📊 Monitoring et logs

### **1. Logs en temps réel**
```bash
# Dans Elest.io dashboard
# 1. Aller dans votre service
# 2. Onglet "Logs"
# 3. Voir les logs en temps réel
# 4. Filtrer par niveau (INFO, ERROR, etc.)
```

### **2. Métriques de performance**
```bash
# Elest.io fournit automatiquement :
# - Utilisation CPU/RAM
# - Temps de réponse
# - Nombre de requêtes
# - Erreurs
```

### **3. Alertes automatiques**
```bash
# 1. Dans Elest.io > Monitoring
# 2. Configurer les alertes :
#    - CPU > 80%
#    - RAM > 80%
#    - Service down
# 3. Notifications par email/Slack
```

## 🔒 Sécurité

### **1. Firewall automatique**
```bash
# Elest.io configure automatiquement :
# - Port 8501 ouvert
# - Ports 22 (SSH) fermés
# - Protection DDoS
# - Rate limiting
```

### **2. SSL/TLS automatique**
```bash
# - Certificats Let's Encrypt automatiques
# - Renouvellement automatique
# - HTTPS obligatoire
# - HSTS activé
```

### **3. Sauvegardes automatiques**
```bash
# Elest.io gère :
# - Sauvegardes quotidiennes
# - Rétention 7 jours
# - Restauration en 1 clic
# - Sauvegarde des volumes
```

## 💰 Coûts estimés

### **Hetzner Cloud**
- **CX11** (1 vCPU, 2GB RAM) : ~3€/mois
- **CX21** (2 vCPU, 4GB RAM) : ~6€/mois (recommandé)
- **CX31** (2 vCPU, 8GB RAM) : ~12€/mois

### **Elest.io**
- **Gratuit** : 1 projet, 1 service
- **Pro** : 10€/mois (illimité)
- **Enterprise** : Sur demande

### **Total estimé**
- **Démarrage** : 3-6€/mois (Hetzner)
- **Production** : 15-20€/mois (Hetzner + Elest.io Pro)

## 🚨 Dépannage

### **Problèmes courants**

#### **1. Build échoue**
```bash
# Vérifier :
# - Fichier requirements_web.txt présent
# - Dockerfile valide
# - Variables d'environnement configurées
```

#### **2. Application ne démarre pas**
```bash
# Vérifier :
# - Port 8501 configuré
# - Variables d'environnement
# - Logs dans Elest.io dashboard
```

#### **3. Erreur OpenAI**
```bash
# Vérifier :
# - Clé API OpenAI valide
# - Crédit suffisant sur OpenAI
# - Variables d'environnement
```

### **Support**
- **Elest.io** : Support intégré dans le dashboard
- **Hetzner** : Support par email/ticket
- **Documentation** : [docs.elest.io](https://docs.elest.io/)

## 🎯 Prochaines étapes

### **Phase 1 : Déploiement basique**
1. ✅ Déploiement sur Elest.io
2. ✅ Configuration SSL
3. ✅ Monitoring de base
4. ✅ Tests de fonctionnement

### **Phase 2 : Optimisation**
1. 🔄 Configuration du cache Redis
2. 🔄 Base de données PostgreSQL
3. 🔄 Load balancing
4. 🔄 CDN

### **Phase 3 : Production**
1. 🔄 Authentification utilisateurs
2. 🔄 Rate limiting avancé
3. 🔄 Monitoring avancé
4. 🔄 Sauvegardes personnalisées

---

**Note** : Elest.io simplifie grandement le déploiement en gérant automatiquement l'infrastructure, la sécurité et le monitoring. Vous vous concentrez sur votre application, Elest.io s'occupe du reste ! 