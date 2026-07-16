import sqlite3

DATABASE = "database.db"


def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        temperature REAL,
        humidity REAL,
        battery REAL,
        prediction TEXT
    )
    """)

    cursor.execute("PRAGMA table_info(history)")
    columns = [row[1] for row in cursor.fetchall()]

    if "device_id" not in columns:
        cursor.execute("ALTER TABLE history ADD COLUMN device_id TEXT")

    conn.commit()
    conn.close()


def insert_history(device_id, temperature, humidity, battery, prediction):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO history
    (device_id, temperature, humidity, battery, prediction)
    VALUES (?,?,?,?,?)
    """, (device_id, temperature, humidity, battery, prediction))

    conn.commit()
    conn.close()


def get_history():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT id, device_id, temperature, humidity, battery, prediction FROM history ORDER BY id DESC")

    rows = cursor.fetchall()

    conn.close()

    return rows


def delete_history(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM history WHERE id=?", (id,))

    conn.commit()
    conn.close()