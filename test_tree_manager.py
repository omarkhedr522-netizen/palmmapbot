from backend.tree_manager import TreeManager

manager = TreeManager(distance_threshold_m=2.0)

# First detection
result1 = manager.process_detection(
    latitude=29.203451,
    longitude=25.519833,
    mission_id=1,
    confidence=0.95
)
print("Detection 1:", result1)

# Second detection very close to the first one
result2 = manager.process_detection(
    latitude=29.203452,
    longitude=25.519834,
    mission_id=1,
    confidence=0.96
)
print("Detection 2:", result2)

# Third detection farther away
result3 = manager.process_detection(
    latitude=29.203600,
    longitude=25.520100,
    mission_id=1,
    confidence=0.92
)
print("Detection 3:", result3)