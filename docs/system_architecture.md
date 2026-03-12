# System Architecture

PalmMapBot combines computer vision, mapping, mission control, and GIS export.

## Core pipeline

Image
? YOLO palm detection
? TreeMapper
? TreeManager
? SQLite database
? Dashboard / HTML map / GeoJSON

## Main modules

### Detection
Located in:
- detection/detect_tree.py
- detection/train_yolo.py
- detection/trigger_and_assign.py

Purpose:
- detect palm trees from images
- return detection confidence
- trigger mapping pipeline

### Mapping
Located in:
- ackend/tree_mapper.py
- ackend/tree_manager.py

Purpose:
- estimate tree position using robot pose + GPS
- assign new or existing tree IDs
- store detections

### Mission Control
Located in:
- ackend/mission_controller.py
- ackend/navigation_manager.py
- ackend/robot_state.py
- ackend/coverage_planner.py

Purpose:
- start mission
- generate survey path
- move through waypoints
- return home
- manage robot state

### Data Layer
Located in:
- create_db.py
- data/palms.db

Tables:
- missions
- trees
- detections

### Interface Layer
Located in:
- dashboard/app.py

Purpose:
- mission control
- robot state display
- live map
- tree/detection/mission view
