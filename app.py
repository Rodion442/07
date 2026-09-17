from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

# --- Baza danych (lista słowników) ---
PRODUKTY = [
    {"id": 1, "nazwa": "Kort Centralny", "cena": 100.0, "dostepny": True},
    {"id": 2, "nazwa": "Kort 2 Trawa", "cena": 80.0, "dostepny": False},
    {"id": 3, "nazwa": "Kort 3 Hard Court", "cena": 90.0, "dostepny": True},
]


@app.route("/")
def index():
    return render_template("index.html")


# --- ZADANIE 2 & 5: Lista + Dodawanie nowego elementu ---
# Obsługujemy zarówno pobieranie strony (GET), jak i wysyłanie formularza (POST)
@app.route("/produkty", methods=["GET", "POST"])
def produkty():
    # Sprawdzamy, czy użytkownik wysłał formularz metodą POST
    if request.method == "POST":
        # Pobieramy wartość z pola <input name="nazwa">
        nazwa = request.form.get("nazwa")
        
        # Pobieramy wartość z pola <input name="cena">
        cena = request.form.get("cena")
        
        # Sprawdzamy czy checkbox był zaznaczony (zwraca True jeśli zaznaczony)
        dostepny = request.form.get("dostepny") == "on"

        # Generujemy nowe ID: bierzemy ID ostatniego elementu i dodajemy 1
        nowe_id = PRODUKTY[-1]["id"] + 1 if PRODUKTY else 1

        # Tworzymy nowy słownik i dodajemy go do naszej bazy danych (listy)
        PRODUKTY.append({
            "id": nowe_id,
            "nazwa": nazwa,
            "cena": float(cena), # Konwertujemy tekst na liczbę zmiennoprzecinkową
            "dostepny": dostepny
        })

        # Przekierowujemy użytkownika z powrotem na listę produktów (odświeżenie strony)
        return redirect(url_for("produkty"))

    # Jeśli to zwykłe wejście na stronę (GET), po prostu wyświetlamy szablon
    return render_template("produkty.html", produkty=PRODUKTY)


# --- ZADANIE 3: Szczegóły elementu (ID) ---
@app.route("/produkt/<int:id>")
def produkt(id):
    znaleziony_produkt = None
    
    # Przechodzimy po wszystkich produktach w poszukiwaniu właściwego ID
    for p in PRODUKTY:
        if p["id"] == id:
            znaleziony_produkt = p

    # Jeśli nie znaleziono produktu o danym ID, zwracamy błąd 404
    if znaleziony_produkt is None:
        abort(404)

    return render_template("szczegoly.html", produkt=znaleziony_produkt)


if __name__ == "__main__":
    app.run(debug=True)