# 🚀 Guide de déploiement - Refonte Frontend Next.js

## 📋 Étapes pour déployer la nouvelle interface

### 1. 🎯 Créer la Pull Request

**Lien direct** : [https://github.com/abdelwebseller/optimiseur-seo/pull/new/refonte-frontend](https://github.com/abdelwebseller/optimiseur-seo/pull/new/refonte-frontend)

#### Configuration de la Pull Request :

**Titre** :
```
🎨 Refonte Frontend : Migration vers Next.js + Heroui
```

**Description** :
```markdown
## 🎯 Objectif
Migration complète du frontend Streamlit vers Next.js 14 avec Heroui

## ✨ Nouvelles fonctionnalités
- Interface moderne avec Next.js 14 (App Router + TypeScript)
- Design system Heroui + TailwindCSS
- Pages : Dashboard, Results, Settings, Login, Signup
- Système de notifications intégré
- API calls préparés pour le backend Python
- Authentication prête (Auth.js/Clerk/Auth0)

## 🔧 Stack technique
- Next.js 14 (App Router + TypeScript)
- TailwindCSS
- Heroui (design system)
- Framer Motion (animations)
- ESLint + TypeScript

## 📁 Structure
- `/dashboard` : Upload sitemap + analyse
- `/results` : Affichage des suggestions SEO
- `/settings` : Configuration
- `/login` & `/signup` : Authentication

## 🚀 Déploiement
Prêt pour déploiement sur Elestio avec variables d'environnement configurées

## 📋 Checklist
- [x] Frontend Next.js créé
- [x] Branche `refonte-frontend` publiée
- [x] Variables d'environnement documentées
- [ ] Pull Request à merger
- [ ] Configuration Elestio à mettre à jour
- [ ] Test de l'interface en production
```

### 2. 🔄 Merger la Pull Request

1. **Clique sur "Create pull request"**
2. **Vérifie les changements** dans l'onglet "Files changed"
3. **Clique sur "Merge pull request"**
4. **Confirme le merge** → `refonte-frontend` devient `main`

### 3. ⚙️ Configuration Elestio

#### Variables d'environnement à ajouter :

```bash
# Variables OBLIGATOIRES
OPENAI_API_KEY=sk-proj-votre-cle-openai-ici
NODE_ENV=production
NEXT_PUBLIC_APP_URL=https://optimiseur-seo-u19040.vm.elestio.app

# API Backend
NEXT_PUBLIC_API_URL=https://optimiseur-seo-u19040.vm.elestio.app/api

# Authentication (optionnel)
NEXTAUTH_SECRET=votre-secret-jwt-ici
NEXTAUTH_URL=https://optimiseur-seo-u19040.vm.elestio.app
```

#### Étapes sur Elestio Dashboard :

1. **Va sur** : [https://optimiseur-seo-u19040.vm.elestio.app/](https://optimiseur-seo-u19040.vm.elestio.app/)
2. **Dashboard Elestio** → Ton projet
3. **Section "Environment Variables"**
4. **Ajoute les variables ci-dessus**
5. **Clique sur "Save"**
6. **Redéploie l'application**

### 4. 🚀 Redéploiement

#### Option 1 : Redéploiement automatique
- Si Elestio est configuré pour détecter les changements sur `main`
- Le redéploiement se fera automatiquement après le merge

#### Option 2 : Redéploiement manuel
1. **Dashboard Elestio** → Ton projet
2. **Section "Deployments"**
3. **Clique sur "Redeploy"**
4. **Attends la fin du déploiement**

### 5. ✅ Vérification

#### Test de l'interface :
1. **Page d'accueil** : [https://optimiseur-seo-u19040.vm.elestio.app/](https://optimiseur-seo-u19040.vm.elestio.app/)
2. **Dashboard** : [https://optimiseur-seo-u19040.vm.elestio.app/dashboard](https://optimiseur-seo-u19040.vm.elestio.app/dashboard)
3. **Results** : [https://optimiseur-seo-u19040.vm.elestio.app/results](https://optimiseur-seo-u19040.vm.elestio.app/results)
4. **Settings** : [https://optimiseur-seo-u19040.vm.elestio.app/settings](https://optimiseur-seo-u19040.vm.elestio.app/settings)

#### Vérifications à faire :
- ✅ L'application se charge sans erreurs
- ✅ Les pages sont accessibles
- ✅ L'interface est responsive
- ✅ Les appels API fonctionnent (si backend configuré)
- ✅ Les notifications s'affichent

### 6. 🔧 Configuration avancée

#### Si backend séparé :
```bash
NEXT_PUBLIC_API_URL=https://votre-backend.elestio.app
```

#### Pour l'authentification :
```bash
NEXTAUTH_SECRET=votre-secret-jwt-ici
NEXTAUTH_URL=https://optimiseur-seo-u19040.vm.elestio.app
```

#### Variables d'interface :
```bash
NEXT_PUBLIC_APP_NAME="Optimiseur SEO"
NEXT_PUBLIC_APP_DESCRIPTION="Maillage interne automatique avec IA"
NEXT_PUBLIC_COMPANY_NAME="Votre Entreprise"
```

## 🎯 Résultat attendu

Après ces étapes, tu auras :
- ✅ Nouvelle interface Next.js moderne
- ✅ Design system Heroui intégré
- ✅ Pages fonctionnelles : Dashboard, Results, Settings
- ✅ Authentication prête
- ✅ API calls configurés
- ✅ Déploiement Elestio opérationnel

## 🆘 En cas de problème

### Erreurs courantes :
1. **Variables manquantes** → Vérifie `ENV_VARIABLES.md`
2. **Build échoue** → Vérifie les logs Elestio
3. **API ne répond pas** → Vérifie `NEXT_PUBLIC_API_URL`
4. **Page blanche** → Vérifie `NODE_ENV=production`

### Support :
- **Logs Elestio** : Dashboard → Logs
- **Variables** : Dashboard → Environment Variables
- **Déploiement** : Dashboard → Deployments

---

**🎉 Félicitations ! Tu auras une interface moderne et performante !** 