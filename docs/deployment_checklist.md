# Deployment Checklist

## Software-only mode

- Clone repo
- Create virtual environment
- Install dependencies
- Run python create_db.py
- Confirm model exists in models/palm_tree_detector.pt
- Run dashboard
- Test mission controller
- Test GeoJSON export

## Hardware mode later

- Install Ubuntu on robot computer
- Install ROS2
- Connect camera
- Connect LiDAR
- Connect GPS
- Confirm image topic
- Confirm scan topic
- Confirm GPS topic
- Confirm SLAM pose
- Connect PalmMapBot mission control to ROS2
- Test Start Mission
- Test Return Home
- Test tree mapping
