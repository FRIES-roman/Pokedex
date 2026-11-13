from flask import Flask, render_template, request, redirect, url_for, session
from data_uzivatele import uzivatele

app = Flask(__name__)
app.secret_key = "tajny_klic_pokedex"  # Nutné pro ukládání přihlášení (session)

# Testovací data pro Katalog a Typy
POKEMON_DATA = [
    {
        "id": 25,
        "name": "Pikachu",
        "type": "Electric",
        "description": "Kultovní elektrický Pokémon. Ukládá elektřinu ve svých tvářích.",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png"
    },
    {
        "id": 137,
        "name": "Porygon",
        "type": "Normal / Tech",
        "description": "Zcela syntetický Pokémon vytvořený z programového kódu.",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/137.png"
    },
    {
        "id": 479,
        "name": "Rotom",
        "type": "Electric / Ghost",
        "description": "Dokáže vstupovat do elektronických zařízení a ovládat je.",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/479.png"
    }
]

# 1. Domů
@app.route("/")
def home():
    return render_template("index.html")

# 2. Katalog
@app.route("/katalog")
def katalog():
    return render_template("katalog.html", pokemons=POKEMON_DATA)

# 3. Typy
@app.route("/typy")
def typy():
    return render_template("typy.html")

# 4. O aplikaci
@app.route("/o-aplikaci")
def about():
    return render_template("about.html")

# 5. Login (povoluje GET pro zobrazení i POST pro odeslání formuláře)
@app.route("/login", methods=["GET", "POST"])
def login():
    chyba = None
    if request.method == "POST":
        zadane_jmeno = request.form.get("username")
        zadane_heslo = request.form.get("password")

        for u in uzivatele:
            if (u.email == zadane_jmeno or u.nickname == zadane_jmeno) and u.heslo == zadane_heslo:
                session["user_id"] = u.id
                return redirect(url_for("profil"))

        chyba = "Špatné uživatelské jméno/e-mail nebo heslo!"

    return render_template("auth/login.html", chyba=chyba)

# 6. Profil přihlášeného uživatele
@app.route("/profil")
def profil():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    aktualni_uzivatel = next((u for u in uzivatele if u.id == user_id), None)
    return render_template("auth/profil.html", uzivatel=aktualni_uzivatel)

# 7. Odhlášení
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)