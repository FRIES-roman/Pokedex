from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from data_uzivatele import uzivatele

app = Flask(__name__)
app.secret_key = "super_tajny_klic"

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
        "description": "Zcela syntetický Pokémon vytvoýený z programového kódu.",
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


# 5. Přihlášení
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = next(
            (u for u in uzivatele if (u.nickname == username or u.email == username) and u.heslo == password),
            None
        )

        if user:
            session["user_id"] = user.id
            session["user_name"] = user.cele_jmeno()
            session["user_role"] = user.role
            flash(f"Vítejte zpět, {user.nickname}!", "success")
            return redirect(url_for("profil"))
        else:
            flash("Nesprávné jméno nebo heslo.", "danger")

    return render_template("auth/login.html")


# 6. Profil uživatele
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

    return render_template("auth/profil.html", uzivatel=aktualni_uzivatel)


# 7. Administrace – seznam uživatelských účtů (jen pro admina, jinak chyba 403)
@app.route("/admin")
def admin():
    if session.get("user_id") is None:
        return redirect(url_for("login"))

    if session.get("user_role") != "admin":
        abort(403)

    return render_template("admin.html", uzivatele=uzivatele)


# 8. Odhlášení
@app.route("/logout")
def logout():
    session.clear()
    flash("Byli jste odhlášeni.", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)