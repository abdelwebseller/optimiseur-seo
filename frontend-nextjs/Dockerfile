# Dockerfile pour l'application Next.js SEO Optimizer
FROM node:18-alpine

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY package*.json ./

# Installer les dépendances
RUN npm ci --only=production

# Copier le code source
COPY . .

# Construire l'application
RUN npm run build

# Exposer le port
EXPOSE 3000

# Variables d'environnement
ENV NODE_ENV=production
ENV PORT=3000
ENV HOSTNAME=0.0.0.0

# Script de démarrage avec debug
CMD ["sh", "-c", "echo '=== DEBUG INFO ===' && echo 'Current directory: $(pwd)' && echo 'Files in directory: $(ls -la)' && echo 'Starting Next.js on port $PORT' && echo 'Hostname: $HOSTNAME' && echo 'Node ENV: $NODE_ENV' && echo '=== STARTING APP ===' && echo 'Running: npm start' && npm start 2>&1"] 