from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Laad beslisboom
with open("beslisboom.json", encoding="utf-8") as f:
    beslisboom = json.load(f)["beslisboom"]

def zoek_profiel(adl, gedrag, cognitie, mantelzorg):
    for profiel in beslisboom:
        v = profiel["voorwaarden"]
        if (
            v["adl"].strip().lower() == adl.strip().lower() and
            v["gedrag"].strip().lower() == gedrag.strip().lower() and
            v["cognitie"].strip().lower() == cognitie.strip().lower() and
            v["mantelzorg"].strip().lower() == mantelzorg.strip().lower()
        ):
            return profiel
    return {
        "advies": "Geen exacte match gevonden.",
        "onderbouwing": "Geen profiel gevonden. Controleer de ingevoerde waarden of kies een profiel met vergelijkbare kenmerken."
    }

@app.route("/api/advies", methods=["POST"])
def advies():
    try:
        data = request.get_json(force=True)
        result = zoek_profiel(
            data.get("adl", ""),
            data.get("gedrag", ""),
            data.get("cognitie", ""),
            data.get("mantelzorg", "")
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "Serverfout", "details": str(e)}), 500

@app.route("/openapi.json")
def serve_openapi():
    return send_from_directory(os.getcwd(), 'openapi.json', mimetype='application/json')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)