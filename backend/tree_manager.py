import sqlite3
import math
from datetime import datetime

DB_PATH = "data/palms.db"


class TreeManager:
    def __init__(self, db_path=DB_PATH, distance_threshold_m=2.0):
        self.db_path = db_path
        self.distance_threshold_m = distance_threshold_m

    def connect(self):
        return sqlite3.connect(self.db_path)

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate distance between two GPS points in meters.
        """
        r = 6371000  # Earth radius in meters

        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = (
            math.sin(delta_phi / 2) ** 2
            + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return r * c

    def generate_tree_id(self):
        """
        Generate a new tree ID like PALM-0001, PALM-0002, ...
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM trees")
        count = cursor.fetchone()[0]

        conn.close()

        return f"PALM-{count + 1:04d}"

    def find_existing_tree(self, latitude, longitude):
        """
        Find the nearest existing tree within the threshold distance.
        Returns tree row if found, otherwise None.
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, tree_id, latitude, longitude
            FROM trees
        """)

        trees = cursor.fetchall()
        conn.close()

        nearest_tree = None
        nearest_distance = float("inf")

        for tree in trees:
            tree_db_id, tree_id, tree_lat, tree_lon = tree
            distance = self.haversine_distance(latitude, longitude, tree_lat, tree_lon)

            if distance < self.distance_threshold_m and distance < nearest_distance:
                nearest_distance = distance
                nearest_tree = {
                    "id": tree_db_id,
                    "tree_id": tree_id,
                    "latitude": tree_lat,
                    "longitude": tree_lon,
                    "distance_m": distance
                }

        return nearest_tree

    def create_new_tree(self, latitude, longitude):
        """
        Create a new tree record.
        """
        tree_id = self.generate_tree_id()
        now = datetime.now().isoformat()

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO trees (tree_id, latitude, longitude, first_seen, last_seen)
            VALUES (?, ?, ?, ?, ?)
        """, (tree_id, latitude, longitude, now, now))

        conn.commit()
        conn.close()

        return tree_id

    def update_existing_tree(self, tree_id):
        """
        Update the last_seen timestamp of an existing tree.
        """
        now = datetime.now().isoformat()

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE trees
            SET last_seen = ?, updated_at = CURRENT_TIMESTAMP
            WHERE tree_id = ?
        """, (now, tree_id))

        conn.commit()
        conn.close()

    def add_detection(self, tree_id, latitude, longitude, mission_id=None, confidence=1.0):
        """
        Add a detection row linked to a tree.
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO detections (tree_id, mission_id, latitude, longitude, confidence)
            VALUES (?, ?, ?, ?, ?)
        """, (tree_id, mission_id, latitude, longitude, confidence))

        conn.commit()
        conn.close()

    def process_detection(self, latitude, longitude, mission_id=None, confidence=1.0):
        """
        Main logic:
        - if nearby tree exists -> use same tree_id
        - otherwise create new tree
        - always store detection
        """
        existing_tree = self.find_existing_tree(latitude, longitude)

        if existing_tree:
            tree_id = existing_tree["tree_id"]
            self.update_existing_tree(tree_id)
            self.add_detection(tree_id, latitude, longitude, mission_id, confidence)

            return {
                "action": "matched_existing_tree",
                "tree_id": tree_id,
                "distance_m": round(existing_tree["distance_m"], 3)
            }

        tree_id = self.create_new_tree(latitude, longitude)
        self.add_detection(tree_id, latitude, longitude, mission_id, confidence)

        return {
            "action": "created_new_tree",
            "tree_id": tree_id,
            "distance_m": None
        }