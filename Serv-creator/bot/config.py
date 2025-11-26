"""
Configuration du bot Discord Serv-Creator

Ce fichier contient les variables de configuration nécessaires
au fonctionnement du bot Discord.
"""

import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Token du bot Discord
# Option 1: Variable d'environnement (recommandé)
# Option 2: Valeur directe (pour développement uniquement)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "TOKEN_HERE")

# Chemin vers le dossier des structures générées
STRUCTURE_PATH = os.getenv("STRUCTURE_PATH", "../site/structures")

# Configuration supplémentaire
BOT_PREFIX = os.getenv("BOT_PREFIX", "!")
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

# Vérification des variables obligatoires
if DISCORD_TOKEN == "TOKEN_HERE":
    print("⚠️  ATTENTION: Veuillez configurer votre token Discord")
    print("   1. Créez un fichier .env avec: DISCORD_TOKEN=votre_token")
    print("   2. Ou modifiez directement ce fichier")
