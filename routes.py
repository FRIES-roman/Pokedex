from flask import render_template, request, session, redirect, url_for
from models import auth_bp
from data_uzivatele import uzivatele
from auth_service import AuthService

auth = AuthService(uzivatele)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    chyba = None

    if request.method == 'POST':
        # V HTML šabloně musí být atribut name="username"
        username = request.form.get("username")
        password = request.form.get("password")

        uzivatel = auth.prihlas(username, password)

        if uzivatel is not None:
            session.clear()
            session["uzivatel_id"] = uzivatel.id
            session["uzivatel_jmeno"] = uzivatel.jmeno
            session["uzivatel_prijmeni"] = uzivatel.prijmeni
            session["uzivatel_role"] = uzivatel.role


         return redirect(url_for("index"))

        chyba = "Nesprávný email nebo heslo"

    return render_template('login.html', chyba=chyba)

@auth_bp.route('/profil')
def profil():
    if session.get("uzivatel_id") is None:
        return redirect(url_for('login'))
