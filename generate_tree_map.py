import sqlite3
import folium
import os

DB_PATH = "data/palms.db"
OUTPUT_PATH = "output/palm_tree_map.html"


def load_trees():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT tree_id, latitude, longitude, first_seen, last_seen
        FROM trees
        WHERE latitude IS NOT NULL AND longitude IS NOT NULL
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def generate_map():
    trees = load_trees()

    if not trees:
        print("No trees found in database.")
        return

    avg_lat = sum(row[1] for row in trees) / len(trees)
    avg_lon = sum(row[2] for row in trees) / len(trees)

    palm_map = folium.Map(location=[avg_lat, avg_lon], zoom_start=18)

    for tree_id, lat, lon, first_seen, last_seen in trees:
        popup_text = f"""
        <b>Tree ID:</b> {tree_id}<br>
        <b>Latitude:</b> {lat}<br>
        <b>Longitude:</b> {lon}<br>
        <b>First Seen:</b> {first_seen}<br>
        <b>Last Seen:</b> {last_seen}
        """

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=tree_id
        ).add_to(palm_map)

    os.makedirs("output", exist_ok=True)
    palm_map.save(OUTPUT_PATH)

    print(f"Map saved successfully: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_map()
