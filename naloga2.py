from flask import Flask, render_template, jsonify, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/toggle/<state>')
def toggle(state):
    if state == 'on':
        return jsonify({'image': url_for('static', filename='light_on.jpg'), 'state': 'off'})
    return jsonify({'image': url_for('static', filename='light_off.jpg'), 'state': 'on'})

if __name__ == '__main__':
    app.run(debug=True)
