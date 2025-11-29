from flask import Flask, render_template
from app import db
from app.routes import bp
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    @app.teardown_appcontext
    def close_db_context(exception=None):
        db.close_db(exception)

    app.register_blueprint(bp)
    return app

app = create_app()

@app.cli.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    db.init_db()
    print('Initialized the database.')

@app.cli.command('sample-data')
def sample_data_command():
    """Insert sample data into the database."""
    db.insert_sample_data()
    print('Inserted sample data.')

if __name__ == '__main__':
    app.run(debug=True)


