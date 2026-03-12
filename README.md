# PalmMapBot

PalmMapBot is a graduation project for **automatic palm tree detection, mapping, and tree-ID assignment**.

The system is designed to work first as a **software pipeline** and later as a **robotic field system** using:

- a camera for palm-tree detection
- GPS for global position
- SLAM for local robot pose
- a database for tree logging
- GIS export for farm mapping

The main idea is:

1. detect whether a palm tree is in front of the robot
2. estimate the robot pose using SLAM
3. anchor the map globally using GPS
4. estimate tree position
5. assign or reuse a unique tree ID
6. store everything in a SQLite database
7. export the result as a GIS map

---

## 1) Full project function

PalmMapBot performs the following pipeline:

Image  
→ YOLO palm-tree detection  
→ robot pose from SLAM  
→ GPS anchor  
→ tree position estimation  
→ tree ID assignment / matching  
→ database logging  
→ map / GeoJSON export

### Detection logic
The trained YOLO model is used to answer:

- **Is there a palm tree in this image or not?**

If a tree is detected above the configured confidence threshold, the pipeline continues.

### Mapping logic
Tree identity is **not based on visual features**.  
Tree identity is based on **spatial association**.

That means:

- if a detected tree position is near an existing stored tree, reuse that tree ID
- if it is not near an existing stored tree, create a new tree ID

### Database logic
The project stores:

- missions
- trees
- detections

This allows the system to keep a persistent digital inventory of trees.

### GIS logic
The project can export tree points to:

- interactive HTML map
- GeoJSON

This allows viewing results in:

- browser maps
- QGIS
- ArcGIS
- web GIS systems

---

## 2) Repository structure

```text
palmmapbot
│
├── backend
│   ├── __init__.py
│   ├── api.py
│   ├── mission_manager.py
│   ├── tree_manager.py
│   └── tree_mapper.py
│
├── data
│   └── palms.db
│
├── dataset
│   ├── data.yaml
│   ├── images
│   │   ├── train
│   │   ├── val
│   │   └── test
│   ├── labels
│   │   ├── train
│   │   ├── val
│   │   └── test
│   └── unlabeled
│
├── detection
│   ├── auto_label_unlabeled.py
│   ├── detect_tree.py
│   ├── train_yolo.py
│   └── trigger_and_assign.py
│
├── models
│   └── palm_tree_detector.pt
│
├── output
│   ├── palm_tree_map.html
│   └── palm_trees.geojson
│
├── palm_env
│
├── utils
│
├── check_labels.py
├── create_db.py
├── export_geojson.py
├── fix_class_ids.py
├── generate_tree_map.py
├── requirements.txt
├── test_detector_on_val.py
├── test_mission_manager.py
├── test_pipeline.py
├── test_tree_manager.py
├── test_tree_mapper.py
└── README.md