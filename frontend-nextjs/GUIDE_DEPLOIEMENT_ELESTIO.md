# 🚀 Guide de Déploiement Elestio - SEO Optimizer

## 📋 Configuration Elestio

### **1. Variables d'environnement (.env)**

```env
# Configuration Next.js
NODE_ENV=production
NEXT_PUBLIC_APP_URL=https://ton-domaine.elestio.app
NEXT_PUBLIC_API_URL=https://ton-domaine.elestio.app/api

# Configuration serveur
PORT=3000
HOSTNAME=0.0.0.0

# Clé OpenAI
OPENAI_API_KEY=sk-proj-ta-clé-openai

# Configuration NextAuth
NEXTAUTH_SECRET=ton-secret-ici
NEXTAUTH_URL=https://ton-domaine.elestio.app
```

### **2. Ports exposés**

| Interface | Protocole | Port Host | Port Container |
|-----------|-----------|-----------|----------------|
| 0.0.0.0   | HTTP      | 3000      | 3000           |

### **3. Configuration Volume**

| Chemin Host | Chemin Container |
|-------------|------------------|
| `./logs`    | `/app/logs`      |
| `./output`  | `/app/output`    |

### **4. Reverse Proxy Configuration**

**Listen :**
- Protocol : HTTPS
- Port : 443
- Require Basic Auth : ❌ (décoché)

**Target :**
- Protocol : HTTP
- IP : 172.17.0.1
- Port : 3000
- Path : /

### **5. Commandes de build/démarrage**

**Build Command :**
```bash
npm ci && npm run build
```

**Start Command :**
```bash
npm start
```

## 🔧 Étapes de Déploiement

### **Étape 1 : Préparation**
1. Assurez-vous que votre code est poussé sur GitHub
2. Vérifiez que le Dockerfile est présent dans le dossier `frontend-nextjs/`

### **Étape 2 : Configuration Elestio**
1. Connectez-vous à votre dashboard Elestio
2. Créez un nouveau service ou modifiez l'existant
3. Configurez les variables d'environnement ci-dessus
4. Définissez les ports exposés (3000)
5. Configurez le reverse proxy pour cibler le port 3000

### **Étape 3 : Déploiement**
1. Lancez le déploiement
2. Surveillez les logs pour détecter d'éventuelles erreurs
3. Vérifiez que l'application démarre correctement

## 🐛 Dépannage

### **Problème : Erreur 502**
- Vérifiez que le port 3000 est bien exposé
- Contrôlez les logs du conteneur
- Assurez-vous que `HOSTNAME=0.0.0.0` est défini

### **Problème : Variables d'environnement non reconnues**
- Vérifiez que les variables commençant par `NEXT_PUBLIC_` sont bien définies
- Redéployez après modification des variables

### **Problème : Build échoue**
- Vérifiez que `package.json` est présent
- Contrôlez que toutes les dépendances sont installées

## 📊 Vérification

### **URLs de test :**
- **Page d'accueil** : `https://ton-domaine.elestio.app/`
- **Dashboard** : `https://ton-domaine.elestio.app/dashboard`
- **Résultats** : `https://ton-domaine.elestio.app/results`
- **Paramètres** : `https://ton-domaine.elestio.app/settings`

### **Fonctionnalités à tester :**
1. ✅ Navigation entre les pages
2. ✅ Mode sombre/clair
3. ✅ Formulaire de connexion
4. ✅ Dashboard avec formulaire d'analyse
5. ✅ Page des résultats avec tableau
6. ✅ Page des paramètres avec formulaires

## 🔄 Mise à jour

Pour mettre à jour l'application :
1. Poussez les modifications sur GitHub
2. Redéployez sur Elestio
3. Vérifiez que les nouvelles fonctionnalités fonctionnent

## 📞 Support

En cas de problème :
1. Vérifiez les logs Elestio
2. Testez l'application en local d'abord
3. Consultez la documentation Next.js si nécessaire 