from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Laad het volledige indicatiebestand
with open('beslisboom.json', encoding='utf-8') as f:
    beslisboom = json.load(f)["beslisboom"]

# Helperfunctie voor exacte match
def zoek_profiel(adl, gedrag, cognitie, mantelzorg):
    for regel in beslisboom:
        voorwaarden = regel['voorwaarden']
        if (voorwaarden['adl'] == adl and
            voorwaarden['gedrag'] == gedrag and
            voorwaarden['cognitie'] == cognitie and
            voorwaarden['mantelzorg'] == mantelzorg):
            return regel
    return None

@app.route('/', methods=['GET'])
def triage_get():
    adl = request.args.get('adl')
    gedrag = request.args.get('gedrag')
    cognitie = request.args.get('cognitie')
    mantelzorg = request.args.get('mantelzorg')

    result = zoek_profiel(adl, gedrag, cognitie, mantelzorg)
    if result:
        return jsonify(result)
    else:
        return jsonify({
            "advies": "Geen exacte match gevonden.",
            "onderbouwing": "De combinatie van kenmerken komt niet overeen met een bekend profiel. Overweeg nadere analyse."
        })

@app.route('/api/advies', methods=['POST'])
def triage_post():
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
            "onderbouwing": "De combinatie van kenmerken komt niet overeen met een bekend profiel. Overweeg alternatief profiel."
        })

if __name__ == '__main__':
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
