from backend.tree_mapper import TreeMapper
from backend.mission_manager import MissionManager

mission_manager = MissionManager()
tree_mapper = TreeMapper(assumed_tree_distance_m=2.0)

mission_id = mission_manager.create_mission(
    mission_name="Tree Mapper Test",
    area_name="Simulated SLAM Zone",
    notes="Software-only test for slam+gps mapping"
)

print(f"Mission started: {mission_id}")

# Simulated robot pose and GPS anchor
robot_x = 10.0
robot_y = 5.0
robot_yaw_rad = 0.0   # facing along +x
gps_lat = 29.203451
gps_lon = 25.519833

result = tree_mapper.process_tree_detection(
    robot_x=robot_x,
    robot_y=robot_y,
    robot_yaw_rad=robot_yaw_rad,
    gps_lat=gps_lat,
    gps_lon=gps_lon,
    mission_id=mission_id,
    confidence=0.92
)

print(result)

mission_manager.end_mission(mission_id)
print("Mission ended.")
