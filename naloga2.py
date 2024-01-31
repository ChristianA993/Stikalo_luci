# IMPORT
# ------------------------------------------------
from flask import Flask, render_template, jsonify, url_for  # Uvoz potrebnih knjižnic za delo s Flaskom, renderiranje predlog, vračanje JSON odgovorov in delo z URLji
from datetime import datetime  # Uvoz knjižnice za delo z datumom in časom
import csv  # Uvoz knjižnice za delo s CSV datotekami

# GLOBALNE SPREMENLJIVKE
# ------------------------------------------------
consumption_data = []   # Globalni seznam za shranjevanje podatkov o porabi
total_Wh = 0            # Globalna spremenljivka za shranjevanje skupne porabe v vatnih urah


# FUNKCIJE
# ------------------------------------------------
def save_to_csv():
    # Funkcija za shranjevanje podatkov o porabi v CSV datoteko
    global consumption_data
    try:
        with open('consumption_data.csv', 'w', newline='') as file:
            fieldnames = ['timestamp', 'time', 'watts', 'watt-hours']  # Imena stolpcev v CSV datoteki
            writer = csv.DictWriter(file, fieldnames=fieldnames)  # Ustvarjanje pisalca za pisanje slovarjev v CSV

            writer.writeheader()  # Pisanje vrstice z imeni stolpcev
            for data in consumption_data:
                writer.writerow(data)  # Pisanje posameznih vrstic podatkov
    except Exception as e:
        print("Error saving to CSV:", str(e))


def load_from_csv():
    # Funkcija za branje podatkov o porabi iz CSV datoteke in njihovo nalaganje ob zagonu aplikacije
    global consumption_data
    try:
        with open('consumption_data.csv', 'r') as file:
            reader = csv.DictReader(file)  # Ustvarjanje bralca za branje podatkov iz CSV
            consumption_data = [row for row in reader]  # Branje vseh vrstic in shranjevanje v seznam
            # Pretvorba vrednosti nazaj v ustrezne podatkovne tipe
            for data in consumption_data:
                data['time'] = int(data['time'])
                data['watts'] = int(data['watts'])
                data['watt-hours'] = float(data['watt-hours'])
    except FileNotFoundError:
        consumption_data = []  # Če datoteka ne obstaja, začnemo s praznim seznamom


def print_consumption_data():
    # Funkcija za izpis trenutnih podatkov o porabi v konzolo
    global consumption_data, total_Wh
    print("\nConsumption Data List:\n" + '-' * 50)
    for index, data in enumerate(consumption_data):
        # Izpis podatkov za vsak vnos s časovnim žigom, časom, vatih in vatnih urah
        print(f"Entry {index + 1}: Timestamp - {data['timestamp']}, Time - {data['time']}s, Watts - {data['watts']}, Watt-hours - {data['watt-hours']:.3f}")

    print('-' * 50 + f"\nTotal Watt-Hours: {total_Wh:.3f}\n")


def recalculate_total_Wh():
    # Funkcija za ponovni izračun skupnih vatnih ur
    global total_Wh
    total_Wh = sum([data['watt-hours'] for data in consumption_data])  # Seštevanje vatnih ur iz vseh vnsov


# FLASK
# ------------------------------------------------
app = Flask(__name__)  # Ustvarjanje Flask aplikacije


@app.route('/')
def index():
    # Funkcija za prikaz glavne HTML strani ob obisku korenske poti
    return render_template('index2.html')


@app.route('/toggle/<state>/<time>/<watts>')
def export_to_list(state, time, watts):
    # Funkcija za upravljanje stanja luči (vklop/izklop) in shranjevanje podatkov o porabi
    global total_Wh

    if state == 'on':
        image_file = 'light_on.png'
    else:
        if time != "0":
            current_time = datetime.now()  # Zajem trenutnega datuma in časa
            watt_hours = (int(time) / 3600) * int(watts)  # Izračun vatnih ur
            consumption_data.append({
                "time": int(time),
                "watts": int(watts),
                "watt-hours": watt_hours,
                "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S")  # Formatiranje časovnega žiga
            })
            total_Wh += watt_hours  # Dodajanje k skupnim vatnim uram
            print_consumption_data()  # Izpis podatkov o porabi
            save_to_csv()

        image_file = 'light_off.png'
    return jsonify({'image': url_for('static', filename=image_file), 'state': 'off' if state == 'on' else 'on'})


@app.route('/get_consumption_data')
def get_consumption_data():
    # Funkcija za vračanje trenutnih podatkov o porabi preko API-ja za prikaz na front-endu
    global total_Wh
    return jsonify({'data': consumption_data, 'total_Wh': total_Wh})


@app.route('/delete_entry/<int:index>', methods=['POST'])
def delete_entry(index):
    # Funkcija za brisanje vnosa iz seznama porabe in posodobitev CSV datoteke
    global consumption_data, total_Wh
    try:
        removed_entry = consumption_data.pop(index)  # Brisanje vnosa
        total_Wh -= removed_entry['watt-hours']  # Prilagoditev skupnih vatnih ur
        save_to_csv()  # Shranjevanje posodobljenega seznama v CSV
        return jsonify({'success': True, 'total_Wh': total_Wh})
    except IndexError:
        return jsonify({'success': False, 'error': 'Index out of range'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# GLAVNI DEL
# ------------------------------------------------
if __name__ == '__main__':
    load_from_csv()  # Nalaganje obstoječih vnosov iz CSV datoteke ob zagonu aplikacije
    recalculate_total_Wh()  # Ponovni izračun skupnih vatnih ur
    app.run(debug=True)  # Zagon Flask aplikacije v načinu za razhroščevanje
