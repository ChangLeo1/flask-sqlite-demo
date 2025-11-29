# Flask SQLite Minimal Demo

This is a minimal, working project using Flask and SQLite.

## Structure

```
app/
    __init__.py
    db.py
    routes.py
    schema.sql
    templates/
        index.html
run.py
requirements.txt
README.md
```

## Setup Instructions

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Initialize the database:**

```bash
flask --app run.py init-db
```

3. **Insert sample data:**

```bash
flask --app run.py sample-data
```

4. **Run the app:**

```bash
flask --app run.py run
```

App will be available at http://127.0.0.1:5000/ .

---

- You can add more items via the form on the main page.
- Database file: `app.db` (created at project root).


