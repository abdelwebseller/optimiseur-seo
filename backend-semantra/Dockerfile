FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Créer le répertoire pour les logs
RUN mkdir -p logs

# Exposer le port
EXPOSE 8000

# Commande par défaut
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"] 