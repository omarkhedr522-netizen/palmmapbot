# PalmMapBot ROS2 Node Architecture

The final hardware implementation will run PalmMapBot as a set of ROS2 nodes.

Each node performs a specific task.

---

# Node Overview

camera_node  
Publishes raw camera images.

Topic:

/camera/image_raw

---

palm_detection_node

Runs the YOLO model.

Input:

/camera/image_raw

Output:

/tree_detection

Example message:


detected: true
confidence: 0.92


---

slam_node

Runs LiDAR SLAM.

Examples:

slam_toolbox  
cartographer

Outputs:

/map
/odom
/tf

---

gps_node

Publishes GPS location.

Topic:

/gps/fix

Message:

latitude  
longitude

---

pose_fusion_node

Combines:

SLAM pose  
GPS

Produces global robot pose.

---

tree_mapper_node

Responsible for mapping tree locations.

Inputs:

/tree_detection  
/robot_pose  
/gps

Outputs:

/tree_position

Then calls backend logic to assign tree IDs.

---

database_logger_node

Stores results in SQLite.

Writes:

missions  
trees  
detections

---

# ROS2 Topic Flow

camera_node
↓
palm_detection_node
↓
tree_mapper_node
↓
database_logger_node

SLAM + GPS provide pose inputs for the mapping node.

---

# Future Nodes

tree_health_node  
Analyze tree condition.

map_server_node  
Serve live farm map.

mission_controller_node  
Control robot mapping missions.