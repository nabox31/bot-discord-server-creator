# 🤖 Serv-Creator - Générateur de Serveur Discord

Un projet complet pour générer automatiquement des serveurs Discord avec une interface web et un bot Discord.

## 📋 Description

Serv-Creator est une solution tout-en-un qui permet de :
- Générer des structures de serveur Discord via une interface web utilisant l'IA (OpenAI)
- Déployer automatiquement les structures générées avec un bot Discord
- Personnaliser les serveurs selon différents thèmes et préférences

## 🏗️ Architecture du Projet

```
Serv-creator/
├── bot/                    # Bot Discord
│   ├── bot.py             # Code principal du bot
│   ├── config.py          # Configuration du bot
│   └── requirements.txt   # Dépendances Python
├── site/                   # Interface web
│   ├── app.py             # Application Flask
│   ├── templates/         # Templates HTML
│   │   └── index.html     # Page principale
│   ├── structures/        # Stockage des structures JSON
│   └── requirements.txt   # Dépendances Python
└── README.md              # Ce fichier
```

## 🚀 Fonctionnalités

### 🌐 Interface Web
- Génération de structures de serveur via IA
- Interface moderne et intuitive
- Génération de codes uniques pour chaque structure
- Support des thèmes esthétiques avec emojis

### 🤖 Bot Discord
- Création automatique de catégories et salons
- Gestion des rôles
- Commande de nettoyage avec confirmation
- Salon de bienvenue automatique

## 🛠️ Installation et Configuration

### Prérequis
- Python 3.8+
- Une clé API OpenAI
- Un token de bot Discord

### 1. Cloner le projet
```bash
git clone https://github.com/votre-username/Serv-creator.git
cd Serv-creator/Serv-creator
```

### 2. Configuration du Bot Discord
1. Créez un bot sur le [Portail Développeur Discord](https://discord.com/developers/applications)
2. Obtenez le token du bot
3. Configurez les permissions nécessaires :
   - Gérer les salons
   - Gérer les rôles
   - Lire les messages

4. Mettez à jour `bot/config.py` :
```python
DISCORD_TOKEN = "VOTRE_TOKEN_DISCORD"
STRUCTURE_PATH = "../site/structures"
```

### 3. Configuration de l'Interface Web
1. Obtenez une clé API OpenAI sur [platform.openai.com](https://platform.openai.com)
2. Mettez à jour `site/app.py` :
```python
client = OpenAI(api_key="VOTRE_CLÉ_API_OPENAI")
```

### 4. Installation des dépendances

#### Pour le bot :
```bash
cd bot
pip install -r requirements.txt
```

#### Pour le site web :
```bash
cd site
pip install -r requirements.txt
```

## 🎯 Utilisation

### Démarrer le site web
```bash
cd site
python app.py
```
Le site sera accessible sur `http://localhost:5000`

### Démarrer le bot
```bash
cd bot
python bot.py
```

### Étapes d'utilisation
1. **Générer une structure** : Utilisez l'interface web pour décrire votre serveur
2. **Obtenir le code** : Le site vous donnera un code unique (ex: 123456)
3. **Ajouter le bot** : Invitez le bot sur votre serveur Discord
4. **Créer le serveur** : Utilisez la commande `!create 123456` sur Discord

## 📝 Commandes du Bot

- `!help` - Affiche l'aide et les commandes disponibles
- `!create <code>` - Crée la structure du serveur à partir d'un code
- `!test` - Vérifie si le bot fonctionne correctement
- `!nuke` - Supprime tous les salons (nécessite les permissions administrateur)

## 🔧 Personnalisation

### Thèmes supportés
L'IA peut générer des structures pour différents thèmes :
- Gaming (Fortnite, Minecraft, etc.)
- Communauté
- Esthétique (avec emojis et caractères spéciaux)
- Professionnel
- Éducation

### Modification des templates
Vous pouvez modifier le prompt système dans `site/app.py` pour ajuster les générations.

## 🐛 Dépannage

### Problèmes courants
1. **Bot ne répond pas** : Vérifiez que le token est correct et que le bot a les permissions nécessaires
2. **Erreur API OpenAI** : Vérifiez votre clé API et votre quota
3. **Code introuvable** : Assurez-vous que le dossier `structures` existe et est accessible

### Logs
- Le bot affiche les erreurs dans la console
- Le site web logge les réponses de l'API OpenAI

## 🤝 Contribuer

Les contributions sont les bienvenues ! Voici comment vous pouvez aider :
1. Fork le projet
2. Créez une branche (`git checkout -b feature/nouvelle-fonctionnalité`)
3. Commitez vos changements (`git commit -am 'Ajout d'une nouvelle fonctionnalité'`)
4. Pushez vers la branche (`git push origin feature/nouvelle-fonctionnalité`)
5. Créez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 👨‍💻 Auteur

Créé par **MR NAB** 
- [GitHub](https://github.com/nabox31)
- [Discord](https://discord.com/users/1277325659508703274)

## 🙏 Remerciements

- Merci à Discord pour l'API et le support
- Merci à OpenAI pour l'API de génération de contenu
- Merci à la communauté Python pour les excellentes bibliothèques

---

⚠️ **Avertissement** : Ce bot peut modifier considérablement votre serveur Discord. Utilisez-le avec précaution et assurez-vous d'avoir des sauvegardes si nécessaire.
