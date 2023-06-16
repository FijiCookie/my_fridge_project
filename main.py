from flask import Flask, render_template, request
import json
import daten
import datetime

"""
Diese Webapplikation wurde anhand verschiedene Tutorials, Dokumentationen & YouTube-Videos erstellt. 
Hierbei handelte es sich hauptsächlich um W3Schools, DelftStack, geeksforgeeks, Bootstrap Dokumentation, Jinja Dokumentation, Python Dokumentationen wie zum Beispiel über datetime. 
Zudem orientierte sich die Autorin an ähnlichen Projekte auf Github und den Vorlesungen von den Modulen Programmieren 1 und 2. Nebst dem Tutoring von einem Vorganggenprojekt, welches  hier auch angewendet werden konnte, hatte die Autorin die Möglichkeit kleines Tutoring von zwei Studenten (N. Steiger & S. Kienberger), welche das Modul schon absolvierten, zu erhalten.
"""

app = Flask("My_Fridge")

@app.route('/', methods=['GET', 'POST']) #Die Startseite wird hier erstellt in Form von einem Formular.
def index(): #Durch die Definition index, werden die Daten den jeweiligen Übertitel zugeordnet.
    if request.method == 'POST': #passiert nur mit dem Button senden
        name = request.form['name']
        kategorie = request.form['kategorie']
        mhd = request.form['mhd']
        bewertung = int(request.form['bewertung'])
        daten.speichern(name, kategorie, mhd, bewertung) #Hier werden die eingegeben Daten gespeichert.

        eintrag_gespeichert = "Supper, du hast ein Lebensmittel in My Fridge hinzugefügt. Willst noch du mehr hinzufügen?."

        return render_template('index.html', eintrag=eintrag_gespeichert) #Das Formular wird gerendert und falls etwas eingegeben wird es gesendet/gespeichert. Die Funktion dazu befindet sich in daten.py.

    return render_template('index.html')


def eingabe_laden(): #In dieser Funktion werden die Daten aus der Json Datei geladen
    with open('ausgabe_dictonary.json', 'r') as file:
        daten = json.load(file)
    return daten

@app.route('/statistik', methods=['GET', 'POST']) #Hier werden die Daten vorbereitet für die Listen Ausgabe im statistik.html
def ausgabe():
    abgelaufen_liste = abgelaufen() #speichert das Ergebnis von abgelaufen in der 'abgelaufen-liste' Variabel
    eingabe = eingabe_laden()  # ruft eingabe_laden aus daten.py auf uns speichert es in der eingabe variabel

    eingabe_sortiert = sorted(eingabe.items(), key=lambda x: datetime.datetime.strptime(x[1]['MHD'], '%d-%m-%y'))# Daten sortieren nach dem aktuellen Datum

    return render_template('statistik.html', eintraege=eingabe_sortiert, abgelaufen=abgelaufen_liste)

def abgelaufen(): #Hier wird die Datenverarbeitung rund ums MHD vorgenommen. Um das Modul datetime richtig anzuwenden, wurden verschiedene Quellen benutz zum einen https://www.programiz.com/python-programming/datetime, die Dokumentation von Python und schlussendlich mit Nicolas Steiger angeschaut.
    heute = datetime.date.today() #mit datetime.date.today
    with open('ausgabe_dictonary.json', 'r') as file: #Die Json Datei wird geöffnet
        daten = json.load(file) #Die Daten der Datei werden in das 'daten'-Dictionary geladen

    abgelaufen_liste = []
    for element in daten.values(): #jedes element (also jedes Lebensmittel) wird bei den Daten durchlaufen
        mhd = datetime.datetime.strptime(element['MHD'], '%d-%m-%y').date() #Das MHD Datum wird hier in ein Daytime Opjekt verwandelt, sodas es rechnen kann.
        abgelaufen_seit = (heute - mhd).days #Hier wird berechnet wieviel Tage es her sind, seit das Lebensmittel abgelaufen ist.
        element['abgelaufen_seit'] = abgelaufen_seit  # Das 'abelaufen-seit' Feld wird dem 'element' Dictionary hinzugefüt.
        if mhd < heute: #Ist das MHD von der Vergangenheit? Wenn ja wird es dem 'element'-Dictionary hinzugefügt
            abgelaufen_liste.append(element)

    return abgelaufen_liste

@app.errorhandler(404) #Bei einer nichtvorhandener URL Abfrage,wird hier das 404.html gerendert
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__": #Startet die Flask Anwendung
    app.run(debug=True, port=5000)