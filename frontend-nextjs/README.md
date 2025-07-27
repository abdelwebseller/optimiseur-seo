# Optimiseur SEO - Frontend Next.js

Application de maillage interne intelligent alimentée par l'IA pour optimiser votre SEO.

## 🚀 Technologies Utilisées

- **Next.js 14** - Framework React avec App Router
- **TypeScript** - Typage statique pour un code plus robuste
- **TailwindCSS** - Framework CSS utilitaire
- **Heroui** - Composants UI modernes et accessibles
- **Framer Motion** - Animations fluides
- **NextAuth.js** - Authentification (préparé pour l'intégration)

## 📋 Prérequis

- Node.js 18+ 
- npm ou yarn
- Git

## 🛠️ Installation

1. **Cloner le projet**
   ```bash
   git clone <votre-repo>
   cd frontend-nextjs
   ```

2. **Installer les dépendances**
   ```bash
   npm install
   ```

3. **Lancer le serveur de développement**
   ```bash
   npm run dev
   ```

4. **Ouvrir l'application**
   ```
   http://localhost:3000
   ```

## 📁 Structure du Projet

```
frontend-nextjs/
├── src/
│   ├── app/                    # App Router Next.js 14
│   │   ├── dashboard/         # Page dashboard
│   │   ├── results/           # Page résultats
│   │   ├── settings/          # Page paramètres
│   │   ├── login/             # Page connexion
│   │   ├── signup/            # Page inscription
│   │   ├── layout.tsx         # Layout principal
│   │   ├── page.tsx           # Page d'accueil
│   │   └── providers.tsx      # Providers Heroui
│   ├── components/            # Composants réutilisables
│   │   └── Navigation.tsx     # Navigation principale
│   └── lib/                   # Utilitaires et configurations
├── public/                    # Assets statiques
├── package.json
└── README.md
```

## 🎯 Fonctionnalités

### ✅ Implémentées
- **Page d'accueil** - Landing page moderne avec présentation des fonctionnalités
- **Dashboard** - Interface pour uploader et analyser des sitemaps
- **Résultats** - Tableau interactif des suggestions de maillage interne
- **Paramètres** - Configuration de l'application et des APIs
- **Authentification** - Pages de connexion et inscription (UI prête)
- **Navigation** - Menu responsive avec navigation fluide
- **Design System** - Interface cohérente avec Heroui

### 🔄 En cours de développement
- Intégration avec l'API backend Python
- Système d'authentification complet
- Export CSV des résultats
- Notifications en temps réel

## 🎨 Design System

L'application utilise **Heroui** comme design system principal avec :

- **Couleurs** : Palette bleu-violet moderne
- **Typographie** : Geist Sans (Google Fonts)
- **Composants** : Cards, Buttons, Tables, Forms, etc.
- **Responsive** : Mobile-first design
- **Accessibilité** : Conforme aux standards WCAG

## 🔌 API Endpoints

L'application est préparée pour communiquer avec le backend Python via ces endpoints :

```typescript
// Endpoints à implémenter
POST /api/process-sitemap    // Lancer l'analyse
GET  /api/status            // Statut de l'analyse
GET  /api/results           // Récupérer les résultats
GET  /api/download          // Export CSV
```

## 🚀 Déploiement

### Vercel (Recommandé)
```bash
npm run build
vercel --prod
```

### Autres plateformes
```bash
npm run build
npm start
```

## 🔧 Configuration

### Variables d'environnement
Créer un fichier `.env.local` :

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_SECRET=your-secret-key
NEXTAUTH_URL=http://localhost:3000
```

### Configuration Heroui
Le thème est configuré dans `src/app/providers.tsx` avec support du mode sombre.

## 📱 Pages Disponibles

- **/** - Page d'accueil avec présentation
- **/dashboard** - Interface d'analyse de sitemap
- **/results** - Affichage des suggestions de maillage
- **/settings** - Configuration de l'application
- **/login** - Page de connexion
- **/signup** - Page d'inscription

## 🎯 Fonctionnalités Clés

### Dashboard
- Upload de sitemap XML via URL
- Suivi en temps réel de l'analyse
- Historique des analyses récentes
- Interface intuitive avec feedback visuel

### Résultats
- Tableau interactif avec filtres
- Recherche dans les résultats
- Pagination des suggestions
- Actions d'approbation/rejet
- Export CSV des données

### Paramètres
- Configuration API OpenAI
- Seuils de similarité
- Préférences utilisateur
- Configuration avancée

## 🔒 Sécurité

- Validation des formulaires côté client
- Protection CSRF (via Next.js)
- Authentification préparée (NextAuth.js)
- Variables d'environnement sécurisées

## 🧪 Tests

```bash
# Tests unitaires
npm run test

# Tests E2E
npm run test:e2e

# Vérification des types
npm run type-check
```

## 📈 Performance

- **Lazy Loading** des composants
- **Image Optimization** avec Next.js
- **Code Splitting** automatique
- **Bundle Analysis** disponible

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

Pour toute question ou problème :

1. Consulter la documentation
2. Vérifier les issues existantes
3. Créer une nouvelle issue avec les détails

## 🔄 Mise à jour

```bash
# Mettre à jour les dépendances
npm update

# Vérifier les vulnérabilités
npm audit

# Mettre à jour Next.js
npm install next@latest
```

---

**Développé avec ❤️ pour optimiser votre SEO**
