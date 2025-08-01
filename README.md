# 🔗 Optimiseur SEO - Frontend Next.js

Application web moderne pour optimiser le maillage interne de sites web en utilisant l'intelligence artificielle OpenAI.

## 🚀 Déploiement

### Déploiement sur Elest.io

1. Connecter ce repository à Elest.io
2. Configurer les variables d'environnement
3. Déploiement automatique en 5 minutes

### Variables d'environnement requises

```bash
OPENAI_API_KEY=sk-proj-votre-cle-openai-ici
NODE_ENV=production
NEXT_PUBLIC_APP_URL=https://votre-app.elestio.app
NEXT_PUBLIC_API_URL=https://votre-app.elestio.app/api
```

## 📁 Structure du projet

```
optimiseur-seo/
├── frontend-nextjs/           # Application Next.js
│   ├── src/                   # Code source
│   ├── public/                # Assets statiques
│   ├── package.json           # Dépendances Node.js
│   ├── Dockerfile             # Configuration Docker
│   └── README.md              # Documentation Next.js
└── README.md                  # Ce fichier
```

## 🔧 Fonctionnalités

* ✅ Interface moderne avec Next.js 14 + TypeScript
* ✅ Design system Heroui + TailwindCSS
* ✅ Pages : Dashboard, Results, Settings, Login, Signup
* ✅ Système de notifications intégré
* ✅ API calls préparés pour le backend Python
* ✅ Authentication prête (Auth.js/Clerk/Auth0)
* ✅ Responsive design
* ✅ Export CSV/Excel

## 🌐 Accès

Une fois déployé, l'application sera accessible sur :

```
https://votre-app.elestio.app
```

## 📞 Support

* Documentation : `frontend-nextjs/README.md`
* Variables d'environnement : `frontend-nextjs/ENV_VARIABLES.md`
* Guide de déploiement : `frontend-nextjs/GUIDE_DEPLOIEMENT.md`
* Support Elest.io : Dashboard intégré

---

**Note** : Cette version utilise Next.js 14 avec Heroui pour une interface moderne et performante.

## 🗂️ Branches

- `main` : Frontend Next.js (actuel)
- `refonte-frontend` : Branche de développement Next.js
- `backup-streamlit` : Sauvegarde de l'ancienne app Streamlit
