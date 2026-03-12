from backend.coverage_planner import CoveragePlanner

planner = CoveragePlanner(lane_spacing=2.0)

waypoints = planner.generate_rectangular_coverage(
    width=10.0,
    height=6.0,
    start_x=0.0,
    start_y=0.0
)

print("Generated waypoints:")
for i, wp in enumerate(waypoints, start=1):
    print(f"{i}: {wp}")
