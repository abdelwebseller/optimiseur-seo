# Dockerfile pour Next.js
FROM node:18-alpine

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY frontend-nextjs/package*.json ./

# Installer les dépendances
RUN npm ci --only=production

# Copier le code source
COPY frontend-nextjs/ .

# Construire l'application
RUN npm run build

# Exposer le port
EXPOSE 3000

# Commande de démarrage
CMD ["npm", "start"] 