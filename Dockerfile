FROM python:3.12-slim

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Installer les dépendances système pour PostgreSQL et psql
RUN apt-get update && apt-get install -y gcc libpq-dev postgresql-client && rm -rf /var/lib/apt/lists/*


# Installer les dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copier le code de l'application
COPY . .

# Commande par défaut pour démarrer le serveur
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
