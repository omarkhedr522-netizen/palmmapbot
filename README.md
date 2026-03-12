<<<<<<< HEAD
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
3) Key files and what each one does
create_db.py

Creates the SQLite database structure.

This is the project’s database schema file.

It creates:

missions

trees

detections

backend/tree_manager.py

Handles tree storage and tree ID assignment.

Responsibilities:

calculate geographic distance between trees

check whether a detected tree already exists

create a new tree if needed

log detections

backend/mission_manager.py

Handles mission creation and mission ending.

Responsibilities:

create a mission

return mission ID

end a mission

fetch mission metadata

backend/tree_mapper.py

Acts as the bridge between:

detection

SLAM pose

GPS

backend tree storage

Responsibilities:

estimate tree position in front of the robot

convert local SLAM coordinates into global coordinates

pass the result to TreeManager

detection/train_yolo.py

Trains the YOLO model.

detection/detect_tree.py

Loads the trained YOLO model and returns:

has_tree

confidence

detection/trigger_and_assign.py

Runs the integrated pipeline:

detect tree

read pose

read GPS

call TreeMapper

store result

generate_tree_map.py

Generates an interactive HTML map from the database.

export_geojson.py

Exports trees from the database to GeoJSON.

4) Trained model location

The trained YOLO model is already included in the repository here:

models/palm_tree_detector.pt

This is the model used by:

detection/detect_tree.py

So after cloning the repo, you do not need to retrain the model unless you want to improve it.

5) Database file

The working database file is:

data/palms.db

If it does not exist yet, create it by running:

python create_db.py
6) How to clone and run the project on another device
Step 1 — Clone the repository
git clone https://github.com/omarkhedr522-netizen/palmmapbot.git
cd palmmapbot
Step 2 — Create a Python virtual environment

Windows:

python -m venv palm_env
palm_env\Scripts\activate
Step 3 — Install dependencies
pip install -r requirements.txt

If requirements.txt is incomplete on a fresh machine, install these minimum packages too:

pip install ultralytics folium opencv-python
Step 4 — Create the database
python create_db.py
Step 5 — Test the pipeline
python detection\trigger_and_assign.py
Step 6 — Generate the HTML map
python generate_tree_map.py
Step 7 — Export GeoJSON
python export_geojson.py
7) How to keep working from multiple devices
On device A

After making changes:

git add .
git commit -m "Describe your update"
git push
On device B

Before starting new work:

git pull

Then continue editing, and when finished:

git add .
git commit -m "Describe your update"
git push
8) How to use Git with different users if needed
Case A — same GitHub account on multiple devices

Use the same repo URL and same GitHub account on all devices.

Set your local Git identity on each device:

git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"

Then work normally:

git pull
git add .
git commit -m "Update message"
git push
Case B — different users collaborating on the same project

The clean method is:

each collaborator forks the repository

each collaborator clones their fork

each collaborator creates a branch

they push to their fork

they open a Pull Request into the main project

Example:

git checkout -b feature/my-change
git add .
git commit -m "My change"
git push origin feature/my-change
Case C — same physical machine, different Git identities

Set Git identity globally for one user:

git config --global user.name "User One"
git config --global user.email "user1@example.com"

Or set it only for the current repo:

git config user.name "User Two"
git config user.email "user2@example.com"

That changes the commit identity for this repository only.

9) How the current software pipeline works

The current software test flow is:

choose an image

YOLO checks whether a tree exists

if a tree is detected:

a robot pose is used

a GPS anchor is used

TreeMapper estimates tree position

TreeManager checks for an existing tree

a tree ID is created or reused

detection is stored in SQLite

Current test mode

Right now:

the YOLO detector is real

the database is real

the tree-ID logic is real

the SLAM pose and GPS inputs are currently stubs/placeholders in software tests

That is intentional until the hardware is connected.

10) How to retrain the model

If you want to retrain the detector:

Step 1 — Prepare dataset

Make sure your dataset has:

dataset/images/train
dataset/images/val
dataset/labels/train
dataset/labels/val
dataset/data.yaml
Step 2 — Train
python detection\train_yolo.py
Step 3 — Find best model

Training output will be under:

runs/detect/...

Copy the best model to:

models/palm_tree_detector.pt
Step 4 — Commit the updated model if desired
git add models/palm_tree_detector.pt
git commit -m "Update trained palm detector"
git push
11) How to generate the map
Interactive browser map
python generate_tree_map.py

Output:

output/palm_tree_map.html

Open it in a browser to view tree markers.

GeoJSON export
python export_geojson.py

Output:

output/palm_trees.geojson

This file can be opened in:

QGIS

ArcGIS

web GIS software

12) Hardware implementation plan

This is the recommended real robot implementation path.

Recommended hardware

Raspberry Pi 5 or Raspberry Pi 4 (8 GB preferred)

USB camera or Raspberry Pi camera

LiDAR sensor

GPS module

optional IMU

robot base / chassis

battery and power regulation

Recommended software stack

Ubuntu 24.04 64-bit on Raspberry Pi

ROS 2 Kilted

Python nodes for PalmMapBot logic

SLAM package

LiDAR driver

camera driver

GPS ROS package

13) Recommended hardware setup choice

For the easiest official ROS 2 route on Raspberry Pi:

install Ubuntu 24.04 64-bit on the Pi

install ROS 2 Kilted

use ROS base

run your PalmMapBot packages as ROS 2 nodes

This is preferred over plain Raspberry Pi OS for a native binary ROS 2 setup.

14) Step-by-step hardware implementation on Raspberry Pi
Phase A — Prepare the Pi
Step 1 — Flash the OS

Flash Ubuntu 24.04 64-bit for Raspberry Pi onto the SD card.

Step 2 — Boot the Pi

Connect:

display or SSH

keyboard/mouse if needed

network

Step 3 — Update system
sudo apt update
sudo apt upgrade -y
Phase B — Install ROS 2 on the Pi
Step 4 — Set locale
sudo apt install locales -y
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
Step 5 — Enable universe
sudo apt install software-properties-common -y
sudo add-apt-repository universe
Step 6 — Install ROS 2 apt source
sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
Step 7 — Install ROS 2 base
sudo apt update
sudo apt install ros-kilted-ros-base -y
Step 8 — Source ROS 2
echo "source /opt/ros/kilted/setup.bash" >> ~/.bashrc
source ~/.bashrc
Step 9 — Install development tools
sudo apt install ros-dev-tools -y
Phase C — Create the ROS 2 workspace
Step 10 — Create a workspace
mkdir -p ~/palmmapbot_ws/src
cd ~/palmmapbot_ws
Step 11 — Clone the repo into src
cd ~/palmmapbot_ws/src
git clone https://github.com/omarkhedr522-netizen/palmmapbot.git
Step 12 — Install Python dependencies
cd ~/palmmapbot_ws/src/palmmapbot
python3 -m venv palm_env
source palm_env/bin/activate
pip install -r requirements.txt
Step 13 — Create database
python create_db.py
Phase D — Connect the sensors
Step 14 — Camera

Connect the camera and verify that images can be read in Python or from a ROS image topic.

Expected ROS topic later:

/camera/image_raw
Step 15 — LiDAR

Install the ROS 2 driver package for your LiDAR model.

Expected LiDAR topic:

/scan
Step 16 — GPS

Connect the GPS module and publish its output to ROS 2.

Expected GPS topic:

/gps/fix
Step 17 — Optional IMU

If used:

/imu/data
Phase E — Add SLAM

Choose one SLAM approach:

Option 1 — LiDAR SLAM

Examples:

slam_toolbox

cartographer

Option 2 — Visual SLAM

Examples:

ORB-SLAM3 integration

stereo/monocular visual odometry + mapping

Step 18 — Start SLAM

The robot should now publish:

pose

map

odometry

Expected topics may include:

/map
/odom
/tf
Phase F — ROS 2 node design for PalmMapBot

The PalmMapBot software should be split into ROS 2 nodes.

1. camera_node

Publishes raw image frames.

2. palm_detection_node

Wraps models/palm_tree_detector.pt
and publishes:

/tree_detection

Message example:

detected: true/false

confidence

3. pose_fusion_node

Consumes:

SLAM pose

GPS

optionally IMU

Publishes:

robot global/local pose

4. tree_mapper_node

Consumes:

detection result

robot pose

GPS anchor

Runs logic similar to:

backend/tree_mapper.py

backend/tree_manager.py

Publishes:

tree position

tree ID

5. database_logger_node

Writes:

missions

trees

detections

to SQLite

15) Example ROS 2 runtime flow

When the robot drives:

camera publishes image

detection node runs YOLO

if a palm is detected:

current pose is read from SLAM

GPS is read

tree position is estimated

tree is matched or created

database is updated

next frame is processed

This creates a continuous palm-tree inventory map.

16) Practical implementation order on hardware

Use this exact order:

Stage 1 — Raspberry Pi only

install Ubuntu

install ROS 2

clone repo

run software-only tests

Stage 2 — Camera only

publish image

run detector

verify has_tree

Stage 3 — GPS only

read GPS

verify coordinates

Stage 4 — LiDAR + SLAM

start SLAM

verify robot pose

Stage 5 — Full integration

detection + pose + GPS + mapper + database

Stage 6 — Mapping output

HTML map

GeoJSON export

QGIS visualization

17) Notes about deployment
On the Pi

Use:

ros-kilted-ros-base

headless operation

SSH for control

For model speed

YOLO nano/small is preferred on Raspberry Pi.
If needed later:

use a lighter model

use image resizing

process every Nth frame

For database

SQLite is good for local field storage.
Later, it can be replaced with PostgreSQL/PostGIS if needed.

18) Current status of the project

Implemented:

trained YOLO detector

tree detection pipeline

tree mapping layer

tree-ID assignment

SQLite logging

HTML map generation

GeoJSON export

GitHub repository

Pending full hardware deployment:

ROS 2 nodes

live sensor integration

real SLAM pose input

real GPS topic input

continuous mission execution

19) Quick start summary
Local software test
python create_db.py
python detection\trigger_and_assign.py
python generate_tree_map.py
python export_geojson.py
Clone on another device
git clone https://github.com/omarkhedr522-netizen/palmmapbot.git
cd palmmapbot
python -m venv palm_env
palm_env\Scripts\activate
pip install -r requirements.txt
python create_db.py
Push changes
git add .
git commit -m "Your update"
git push
20) Author / project purpose

PalmMapBot is being developed as a graduation project focused on:

precision agriculture

robotic mapping

digital farm inventory

autonomous tree monitoring

The final objective is a robot that can move through a palm plantation and build a reliable digital tree map automatically.