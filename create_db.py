import sqlite3
import os

# Make sure data folder exists
os.makedirs("data", exist_ok=True)

DB_PATH = os.path.join("data", "palms.db")

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Missions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS missions (
        mission_id INTEGER PRIMARY KEY AUTOINCREMENT,
        mission_name TEXT NOT NULL,
        start_time TEXT,
        end_time TEXT,
        area_name TEXT,
        notes TEXT
    )
    """)

    # Trees table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tree_id TEXT UNIQUE NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        status TEXT DEFAULT 'active',
        first_seen TEXT,
        last_seen TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Detections table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detections (
        detection_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tree_id TEXT NOT NULL,
        mission_id INTEGER,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        detection_flag INTEGER NOT NULL DEFAULT 1,
        confidence REAL,
        detected_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (tree_id) REFERENCES trees(tree_id),
        FOREIGN KEY (mission_id) REFERENCES missions(mission_id)
    )
    """)

    conn.commit()
    conn.close()

    print(f"Database created successfully at: {DB_PATH}")
    print("Tables created: missions, trees, detections")


if __name__ == "__main__":
    create_database()