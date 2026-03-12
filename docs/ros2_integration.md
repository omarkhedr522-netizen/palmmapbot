# ROS2 Integration

PalmMapBot is designed to integrate with ROS2 for hardware deployment.

## Expected ROS2 nodes

- camera_node
- lidar_node
- gps_node
- slam_node
- navigation_node
- tree_detection_node
- mission_control_node

## Expected ROS2 topics

- /camera/image_raw
- /scan
- /gps/fix
- /robot_pose
- /tree_detection
- /mission_status

## Expected ROS2 services or actions

- /start_mission
- /abort_mission
- /return_home
- navigate_through_waypoints

## Integration strategy

Current Python mission controller should later become the logic behind:
- ROS2 mission services
- ROS2 navigation goals
- ROS2 state publishing
