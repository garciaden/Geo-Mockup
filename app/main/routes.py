from flask import app, render_template, redirect, url_for
from app.main import bp

@bp.route('/')
#@bp.route('/index')
def index():
        
    return render_template("main/index.html", title="Home")

@bp.route('/login')
def fake_login():
    return redirect(url_for('auth.login'))

