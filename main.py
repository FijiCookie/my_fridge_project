import py as py
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import json


#test
# import plotly.express as px
# import pandas as pd

app = Flask("My_Fridge")


daten_lebensmittel = 'daten.json'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        mhd = request.form['mhd']
        bewertung = int(request.form['bewertung'])
        lebensmittel = {'name': name, 'mhd': mhd, 'bewertung': bewertung}

        try:
            with open(daten_lebensmittel, 'r') as file:
                daten = json.load(file)
        except FileNotFoundError:
            daten = {}

        daten[name] = lebensmittel

        with open(daten_lebensmittel, 'w') as file:
            json.dump(daten, file)

        return render_template('index.html')
    return render_template('index.html')

@app.route('/loeschen/<name>')
def loeschen(name):
    try:
        with open(daten_lebensmittel, 'r') as file:
            daten = json.load(file)
    except FileNotFoundError:
        daten = {}

    if name in daten:
        del daten[name]

        with open(daten_lebensmittel, 'w') as file:
            json.dump(daten, file)

    return redirect('/')

@app.route('/visualisierung')
def visualisierung():
    try:
        with open(daten_lebensmittel, 'r') as file:
            daten = json.load(file)
    except FileNotFoundError:
        daten = {}

    df = pd.DataFrame.from_dict(daten, orient='index', columns=['name', 'mhd', 'bewertung'])

    fig = px.bar(df, x='name', y='bewertung')

    fig.write_html('statistik.html')

    return render_template('statistik.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)