from flask import Blueprint, render_template, request, redirect, url_for, g, flash, current_app
from .db import get_db
import csv
import io

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    db = get_db()
    items = db.execute('SELECT id, name FROM item').fetchall()
    return render_template('index.html', items=items)

@bp.route('/add', methods=['POST'])
def add():
    db = get_db()
    name = request.form.get('name', '').strip()
    if not name:
        flash("Item name cannot be empty!", "warning")
        return redirect(url_for('main.index'))
    db.execute('INSERT INTO item (name) VALUES (?)', (name,))
    db.commit()
    return redirect(url_for('main.index'))

@bp.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    db = get_db()
    db.execute('DELETE FROM item WHERE id = ?', (item_id,))
    db.commit()
    flash("Item deleted.", "success")
    return redirect(url_for('main.index'))

@bp.route('/api/items')
def api_items():
    db = get_db()
    items = db.execute('SELECT id, name FROM item').fetchall()
    return {'items': [dict(item) for item in items]}

@bp.route('/upload-csv', methods=['POST'])
def upload_csv():
    file = request.files.get('file')
    if not file or file.filename == '':
        flash('No selected file for CSV import.', 'warning')
        return redirect(url_for('main.index'))
    if not file.filename.lower().endswith('.csv'):
        flash('Please upload a CSV file.', 'danger')
        return redirect(url_for('main.index'))
    try:
        stream = io.StringIO(file.stream.read().decode('utf-8', errors='ignore'))
        reader = csv.reader(stream)
        db = get_db()
        count = 0
        for row in reader:
            if not row:
                continue
            name = row[0].strip()
            if not name:
                continue
            db.execute('INSERT INTO item (name) VALUES (?)', (name,))
            count += 1
        db.commit()
        flash(f"Imported {count} items from CSV.", "success")
        current_app.logger.info(f"CSV import: {count} items from {file.filename}")
    except Exception as e:
        flash("Error importing CSV: " + str(e), "danger")
        current_app.logger.error(f"CSV import error: {e}")
    return redirect(url_for('main.index'))



