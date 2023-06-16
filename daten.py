import json

# Diese Funktion speichert die eingegebenen Daten in einem Jason-File (Json-File wird geschrieben "w")
def speichern(name, kategorie, mhd, bewertung):
    datei = "ausgabe_dictonary.json"
    try:
        with open(datei) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {}

    datei_inhalt[name] = {'Name': name, #Hier wird ein Dictionary erstellt um die Kategorien und Werte festzuhalten
                          'Kategorie' : kategorie,
                          'MHD': mhd,
                          'Bewertung': bewertung}

    with open(datei, "w") as open_file:
        json.dump(datei_inhalt, open_file, indent=4)

# Funktion, um gespeicherte Daten (vom Json-File) wieder laden zu können
def eingabe_laden():
    datei_name = "ausgabe_dictonary.json"

    try:
        with open(datei_name) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {}

    return datei_inhalt

