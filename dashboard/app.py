import sys
import os

# add project root to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3
from flask import Flask, jsonify, request, render_template_string, redirect, url_for
from backend.controller_instance import controller

DB_PATH = "data/palms.db"

app = Flask(__name__)


def get_connection():
    return sqlite3.connect(DB_PATH)


def load_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM trees")
    total_trees = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM detections")
    total_detections = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM missions")
    total_missions = cursor.fetchone()[0]

    conn.close()

    return {
        "total_trees": total_trees,
        "total_detections": total_detections,
        "total_missions": total_missions
    }


def load_missions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT mission_id, mission_name, start_time, end_time, area_name
        FROM missions
        ORDER BY mission_id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    missions = []
    for r in rows:
        missions.append({
            "mission_id": r[0],
            "mission_name": r[1],
            "start_time": r[2],
            "end_time": r[3],
            "area_name": r[4]
        })
    return missions


def load_trees(limit=100):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT tree_id, latitude, longitude, status, first_seen, last_seen
        FROM trees
        WHERE latitude IS NOT NULL AND longitude IS NOT NULL
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    trees = []
    for r in rows:
        trees.append({
            "tree_id": r[0],
            "lat": r[1],
            "lon": r[2],
            "status": r[3] if r[3] else "active",
            "first_seen": r[4],
            "last_seen": r[5]
        })
    return trees


def load_detections(limit=50):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT detection_id, tree_id, mission_id, latitude, longitude, confidence, detected_at
        FROM detections
        ORDER BY detection_id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    detections = []
    for r in rows:
        detections.append({
            "detection_id": r[0],
            "tree_id": r[1],
            "mission_id": r[2],
            "lat": r[3],
            "lon": r[4],
            "confidence": r[5],
            "detected_at": r[6]
        })
    return detections


@app.route("/start_mission", methods=["POST"])
def start_mission():
    waypoints = [
        {"x": 2.0, "y": 0.0, "yaw": 0.0},
        {"x": 4.0, "y": 0.0, "yaw": 0.0},
        {"x": 6.0, "y": 1.0, "yaw": 0.2},
        {"x": 8.0, "y": 1.5, "yaw": 0.2}
    ]

    controller.start_mission(
        mission_name="Dashboard Survey Mission",
        area_name="Web-Controlled Farm Sector",
        notes="Started from dashboard"
    )

    controller.survey_farm(waypoints)
    controller.return_home()
    controller.complete_mission()

    return redirect(url_for("index"))


@app.route("/abort_mission", methods=["POST"])
def abort_mission():
    controller.abort_mission()
    return redirect(url_for("index"))


@app.route("/return_home", methods=["POST"])
def return_home():
    controller.return_home()
    return redirect(url_for("index"))


@app.route("/api/state")
def api_state():
    return jsonify(controller.get_state())


@app.route("/")
def index():
    summary = load_summary()
    missions = load_missions()
    trees = load_trees()
    detections = load_detections()
    robot_state = controller.get_state()

    map_center_lat = 29.203451
    map_center_lon = 25.519833

    if trees:
        map_center_lat = trees[0]["lat"]
        map_center_lon = trees[0]["lon"]

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>PalmMapBot Dashboard</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <meta http-equiv="refresh" content="5">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f7f9fc; color: #222; }
        .cards { display: flex; gap: 16px; margin-bottom: 20px; flex-wrap: wrap; }
        .card { background: white; border: 1px solid #ddd; border-radius: 12px; padding: 16px; min-width: 180px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
        .card h3 { margin: 0 0 8px 0; font-size: 16px; }
        .card p { margin: 0; font-size: 24px; font-weight: bold; }
        .section { background: white; padding: 16px; border-radius: 12px; border: 1px solid #ddd; box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin-bottom: 24px; }
        #map { height: 520px; border-radius: 12px; overflow: hidden; border: 1px solid #ddd; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #e5e5e5; padding: 8px; text-align: left; font-size: 14px; }
        th { background: #f0f3f8; }
        form.inline { display: inline-block; margin-right: 10px; }
        button { padding: 10px 14px; border: none; border-radius: 8px; cursor: pointer; }
        .start { background: #198754; color: white; }
        .home { background: #0d6efd; color: white; }
        .abort { background: #dc3545; color: white; }
    </style>
</head>
<body>

    <h1>PalmMapBot Dashboard</h1>
    <p>Mission control + database + map view.</p>

    <div class="cards">
        <div class="card"><h3>Total Trees</h3><p>{{ summary.total_trees }}</p></div>
        <div class="card"><h3>Total Detections</h3><p>{{ summary.total_detections }}</p></div>
        <div class="card"><h3>Total Missions</h3><p>{{ summary.total_missions }}</p></div>
        <div class="card"><h3>Robot Status</h3><p>{{ robot_state.status }}</p></div>
    </div>

    <div class="section">
        <h2>Mission Control</h2>
        <form class="inline" method="post" action="/start_mission">
            <button class="start" type="submit">Start Mission</button>
        </form>
        <form class="inline" method="post" action="/return_home">
            <button class="home" type="submit">Return Home</button>
        </form>
        <form class="inline" method="post" action="/abort_mission">
            <button class="abort" type="submit">Abort Mission</button>
        </form>

        <h3>Robot State</h3>
        <p><b>Status:</b> {{ robot_state.status }}</p>
        <p><b>Current Mission:</b> {{ robot_state.current_mission_id }}</p>
        <p><b>Current Pose:</b> {{ robot_state.current_pose }}</p>
        <p><b>Home Pose:</b> {{ robot_state.home_pose }}</p>
    </div>

    <div class="section">
        <h2>Tree Map</h2>
        <div id="map"></div>
    </div>

    <div class="section">
        <h2>Recent Missions</h2>
        <table>
            <thead>
                <tr>
                    <th>Mission ID</th>
                    <th>Mission Name</th>
                    <th>Start Time</th>
                    <th>End Time</th>
                    <th>Area Name</th>
                </tr>
            </thead>
            <tbody>
                {% for m in missions %}
                <tr>
                    <td>{{ m.mission_id }}</td>
                    <td>{{ m.mission_name }}</td>
                    <td>{{ m.start_time }}</td>
                    <td>{{ m.end_time }}</td>
                    <td>{{ m.area_name }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>Recent Trees</h2>
        <table>
            <thead>
                <tr>
                    <th>Tree ID</th>
                    <th>Latitude</th>
                    <th>Longitude</th>
                    <th>Status</th>
                    <th>First Seen</th>
                    <th>Last Seen</th>
                </tr>
            </thead>
            <tbody>
                {% for tree in trees %}
                <tr>
                    <td>{{ tree.tree_id }}</td>
                    <td>{{ tree.lat }}</td>
                    <td>{{ tree.lon }}</td>
                    <td>{{ tree.status }}</td>
                    <td>{{ tree.first_seen }}</td>
                    <td>{{ tree.last_seen }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>Recent Detections</h2>
        <table>
            <thead>
                <tr>
                    <th>Detection ID</th>
                    <th>Tree ID</th>
                    <th>Mission ID</th>
                    <th>Latitude</th>
                    <th>Longitude</th>
                    <th>Confidence</th>
                    <th>Detected At</th>
                </tr>
            </thead>
            <tbody>
                {% for d in detections %}
                <tr>
                    <td>{{ d.detection_id }}</td>
                    <td>{{ d.tree_id }}</td>
                    <td>{{ d.mission_id }}</td>
                    <td>{{ d.lat }}</td>
                    <td>{{ d.lon }}</td>
                    <td>{{ d.confidence }}</td>
                    <td>{{ d.detected_at }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

<script>
    var map = L.map('map').setView([{{ map_center_lat }}, {{ map_center_lon }}], 18);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 20
    }).addTo(map);

    fetch('/api/state')
        .then(r => r.json())
        .then(state => console.log("Robot state:", state));

    fetch('/api/summary')
        .then(r => r.json())
        .then(summary => console.log("Summary:", summary));

    fetch('/api/trees')
        .then(r => r.json())
        .then(data => {
            data.forEach(tree => {
                let color = "green";
                if (tree.status === "inactive") color = "gray";
                if (tree.status === "removed") color = "red";

                var marker = L.circleMarker([tree.lat, tree.lon], {
                    radius: 7,
                    color: color,
                    fillColor: color,
                    fillOpacity: 0.85
                }).addTo(map);

                marker.bindPopup(
                    "<b>" + tree.tree_id + "</b><br>" +
                    "Status: " + tree.status + "<br>" +
                    "Latitude: " + tree.lat + "<br>" +
                    "Longitude: " + tree.lon + "<br>" +
                    "First Seen: " + tree.first_seen + "<br>" +
                    "Last Seen: " + tree.last_seen
                );
            });
        });
</script>

</body>
</html>
    """, summary=summary, missions=missions, trees=trees, detections=detections,
         robot_state=robot_state,
         map_center_lat=map_center_lat, map_center_lon=map_center_lon)


if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
    
