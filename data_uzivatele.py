from werkzeug.security import generate_password_hash
from models.user import User

uzivatele = [
    User(1, "Martin", "Kapcala", "martin@example.com", "Martin", generate_password_hash("heslo123"), "admin"),
    User(2, "Pepa", "Novák", "pepa@example.com", "Pepa", generate_password_hash("pepa123")),
    User(3, "Sandra", "Nadšená", "sandra@example.com", "Sandra", generate_password_hash("sandra123"))
]
