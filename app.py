from flask import Flask, render_template, abort

app = Flask(__name__)

# --- Baza danych (lista słowników) --- tym czsowa baza danych
PRODUKTY = [
    {"id": 1, "nazwa": "Kort Centralny", "cena": 100.0, "dostepny": True},
    {"id": 2, "nazwa": "Kort 2 Trawa", "cena": 80.0, "dostepny": False},
    {"id": 3, "nazwa": "Kort 3 Hard Court", "cena": 90.0, "dostepny": True},
]


# --- Strona główna ---
@app.route("/")
def index():
    return render_template("index.html") #pobieera plik HTML z folderu templates i uzupewnia go danymi z pythona


# --- ZADANIE 2: Lista produktów ---
@app.route("/produkty")
def produkty():
    # Передаем весь список PRODUKTY в шаблон produkty.html
    return render_template("produkty.html", produkty=PRODUKTY)


# --- ZADANIE 3: Szczegóły elementu (ID) ---
@app.route("/produkt/<int:id>")
def produkt(id):
    znaleziony_produkt = None
    
    # Ищем продукт с нужным ID простым циклом for
    for p in PRODUKTY: # pętla przecodzi pokoleji przez każdy słownik
        if p["id"] == id: # sprawdza czy id zgadza sie z podanym w adresem URL
            znaleziony_produkt = p # jeśli zgadza sie id to zapisujemy cały słowik tego produktu do zmoennej

    # Если продукт с таким ID не найден — выдаем ошибку 404
    if znaleziony_produkt is None:
        abort(404)

    # Передаем найденный элемент в шаблон szczegoly.html
    return render_template("szczegoly.html", produkt=znaleziony_produkt)


if __name__ == "__main__":
    app.run(debug=True)