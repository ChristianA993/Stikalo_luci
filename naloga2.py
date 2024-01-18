"""
Aplikacija za vklop/izklop luči s stikalom. Računa koliko časa je luč prižgana oz. stikalo v ON poziciji

"""

from flask import Flask, render_template, jsonify, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index2.html')  # Prikaz glavne HTML strani

@app.route('/toggle/<state>')
def toggle(state):
    if state == 'on':
        return jsonify({'image': url_for('static', filename='light_on.jpg'), 'state': 'off'})
    return jsonify({'image': url_for('static', filename='light_off.jpg'), 'state': 'on'})
    # Vrnitev podatkov v JSON formatu glede na trenutno stanje svetlobe

if __name__ == '__main__':
    app.run(debug=True)  # Zagon Flask aplikacije v načinu razhroščevanja
