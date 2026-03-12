# PalmMapBot Hardware Setup Guide

This document explains how to deploy PalmMapBot on real hardware.

Recommended platform:

Raspberry Pi 5 or Raspberry Pi 4 (8GB)

---

# Required Hardware

Camera

USB camera or Raspberry Pi Camera Module.

Used for palm detection.

---

LiDAR

Used for SLAM and robot localization.

Example sensors:

RPLidar  
YDLidar

---

GPS

Provides global geographic coordinates.

Example modules:

u-blox NEO-M8N

---

Optional IMU

Improves pose estimation.

Examples:

MPU9250  
BNO055

---

# Recommended Software Stack

Ubuntu 24.04 64-bit (Raspberry Pi)

ROS2 Kilted

Python 3

---

# Installation Steps

## 1 Install Ubuntu on Raspberry Pi

Flash Ubuntu 24.04 using Raspberry Pi Imager.

Boot the Pi and update:


sudo apt update
sudo apt upgrade


---

## 2 Install ROS2

Install ROS2 base:


sudo apt install ros-kilted-ros-base


Enable ROS environment:


source /opt/ros/kilted/setup.bash


Add to bashrc.

---

## 3 Create ROS workspace


mkdir -p ~/palmmapbot_ws/src
cd ~/palmmapbot_ws/src
git clone https://github.com/omarkhedr522-netizen/palmmapbot.git


---

## 4 Install Python dependencies


cd palmmapbot
python3 -m venv palm_env
source palm_env/bin/activate
pip install -r requirements.txt


---

## 5 Initialize database


python create_db.py


---

# Sensor Setup

Camera should publish images to:


/camera/image_raw


LiDAR should publish scans to:


/scan


GPS should publish coordinates to:


/gps/fix


---

# System Runtime

When the robot runs:

1. camera publishes frames
2. YOLO detects palm trees
3. SLAM provides robot pose
4. GPS anchors map globally
5. tree position is estimated
6. tree ID is assigned
7. result stored in SQLite
8. map updated

---

# Output

Tree database


data/palms.db


GIS export


output/palm_trees.geojson


Interactive map


output/palm_tree_map.html

4️⃣ Push the new documentation

Run:

git add docs
git commit -m "Add system architecture and hardware documentation"
git push
After this your repository will look very professional

Structure:

README.md
docs/
system_architecture.md
ros2_node_architecture.md
hardware_setup.md
backend/
detection/
models/
dataset/
data/

This is exactly how serious robotics repositories are structured.