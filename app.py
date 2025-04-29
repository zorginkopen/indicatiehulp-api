from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

# Beslisboom laden
with open('beslisboom.json', encoding='utf-8') as f:
    beslisboom = json.load(f)["beslisboom"]

def zoek_profiel(adl, gedrag, cognitie, mantelzorg):
    for regel in beslisboom:
        voorwaarden = regel['voorwaarden']
        if (voorwaarden['adl'].lower().strip() == adl.lower().strip() and
            voorwaarden['gedrag'].lower().strip() == gedrag.lower().strip() and
            voorwaarden['cognitie'].lower().strip() == cognitie.lower().strip() and
            voorwaarden['mantelzorg'].lower().strip() == mantelzorg.lower().strip()):
            return regel
    return None

@app.route('/api/advies', methods=['POST'])
def advies():
    data = request.json
    result = zoek_profiel(
        data.get('adl'),
        data.get('gedrag'),
        data.get('cognitie'),
        data.get('mantelzorg')
    )
    if result:
        return jsonify(result)
    else:
        return jsonify({
            "advies": "Geen exacte match gevonden.",
            "onderbouwing": "Geen profiel past volledig. Overweeg nadere analyse."
        })

@app.route('/openapi.json')
def serve_openapi():
    return send_from_directory(os.getcwd(), 'openapi.json', mimetype='application/json')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)