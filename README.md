# PalmMapBot

PalmMapBot is a graduation project for palm tree mapping using image detection, GPS, and SLAM-style tree association.

## Current software modules
- YOLO-based palm detection
- Tree ID assignment using backend logic
- SQLite database for missions, trees, and detections
- TreeMapper layer for SLAM + GPS style mapping

## Project structure
- backend/
- detection/
- data/
- dataset/
- utils/

## Setup
1. Create and activate a virtual environment
2. Install dependencies:
   pip install -r requirements.txt

## Notes
Large files such as datasets, trained models, and database files are excluded from Git.
