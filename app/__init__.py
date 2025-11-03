from flask import Flask

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.projects import bp as projects_bp
    app.register_blueprint(projects_bp, url_prefix='/project')

    from app.samples import bp as samples_bp
    app.register_blueprint(samples_bp, url_prefix='/samples')

    return app
