# IMPORT
# ------------------------------------------------
from flask import Flask, render_template, jsonify, url_for


# GLOBALNE SPREMENLJIVKE
# ------------------------------------------------
consumption_data = []   # Globalni seznam, ki shranjuje podatke o porabi
total_Wh = 0            # Globalna spremenljivka za shranjevanje skupnih vat-ur


# FUNKCIJE
# ------------------------------------------------
def print_consumption_data():
    # Ta funkcija izpiše trenutne podatke o porabi.
    # Izpisuje podatke za vsak vnos posebej in izračuna skupne vat-ure.
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
    # Ta pot prikaže glavno HTML stran.
    return render_template('index2.html')


@app.route('/toggle/<state>/<time>/<watts>')
def export_to_list(state, time, watts):
    # Ta pot upravlja vklop/izklop in spremlja porabo.
    # Ko se luč izklopi, shranjuje čas, vate in izračuna vat-ure.
    global total_Wh
    if state == 'on':
        image_file = 'light_on.png'
    else:
        if time != "0":
            watt_hours = (int(time) / 3600) * int(watts)
            consumption_data.append({
                "time": int(time),
                "watts": int(watts),
                "watt-hours": watt_hours
            })
            total_Wh += watt_hours      # Dodajanje k skupnim vat-uram
            print_consumption_data()    # Izpis seznama porabe

        image_file = 'light_off.png'
    return jsonify({'image': url_for('static', filename=image_file), 'state': 'off' if state == 'on' else 'on'})


@app.route('/get_consumption_data')
def get_consumption_data():
    # Ta pot vrača trenutne podatke o porabi za prikaz na front-end.
    global total_Wh
    return jsonify({'data': consumption_data, 'total_Wh': total_Wh})


# GLAVNI DEL
# ------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)  # Zagon Flask aplikacije v načinu za razhroščevanje
