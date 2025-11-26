from flask import Flask, request, render_template, jsonify
import os
import json
import random
from openai import OpenAI

app = Flask(__name__)

# Configuration des dossiers
STRUCTURE_FOLDER = "structures"
os.makedirs(STRUCTURE_FOLDER, exist_ok=True)

# Configuration OpenAI - À remplacer par votre clé API
client = OpenAI(api_key="VOTRE_CLÉ_API_ICI")

def extract_json_from_text(text):
    """Extrait le JSON d'une réponse texte."""
    start = text.find('{')
    end = text.rfind('}') + 1
    if start == -1 or end == -1:
        raise ValueError("JSON non trouvé")
    return json.loads(text[start:end])

def generate_structure(prompt):
    """
    Génère une structure de serveur Discord via OpenAI.

    Args:
        prompt (str): La description du serveur.

    Returns:
        dict: La structure du serveur.
    """
    system_msg = """
    Tu es un assistant chargé de générer la structure JSON complète d'un serveur Discord.
    Tu dois retourner uniquement ce format (et rien d'autre) :

    {
      "roles": ["Rôle1", "Rôle2", "Rôle3", "Rôle4"],
      "categories": [
        {
          "name": "Nom de catégorie",
          "text_channels": ["salon1", "salon2", "salon3"],
          "voice_channels": ["vocal1", "vocal2"]
        }
      ]
    }

    Règles :
    - Génère 3 à 5 catégories, chacune avec 2 à 4 salons texte, 1 à 3 vocaux.
    - Si le thème est "esthétique", ajoute des caractères spéciaux ou emojis dans les noms (ex : ⋆ | • | ⭑ | ★).
    - Pas de texte explicatif, pas de code, uniquement du JSON.
    """

    user_msg = f"Demande : {prompt}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.9,
            max_tokens=900
        )

        raw = response.choices[0].message.content.strip()
        print("GPT reply:", raw)
        
        return extract_json_from_text(raw)
    
    except Exception as e:
        print(f"Erreur API OpenAI: {e}")
        # Structure par défaut en cas d'erreur
        return {
            "roles": ["Admin", "Membre", "Modérateur"],
            "categories": [{
                "name": "Général",
                "text_channels": ["général", "annonces"],
                "voice_channels": ["vocal général"]
            }]
        }

@app.route("/", methods=["GET", "POST"])
def index():
    """Page principale du générateur de serveur."""
    if request.method == "POST":
        prompt = request.form.get("prompt", "")
        if not prompt:
            return render_template("index.html", error="Veuillez entrer une description")
        
        structure = generate_structure(prompt)
        code = str(random.randint(100000, 999999))
        
        # Sauvegarder la structure
        path = os.path.join(STRUCTURE_FOLDER, f"{code}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(structure, f, indent=2, ensure_ascii=False)
        
        return render_template("index.html", code=code)
    
    return render_template("index.html")

@app.route("/structure/<code>")
def get_structure(code):
    """API pour récupérer une structure par son code."""
    path = os.path.join(STRUCTURE_FOLDER, f"{code}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read(), 200, {"Content-Type": "application/json"}
    return jsonify({"error": "Code introuvable"}), 404

@app.errorhandler(404)
def not_found(error):
    """Gestion des erreurs 404."""
    return render_template("index.html", error="Page non trouvée"), 404

@app.errorhandler(500)
def internal_error(error):
    """Gestion des erreurs 500."""
    return render_template("index.html", error="Erreur interne du serveur"), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
