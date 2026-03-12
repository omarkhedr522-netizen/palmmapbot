from backend.mission_controller import MissionController

controller = MissionController()

mission_id = controller.start_mission(
    mission_name="Automatic Coverage Mission",
    area_name="Rectangular Farm",
    notes="Coverage planner test"
)

print("Current State:", controller.get_state())

controller.survey_rectangular_farm(
    width=10.0,
    height=6.0,
    start_x=0.0,
    start_y=0.0
)

print("State before return:", controller.get_state())

controller.return_home()

print("State after return:", controller.get_state())

controller.complete_mission()

print("Final State:", controller.get_state())