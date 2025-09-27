# Copilot Instructions for AI Agents

## Project Overview
- This is a minimal Flask web application structured for clarity and Docker-based development.
- Main entrypoint: `myapp.py` (runs the app via `from app import app`).
- Application code is in the `app/` package:
  - `__init__.py`: Initializes the Flask app and imports routes.
  - `routes.py`: Defines HTTP routes (currently only `/` and `/index`).
  - `templates/`: Reserved for Jinja2 templates (currently empty `index.html`).

## Key Workflows
- **Run locally:** `python myapp.py` (runs Flask with debug on, port 5000).
- **Run in Docker:** Build and run using the provided `Dockerfile`. The default CMD uses `flask --app myapp.py run`.
- **Dependencies:** Managed via `requirements.txt` (Flask, Jinja2, python-dotenv).
- **Environment variables:** Can be managed with `python-dotenv` if `.env` is added (not present by default).

## Patterns & Conventions
- All routes are defined in `app/routes.py` and registered via import in `app/__init__.py`.
- The Flask app instance is always imported from `app`.
- Templates should be placed in `app/templates/` and rendered using Flask's `render_template` (not yet used in current code).
- Use `debug=True` for local development; Docker CMD does not set debug by default.
- The project is designed for a single service (no blueprints or API modules yet).

## Docker & Deployment
- Dockerfile uses a non-root user (`devuser`) for security.
- Exposes port 5000; Flask runs on `0.0.0.0` for container access.
- Requirements are installed before copying the full app for better Docker caching.

## Extending the Project
- Add new routes in `app/routes.py`.
- Add templates in `app/templates/` and use `render_template` in route handlers.
- For environment config, add a `.env` file and use `python-dotenv`.
- To add tests, create a `tests/` directory (not present yet) and use `pytest` or similar.

## Examples
- To add a new route:
  ```python
  @app.route('/hello')
  def hello():
      return "Hello from /hello!"
  ```
- To render a template:
  ```python
  from flask import render_template
  @app.route('/page')
  def page():
      return render_template('page.html')
  ```

---

**No project-specific agent rules or conventions were found in the workspace.**
If you add a `README.md` or `.github/copilot-instructions.md`, merge and update this file accordingly.
