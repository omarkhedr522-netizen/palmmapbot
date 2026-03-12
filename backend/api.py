from fastapi import FastAPI
from pydantic import BaseModel
from backend.tree_manager import TreeManager
from backend.mission_manager import MissionManager
import sqlite3

app = FastAPI()

tree_manager = TreeManager(distance_threshold_m=2.0)
mission_manager = MissionManager()

DB_PATH = "data/palms.db"


class MissionCreateRequest(BaseModel):
    mission_name: str
    area_name: str | None = None
    notes: str | None = None


class DetectionRequest(BaseModel):
    latitude: float
    longitude: float
    mission_id: int | None = None
    confidence: float = 1.0


@app.get("/")
def root():
    return {"message": "PalmMapBot backend is running"}


@app.post("/missions")
def create_mission(request: MissionCreateRequest):
    mission_id = mission_manager.create_mission(
        mission_name=request.mission_name,
        area_name=request.area_name,
        notes=request.notes
    )
    return {"mission_id": mission_id}


@app.post("/detections")
def add_detection(request: DetectionRequest):
    result = tree_manager.process_detection(
        latitude=request.latitude,
        longitude=request.longitude,
        mission_id=request.mission_id,
        confidence=request.confidence
    )
    return result


@app.get("/trees")
def get_trees():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, tree_id, latitude, longitude, status, first_seen, last_seen
        FROM trees
    """)
    rows = cursor.fetchall()
    conn.close()

    trees = []
    for row in rows:
        trees.append({
            "id": row[0],
            "tree_id": row[1],
            "latitude": row[2],
            "longitude": row[3],
            "status": row[4],
            "first_seen": row[5],
            "last_seen": row[6]
        })

    return trees


@app.get("/missions")
def get_missions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT mission_id, mission_name, start_time, end_time, area_name, notes
        FROM missions
    """)
    rows = cursor.fetchall()
    conn.close()

    missions = []
    for row in rows:
        missions.append({
            "mission_id": row[0],
            "mission_name": row[1],
            "start_time": row[2],
            "end_time": row[3],
            "area_name": row[4],
            "notes": row[5]
        })

    return missions
