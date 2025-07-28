# Dockerfile pour Next.js
FROM node:18-alpine

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY frontend-nextjs/package*.json ./

# Installer toutes les dépendances
RUN npm ci

# Copier le code source
COPY frontend-nextjs/ .

# Variables d'environnement pour le build
ENV NEXT_TELEMETRY_DISABLED 1
ENV NODE_ENV production

# Build de l'application
RUN npm run build

# Exposer le port
EXPOSE 3000

# Variables d'environnement pour le runtime
ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

# Script de démarrage avec debug complet et vérification
CMD ["sh", "-c", "echo '=== DEBUG INFO ===' && echo 'Current directory: $(pwd)' && echo 'Files in directory: $(ls -la)' && echo 'Starting Next.js on port $PORT' && echo 'Hostname: $HOSTNAME' && echo 'Node ENV: $NODE_ENV' && echo '=== STARTING APP ===' && echo 'Running: npm start' && npm start 2>&1"] 