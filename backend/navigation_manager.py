import time


class NavigationManager:
    def __init__(self, robot_state):
        self.robot_state = robot_state

    def go_to_pose(self, x, y, yaw):
        '''
        Simulated navigation to a waypoint.
        Later this will call ROS2 navigation.
        '''
        print(f"Navigating to pose: x={x}, y={y}, yaw={yaw}")
        time.sleep(1)
        self.robot_state.update_pose(x, y, yaw)
        print("Arrived.")

    def follow_waypoints(self, waypoints):
        '''
        Simulated waypoint following.
        '''
        for i, wp in enumerate(waypoints, start=1):
            print(f"Waypoint {i}/{len(waypoints)}")
            self.go_to_pose(wp["x"], wp["y"], wp["yaw"])

    def return_home(self):
        '''
        Return to stored home pose.
        '''
        home = self.robot_state.home_pose
        if not home:
            raise ValueError("Home pose is not set.")

        print("Returning to home position...")
        self.go_to_pose(home["x"], home["y"], home["yaw"])
        print("Robot returned home.")
