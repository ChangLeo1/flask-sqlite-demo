from flask import Blueprint, render_template, request, redirect, url_for, g
from .db import get_db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    db = get_db()
    items = db.execute('SELECT id, name FROM item').fetchall()
    return render_template('index.html', items=items)

@bp.route('/add', methods=['POST'])
def add():
    db = get_db()
    name = request.form['name']
    db.execute('INSERT INTO item (name) VALUES (?)', (name,))
    db.commit()
    return redirect(url_for('main.index'))


