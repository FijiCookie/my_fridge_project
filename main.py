import py as py
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import json
import daten
from datetime import datetime
from collections import defaultdict


#test
# import plotly.express as px
# import pandas as pd

app = Flask("My_Fridge")


# daten_lebensmittel = 'daten.json'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        kategorie = request.form['kategorie']
        mhd = request.form['mhd']
        bewertung = int(request.form['bewertung'])
        daten.speichern(name, kategorie, mhd, bewertung)

        eintrag_gespeichert = "Du hast ein Lebensmittel in den Kühlschrank hinzugefügt. Willst du mehr hinzufügen?."

        return render_template('index.html', eintrag=eintrag_gespeichert)

    return render_template('index.html')


# Hat fast funktioniert!!
# @app.route('/statistik', methods=['GET', 'POST'])
# def ausgabe():
#     eingabe = daten.eingabe_laden()  # holt Daten aus daten.py
#     filter_liste = []
#     filter_value = ""
#     filter_key = ""
#     gefiltert = False
#
#     if request.method == 'POST':
#         gefiltert = True
#         mhd = request.form['mhd']
#
#         if mhd != "":
#             filter_value = mhd
#             filter_key = "MHD"
#
#         for key, eintrag in eingabe.items():
#             if eintrag[filter_key] == filter_value:
#                 filter_liste.append(eintrag)
#
#     # Daten sortieren nach dem aktuellen Datum
#     eingabe_sortiert = dict(sorted(eingabe.items(), key=lambda x: datetime.strptime(x[1]['MHD'], '%d-%m-%y')))
#
#     return render_template('statistik.html', eintraege=eingabe_sortiert, gefilterte_eintraege=filter_liste, ist_gefiltert=gefiltert)
def eingabe_laden():
    with open('ausgabe_dictonary.json', 'r') as file:
        daten = json.load(file)
    return daten

@app.route('/statistik', methods=['GET', 'POST'])
def ausgabe():
    eingabe = eingabe_laden()  # holt Daten aus JSON-Datei

    # Daten sortieren nach dem aktuellen Datum
    eingabe_sortiert = sorted(eingabe.items(), key=lambda x: datetime.strptime(x[1]['MHD'], '%d-%m-%y'))

    return render_template('statistik.html', eintraege=eingabe_sortiert)


# Versuch Lebensmittel in Kategorien anzuzeigen

# @app.route("/statistik/", methods=['GET'])
# def zahlenauswertung():
#     eingabe = daten.eingabe_laden()
#
#     kategorie_count = defaultdict(int)  # Ein leeres importiertes Wörterbuch zur Zählung der Kategorien
#
#     for lebensmittel in eingabe.values():
#         kategorie = lebensmittel['kategorie']
#         kategorie_count[kategorie] += 1
#
#     print(kategorie_count)
#     return render_template('statistik.html', kategorie_count=kategorie_count)





# @app.route('/loeschen/<name>')
# def loeschen(name):
#     try:
#         with open(daten_lebensmittel, 'r') as file:
#             daten = json.load(file)
#     except FileNotFoundError:
#         daten = {}
#
#     if name in daten:
#         del daten[name]
#
#         with open(daten_lebensmittel, 'w') as file:
#             json.dump(daten, file)
#
#     return redirect('/')

# Fehlerseiten bei ungültigem URl (Seite nicht gefunden)
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Interner Serverfehler URL
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

# @app.route('/visualisierung')
# def visualisierung():
#     try:
#         with open(daten_lebensmittel, 'r') as file:
#             daten = json.load(file)
#     except FileNotFoundError:
#         daten = {}
#
#     df = pd.DataFrame.from_dict(daten, orient='index', columns=['name', 'mhd', 'bewertung'])
#
#     fig = px.bar(df, x='name', y='bewertung')
#
#     fig.write_html('statistik.html')
#
#     return render_template('statistik.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)