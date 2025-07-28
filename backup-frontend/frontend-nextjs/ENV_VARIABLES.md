# 🔧 Variables d'environnement pour Next.js

## 📋 Variables requises pour le déploiement

### 🔐 Variables d'authentification
```bash
# OpenAI API (pour les embeddings et l'IA)
OPENAI_API_KEY=sk-proj-votre-cle-openai-ici

# Auth.js (optionnel - pour l'authentification)
NEXTAUTH_SECRET=votre-secret-jwt-ici
NEXTAUTH_URL=https://votre-app.elestio.app
```

### 🌐 Variables de configuration Next.js
```bash
# Configuration de base
NODE_ENV=production
NEXT_PUBLIC_APP_URL=https://votre-app.elestio.app

# API Backend (URL de votre API Python)
NEXT_PUBLIC_API_URL=https://votre-api-backend.elestio.app
# ou si même domaine :
NEXT_PUBLIC_API_URL=https://votre-app.elestio.app/api
```

### 🔗 Variables pour les appels API
```bash
# Configuration des endpoints API
NEXT_PUBLIC_API_ENDPOINTS='{
  "process_sitemap": "/process-sitemap",
  "get_status": "/status", 
  "get_results": "/results",
  "export_csv": "/download?format=csv"
}'
```

### 🎨 Variables d'interface (optionnelles)
```bash
# Configuration de l'interface
NEXT_PUBLIC_APP_NAME="Optimiseur SEO"
NEXT_PUBLIC_APP_DESCRIPTION="Maillage interne automatique avec IA"
NEXT_PUBLIC_COMPANY_NAME="Votre Entreprise"
```

## 🚀 Configuration Elestio

### 1. Variables obligatoires
```bash
OPENAI_API_KEY=sk-proj-votre-cle-openai-ici
NODE_ENV=production
NEXT_PUBLIC_APP_URL=https://votre-app.elestio.app
```

### 2. Variables pour l'API backend
```bash
# Si vous avez un backend séparé
NEXT_PUBLIC_API_URL=https://votre-backend.elestio.app

# Si même domaine (recommandé)
NEXT_PUBLIC_API_URL=https://votre-app.elestio.app/api
```

### 3. Variables d'authentification (optionnel)
```bash
NEXTAUTH_SECRET=votre-secret-jwt-ici
NEXTAUTH_URL=https://votre-app.elestio.app
```

## 📝 Instructions de configuration

### Sur Elestio Dashboard :
1. Allez dans votre projet
2. Section "Environment Variables"
3. Ajoutez les variables ci-dessus
4. Redéployez l'application

### Variables critiques pour le fonctionnement :
- ✅ `OPENAI_API_KEY` : **OBLIGATOIRE** pour les embeddings
- ✅ `NODE_ENV=production` : **OBLIGATOIRE** pour Next.js
- ✅ `NEXT_PUBLIC_APP_URL` : **OBLIGATOIRE** pour les URLs absolues

### Variables optionnelles :
- 🔧 `NEXT_PUBLIC_API_URL` : Pour les appels API backend
- 🔐 `NEXTAUTH_SECRET` : Pour l'authentification
- 🎨 `NEXT_PUBLIC_APP_NAME` : Personnalisation de l'interface

## 🔍 Vérification

Après déploiement, vérifiez que :
1. L'application se charge sans erreurs
2. Les appels API fonctionnent
3. Les embeddings OpenAI sont générés
4. L'interface est responsive

## 🚨 Notes importantes

- **Toutes les variables `NEXT_PUBLIC_*` sont visibles côté client**
- **Ne jamais exposer les clés API sensibles côté client**
- **Utilisez `NEXTAUTH_SECRET` pour sécuriser les sessions**
- **Testez en local avec `.env.local` avant déploiement** 