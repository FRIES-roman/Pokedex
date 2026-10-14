from flask import Flask, render_template

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(debug=True)