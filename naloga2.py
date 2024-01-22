# IMPORT
# ------------------------------------------------
from flask import Flask, render_template, jsonify, url_for


# GLOBAL VARIABLES
# ------------------------------------------------
consumption_data = []   # Globalni seznam
total_Wh = 0            # Global variable to store total watt-hours


# FUNCTIONS
# ------------------------------------------------
def print_consumption_data():
    global consumption_data, total_Wh
    print("\nConsumption Data List:\n" + '-' * 50)
    for index, data in enumerate(consumption_data):
        print(f"Entry {index + 1}: Time - {data['time']}s, Watts - {data['watts']}, Watt-hours - {data['watt-hours']:.3f}")
    print('-' * 50 + f"\nTotal Watt-Hours: {total_Wh:.3f}\n")


# FLASK
# ------------------------------------------------
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index2.html')  # Prikaz glavne HTML strani


@app.route('/toggle/<state>/<time>/<watts>')
def export_to_list(state, time, watts):
    global total_Wh
    if state == 'on':
        image_file = 'light_on.jpg'
    else:
        if time != "0":
            watt_hours = (int(time) / 3600) * int(watts)
            consumption_data.append({
                "time": int(time),
                "watts": int(watts),
                "watt-hours": watt_hours
            })
            total_Wh += watt_hours  # Add to the total watt-hours
            print_consumption_data()

        image_file = 'light_off.jpg'
    return jsonify({'image': url_for('static', filename=image_file), 'state': 'off' if state == 'on' else 'on'})


@app.route('/get_consumption_data')
def get_consumption_data():
    global total_Wh
    return jsonify({'data': consumption_data, 'total_Wh': total_Wh})


# MAIN
# ------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)  # Zagon Flask aplikacije v načinu razhroščevanja


