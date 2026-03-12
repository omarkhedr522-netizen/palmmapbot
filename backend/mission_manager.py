import sqlite3
from datetime import datetime

DB_PATH = "data/palms.db"


class MissionManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_mission(self, mission_name, area_name=None, notes=None):
        """
        Create a new mission and return its mission_id.
        """
        conn = self.connect()
        cursor = conn.cursor()

        start_time = datetime.now().isoformat()

        cursor.execute("""
            INSERT INTO missions (mission_name, start_time, area_name, notes)
            VALUES (?, ?, ?, ?)
        """, (mission_name, start_time, area_name, notes))

        mission_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return mission_id

    def end_mission(self, mission_id):
        """
        Set the end time of a mission.
        """
        conn = self.connect()
        cursor = conn.cursor()

        end_time = datetime.now().isoformat()

        cursor.execute("""
            UPDATE missions
            SET end_time = ?
            WHERE mission_id = ?
        """, (end_time, mission_id))

        conn.commit()
        conn.close()

    def get_mission(self, mission_id):
        """
        Return one mission by ID.
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT mission_id, mission_name, start_time, end_time, area_name, notes
            FROM missions
            WHERE mission_id = ?
        """, (mission_id,))

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return {
            "mission_id": row[0],
            "mission_name": row[1],
            "start_time": row[2],
            "end_time": row[3],
            "area_name": row[4],
            "notes": row[5]
        }