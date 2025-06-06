from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Charger les données JSON
with open('phones.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('phone_number', '').strip()
    results = []
    
    for category in data.values():
        for entry in category:
            phone = entry.get('Numéro de téléphone', '')
            if search_term in phone:
                results.append({
                    'phone': phone,
                    'operator': entry.get('Operateur', 'Inconnu'),
                    'url': entry.get('URL', '')
                })
    
    return jsonify(results)

@app.route('/all', methods=['GET'])
def get_all():
    results = []
    for category in data.values():
        for entry in category:
            phone = entry.get('Numéro de téléphone', '')
            if phone:  # Ignorer les entrées sans numéro
                results.append({
                    'phone': phone,
                    'operator': entry.get('Operateur', 'Inconnu'),
                    'url': entry.get('URL', '')
                })
    return jsonify({'count': len(results), 'results': results})

if __name__ == '__main__':
    app.run(debug=True)