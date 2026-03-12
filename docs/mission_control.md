# Mission Control

PalmMapBot mission control manages the full robot workflow.

## Mission states

- idle
- starting
- surveying
- returning_home
- completed
- stopped
- error

## Mission sequence

1. Start mission
2. Save home position
3. Generate coverage path
4. Survey farm
5. Detect and map trees
6. Return home
7. Complete mission

## Main files

- ackend/mission_controller.py
- ackend/navigation_manager.py
- ackend/robot_state.py
- ackend/coverage_planner.py

## Current mode

Current implementation is software simulation:
- waypoint navigation is simulated
- mapping is real
- database logging is real
- return-home behavior is real in software logic

## Future hardware mode

Later this same controller should call:
- ROS2 navigation
- ROS2 robot pose topics
- ROS2 mission services/actions
