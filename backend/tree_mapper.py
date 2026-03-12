import math
from backend.tree_manager import TreeManager


class TreeMapper:
    def __init__(self, tree_manager=None, assumed_tree_distance_m=2.0):
        self.tree_manager = tree_manager if tree_manager else TreeManager(distance_threshold_m=2.0)
        self.assumed_tree_distance_m = assumed_tree_distance_m

    def estimate_tree_local_position(self, robot_x, robot_y, robot_yaw_rad):
        '''
        Estimate tree position in local SLAM/map coordinates.
        Assumes the detected tree is directly in front of the robot.
        '''
        tree_x = robot_x + self.assumed_tree_distance_m * math.cos(robot_yaw_rad)
        tree_y = robot_y + self.assumed_tree_distance_m * math.sin(robot_yaw_rad)

        return {
            "tree_x": tree_x,
            "tree_y": tree_y
        }

    def local_to_global(self, gps_lat, gps_lon, tree_x, tree_y):
        '''
        Very simple placeholder conversion from local meters to GPS.
        This is only for software testing.
        Later this should be replaced by a proper map projection / transform.
        '''
        meters_per_deg_lat = 111320.0
        meters_per_deg_lon = 111320.0 * math.cos(math.radians(gps_lat))

        new_lat = gps_lat + (tree_y / meters_per_deg_lat)
        new_lon = gps_lon + (tree_x / meters_per_deg_lon)

        return {
            "latitude": new_lat,
            "longitude": new_lon
        }

    def process_tree_detection(self, robot_x, robot_y, robot_yaw_rad, gps_lat, gps_lon, mission_id=None, confidence=1.0):
        '''
        Full mapping pipeline:
        detection -> local tree estimate -> global estimate -> backend storage
        '''
        local_tree = self.estimate_tree_local_position(robot_x, robot_y, robot_yaw_rad)

        global_tree = self.local_to_global(
            gps_lat=gps_lat,
            gps_lon=gps_lon,
            tree_x=local_tree["tree_x"],
            tree_y=local_tree["tree_y"]
        )

        result = self.tree_manager.process_detection(
            latitude=global_tree["latitude"],
            longitude=global_tree["longitude"],
            mission_id=mission_id,
            confidence=confidence
        )

        return {
            "mapping_mode": "slam+gps",
            "local_tree_position": local_tree,
            "global_tree_position": global_tree,
            "backend_result": result
        }
