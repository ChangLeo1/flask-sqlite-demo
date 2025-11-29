import sqlite3
from flask import g
import os

DATABASE = os.path.join(os.path.dirname(__file__), '..', 'app.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def close_db(e=None):
    db = g.pop('_database', None)
    if db is not None:
        db.close()

def init_db():
    db = sqlite3.connect(DATABASE)
    with open(os.path.join(os.path.dirname(__file__), 'schema.sql')) as f:
        db.executescript(f.read())
    db.close()

def insert_sample_data():
    db = sqlite3.connect(DATABASE)
    db.execute('INSERT INTO item (name) VALUES ("Sample Item 1")')
    db.execute('INSERT INTO item (name) VALUES ("Sample Item 2")')
    db.commit()
    db.close()


