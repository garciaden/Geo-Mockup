from flask import app, render_template
from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    
    
    return render_template("main/index.html", title="Home")


@bp.route('/projects')
def projects():
    projects = [
        {"title": "Tephra Analysis", "owner": "Matthew Kenner", "status": "Ongoing"},
        {"title": "Sediment Study", "owner": "Ian Keitlan", "status": "Completed"},
        {"title": "Volcanic Glass Imaging", "owner": "Killian Bertsch", "status": "In Review"},
        {"title": "Lake Sample Processing", "owner": "Carlos Cortes Garcia", "status": "Completed"}
    ]
    return render_template("main/projects.html", title="Home", projects=projects)