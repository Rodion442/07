from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

# --- Baza danych (lista słowników) ---
PRODUKTY = [
    {"id": 1, "nazwa": "Kort Centralny", "cena": 100.0, "dostepny": True},
    {"id": 2, "nazwa": "Kort 2 Trawa", "cena": 80.0, "dostepny": False},
    {"id": 3, "nazwa": "Kort 3 Hard Court", "cena": 90.0, "dostepny": True},
]


# --- Zadanie 1: Strona główna ---
@app.route("/")
def index():
    nazwa_projektu = "System Rezerwacji Kortów"
    autor = "Rodion"
    return render_template("index.html", projekt=nazwa_projektu, imie=autor)


# --- Zadanie 2, 5: Lista produktów ---
@app.route("/produkty")
def produkty():
    return render_template("produkty.html", produkty=PRODUKTY)


# --- Zadanie 3: Szczegóły elementu ---
@app.route("/produkt/<int:id>")
def produkt(id):
    znaleziony_produkt = None
    
    for p in PRODUKTY:
        if p["id"] == id:
            znaleziony_produkt = p

    if znaleziony_produkt is None:
        abort(404)

    return render_template("szczegoly.html", produkt=znaleziony_produkt)


# --- Zadanie 6: Wyszukiwarka (GET) ---
@app.route("/szukaj")
def szukaj():
    zapytanie = request.args.get("q", "")
    
    wyniki = []
    zapytanie_low = zapytanie.lower()

    for p in PRODUKTY:
        nazwa_low = p["nazwa"].lower()
        if zapytanie_low in nazwa_low:
            wyniki.append(p)

    return render_template("szukaj.html", q=zapytanie, wyniki=wyniki)


# --- Zadanie 7: Dodawanie elementu (POST) ---
@app.route("/dodaj", methods=["GET", "POST"])
def dodaj():
    if request.method == "POST":
        nowe_id = len(PRODUKTY) + 1
        nowa_nazwa = request.form["nazwa"]
        nowa_cena = float(request.form["cena"])
        
        nowy_element = {
            "id": nowe_id,
            "nazwa": nowa_nazwa,
            "cena": nowa_cena,
            "dostepny": True
        }
        
        PRODUKTY.append(nowy_element)
        return redirect(url_for("produkty"))

    return render_template("dodaj.html")


if __name__ == "__main__":
    app.run(debug=True)