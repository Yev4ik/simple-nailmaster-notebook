import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from models import db, User
from datetime import datetime, timezone


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-fallback-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please sign in first'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.clients import clients_bp
    from routes.appointments import appointments_bp
    from routes.finance import finance_bp
    from routes.checklists import checklists_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(finance_bp)
    app.register_blueprint(checklists_bp)

    @app.route('/')
    def index():
        return redirect(url_for('dashboard.dashboard'))

    # Make current year available in all templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.now(timezone.utc)}

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
