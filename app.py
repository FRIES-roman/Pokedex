from flask import Flask, render_template, request, redirect, url_for, flash, session
from data_uzivatele import uzivatele

app = Flask(__name__)
app.secret_key = "super_tajny_klic"

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

# 5. Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Hledání uživatele (funguje pro přezdívku i e-mail)
        user = next(
            (u for u in uzivatele if (u.nickname == username or u.email == username) and u.heslo == password),
            None
        )

        if user:
            session["user_id"] = user.id
            session["user_name"] = user.cele_jmeno()
            flash(f"Vítejte zpět, {user.nickname}!", "success")
            return redirect(url_for("profil"))
        else:
            flash("Nesprávné jméno nebo heslo.", "danger")

    return render_template("auth/login.html")

# 6. Profil a správa účtů pro admina
@app.route("/profil")
def profil():
    user_id = session.get("user_id")
    if not user_id:
        flash("Pro zobrazení profilu se musíte přihlásit.", "warning")
        return redirect(url_for("login"))

    aktualni_uzivatel = next((u for u in uzivatele if u.id == user_id), None)
    if not aktualni_uzivatel:
        session.clear()
        return redirect(url_for("login"))

    # Pokud je uživatel admin, pošleme do šablony všechny účty, jinak prázdný seznam
    vsechny_ucty = uzivatele if aktualni_uzivatel.role == "admin" else []

    return render_template("auth/profil.html", uzivatel=aktualni_uzivatel, vsechny_ucty=vsechny_ucty)

# 7. Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("Byli jste odhlášeni.", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)