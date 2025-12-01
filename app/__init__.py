from flask import Flask
from .routes import bp

def create_app():
    app = Flask(__name__)
    
    # Restore essential configuration
    app.config['SECRET_KEY'] = 'dev-key-change-me'  # Use env var/strong key in prod
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Register blueprint
    app.register_blueprint(bp)

    # teardown: close db
    from .db import close_db
    app.teardown_appcontext(close_db)

    return app
