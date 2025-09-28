from flask import app, render_template
from app.projects import bp

@bp.route('/')
def project_list():
    projects = [
        {"title": "Tephra Analysis", "owner": "Matthew Kenner", "status": "Ongoing"},
        {"title": "Sediment Study", "owner": "Ian Keitlan", "status": "Completed"},
        {"title": "Volcanic Glass Imaging", "owner": "Killian Bertsch", "status": "In Review"},
        {"title": "Lake Sample Processing", "owner": "Carlos Cortes Garcia", "status": "Completed"}
    ]
    return render_template("projects/project_list.html", title="Projects", projects=projects)