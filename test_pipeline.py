from backend.tree_manager import TreeManager
from backend.mission_manager import MissionManager

# create managers
tree_manager = TreeManager(distance_threshold_m=2.0)
mission_manager = MissionManager()

# start mission
mission_id = mission_manager.create_mission(
    mission_name="Palm Mapping Test",
    area_name="Test Farm",
    notes="Simulated run"
)

print("Mission started:", mission_id)

# simulated detections (robot moving through farm)

detections = [
    (29.203451, 25.519833),
    (29.203452, 25.519834),  # same tree
    (29.203600, 25.520100),  # new tree
    (29.203601, 25.520101),  # same as previous
]

for lat, lon in detections:
    result = tree_manager.process_detection(
        latitude=lat,
        longitude=lon,
        mission_id=mission_id,
        confidence=0.95
    )

    print(result)

# end mission
mission_manager.end_mission(mission_id)

print("Mission finished")