from flask import Blueprint, render_template, request, redirect, url_for, g
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
    name = request.form['name']
    db.execute('INSERT INTO item (name) VALUES (?)', (name,))
    db.commit()
    return redirect(url_for('main.index'))

@bp.route('/api/items')
def api_items():
    db = get_db()
    items = db.execute('SELECT id, name FROM item').fetchall()
    return {'items': [dict(item) for item in items]}

@bp.route('/upload-csv', methods=['POST'])
def upload_csv():
    file = request.files.get('file')

    # 1. 没选文件的情况
    if not file or file.filename == '':
        # 这里简单处理：返回首页，不插数据
        return redirect(url_for('main.index'))

    # 2. 读取 CSV 内容
    try:
        # 把上传的文件内容读出来，按 utf-8 解码为字符串
        stream = io.StringIO(file.stream.read().decode('utf-8', errors='ignore'))
        reader = csv.reader(stream)

        db = get_db()
        count = 0
        for row in reader:
            # 每一行是一个 list，比如 ["Item name"]
            if not row:
                continue
            name = row[0].strip()
            if not name:
                continue

            db.execute('INSERT INTO item (name) VALUES (?)', (name,))
            count += 1

        db.commit()
        print(f"Imported {count} items from CSV.")
    except Exception as e:
        # 简单打印错误，实际中可以更优雅一点
        print("Error importing CSV:", e)

    # 3. 导入完成后回到首页，页面会显示新数据
    return redirect(url_for('main.index'))



