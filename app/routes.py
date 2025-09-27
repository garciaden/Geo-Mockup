from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    
    
    return render_template("index.html", title="Home")


@app.route('/projects')
def projects():
    projects = [
        {"title": "Tephra Analysis", "owner": "Matthew Kenner", "status": "Ongoing"},
        {"title": "Sediment Study", "owner": "Ian Keitlan", "status": "Completed"},
        {"title": "Volcanic Glass Imaging", "owner": "Killian Bertsch", "status": "In Review"},
        {"title": "Lake Sample Processing", "owner": "Carlos Cortes Garcia", "status": "Completed"}
    ]
    return render_template("projects.html", title="Home", projects=projects)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Welcome, {}!'.format(form.username.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)