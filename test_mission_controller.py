from backend.mission_controller import MissionController

controller = MissionController()

# Simulated survey path
waypoints = [
    {"x": 2.0, "y": 0.0, "yaw": 0.0},
    {"x": 4.0, "y": 0.0, "yaw": 0.0},
    {"x": 6.0, "y": 1.0, "yaw": 0.2},
    {"x": 8.0, "y": 1.5, "yaw": 0.2}
]

mission_id = controller.start_mission(
    mission_name="UGV Survey Mission 1",
    area_name="Farm Sector A",
    notes="Simulated survey mission controller test"
)

print("Current State:", controller.get_state())

controller.survey_farm(waypoints)

print("State before return:", controller.get_state())

controller.return_home()

print("State after return:", controller.get_state())

controller.complete_mission()

print("Final State:", controller.get_state())
