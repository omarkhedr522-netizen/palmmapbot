from backend.mission_manager import MissionManager

manager = MissionManager()

mission_id = manager.create_mission(
    mission_name="Palm Farm Test Mission 1",
    area_name="Sector A",
    notes="Initial software-only mission test"
)

print("Created mission with ID:", mission_id)

mission = manager.get_mission(mission_id)
print("Mission data:", mission)

manager.end_mission(mission_id)
print("Mission ended.")

mission = manager.get_mission(mission_id)
print("Updated mission data:", mission)