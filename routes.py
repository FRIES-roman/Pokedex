from flask import render_template
from models import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login()
    return render_template('login.html')