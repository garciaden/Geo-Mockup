from flask import render_template, redirect, url_for

from app.main import bp
from app.projects.routes import projects as project_catalog
from app.samples.routes import samples as sample_catalog, format_sample


@bp.route('/')
def index():
    projects_in_progress = [
        project for project in project_catalog if project.get("status") in {"Ongoing", "In Review"}
    ]
    active_workflow_states = {"In Progress", "Queued", "Pending", "In Review", "Draft", "Needs Review"}
    formatted_samples = [format_sample(sample) for sample in sample_catalog]

    active_workflows = sum(
        1
        for sample in sample_catalog
        for step in sample["workflow_status"]
        if step.get("state") in active_workflow_states
    )

    dashboard = {
        "projects_in_progress": len(projects_in_progress),
        "samples_registered": len(formatted_samples),
        "active_workflows": active_workflows,
        "recent_projects": projects_in_progress[:3],
        "recent_samples": formatted_samples[:3],
    }

    return render_template("main/index.html", title="Home", dashboard=dashboard)


@bp.route('/login')
def fake_login():
    return redirect(url_for('auth.login'))
