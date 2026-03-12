import sqlite3
import json
import os

DB_PATH = "data/palms.db"
OUTPUT_PATH = "output/palm_trees.geojson"


def load_trees():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT tree_id, latitude, longitude, status, first_seen, last_seen
        FROM trees
        WHERE latitude IS NOT NULL AND longitude IS NOT NULL
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def build_geojson(trees):
    features = []

    for tree_id, latitude, longitude, status, first_seen, last_seen in trees:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [longitude, latitude]
            },
            "properties": {
                "tree_id": tree_id,
                "status": status,
                "first_seen": first_seen,
                "last_seen": last_seen
            }
        }
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return geojson


def export_geojson():
    trees = load_trees()

    if not trees:
        print("No trees found in database.")
        return

    geojson_data = build_geojson(trees)

    os.makedirs("output", exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(geojson_data, f, indent=2)

    print(f"GeoJSON exported successfully: {OUTPUT_PATH}")


if __name__ == "__main__":
    export_geojson()
