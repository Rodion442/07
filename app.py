from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

PRODUKTY = [
    {"id": 1, "nazwa": "Kort Centralny", "cena": 100.0, "dostepny": True},
    {"id": 2, "nazwa": "Kort 2 Trawa", "cena": 80.0, "dostepny": False},
    {"id": 3, "nazwa": "Kort 3 Hard Court", "cena": 90.0, "dostepny": True},
]


@app.route("/")
def index():
    return render_template("index.html")


# --- ZADANIE 2, 5 & 6: Lista + Dodawanie + Filtrowanie (Zadanie 6) ---
@app.route("/produkty", methods=["GET", "POST"])
def produkty():
    if request.method == "POST":
        nazwa = request.form.get("nazwa")
        cena = request.form.get("cena")
        dostepny = request.form.get("dostepny") == "on"

        nowe_id = PRODUKTY[-1]["id"] + 1 if PRODUKTY else 1

        PRODUKTY.append({
            "id": nowe_id,
            "nazwa": nazwa,
            "cena": float(cena),
            "dostepny": dostepny
        })
        return redirect(url_for("produkty"))

    # ZADANIE 6: Filtrowanie po nazwie (szukaj)
    szukana_fraza = request.args.get("szukaj", "").strip().lower()
    
    if szukana_fraza:
        # Filtrujemy listę produktów po wpisanym tekście
        przefiltrowane = [p for p in PRODUKTY if szukana_fraza in p["nazwa"].lower()]
    else:
        przefiltrowane = PRODUKTY

    return render_template("produkty.html", produkty=przefiltrowane, szukaj=szukana_fraza)


# --- ZADANIE 3: Szczegóły ---
@app.route("/produkt/<int:id>")
def produkt(id):
    znaleziony_produkt = None
    for p in PRODUKTY:
        if p["id"] == id:
            znaleziony_produkt = p

    if znaleziony_produkt is None:
        abort(404)

    return render_template("szczegoly.html", produkt=znaleziony_produkt)


# --- ZADANIE 7: Usuwanie elementu ---
@app.route("/produkt/usun/<int:id>", methods=["POST"])
def usun_produkt(id):
    global PRODUKTY
    # Tworzymy nową listę bez produktu o danym ID
    PRODUKTY = [p for p in PRODUKTY if p["id"] != id]
    return redirect(url_for("produkty"))


# --- ZADANIE 8: Edycja elementu ---
@app.route("/produkt/edytuj/<int:id>", methods=["GET", "POST"])
def edytuj_produkt(id):
    znaleziony_produkt = None
    for p in PRODUKTY:
        if p["id"] == id:
            znaleziony_produkt = p

    if znaleziony_produkt is None:
        abort(404)

    if request.method == "POST":
        # Aktualizujemy dane znalezionego produktu
        znaleziony_produkt["nazwa"] = request.form.get("nazwa")
        znaleziony_produkt["cena"] = float(request.form.get("cena"))
        znaleziony_produkt["dostepny"] = request.form.get("dostepny") == "on"
        
        return redirect(url_for("produkt", id=id))

    return render_template("edytuj.html", produkt=znaleziony_produkt)


if __name__ == "__main__":
    app.run(debug=True)