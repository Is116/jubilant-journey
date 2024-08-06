from flask import Flask
from attendance_system.routes.main_routes import main_bp
from attendance_system.routes.user_routes import user_bp
from attendance_system.routes.attendance_routes import attendance_bp
from attendance_system.routes.fingerprint_routes import fingerprint_bp
from db_setup import init_sqlite_db  # Adjusted import

def create_app():
    app = Flask(__name__)

    # Initialize the SQLite database
    init_sqlite_db()

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(attendance_bp, url_prefix='/attendance')
    app.register_blueprint(fingerprint_bp, url_prefix='/fingerprint')

    return app
