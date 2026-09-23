from app import create_app
from app.extensions import db
import sqlite3

app = create_app()

with app.app_context():
    print("SQLAlchemy Database URI:")
    print(db.engine.url)

    db_path = db.engine.url.database
    print("\nActual database file:")
    print(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    print("\nTables:")
    for table in cursor.fetchall():
        print(table[0])

    conn.close()