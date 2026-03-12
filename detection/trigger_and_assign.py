import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.tree_mapper import TreeMapper
from backend.mission_manager import MissionManager
from detection.detect_tree import TreeDetector


def get_current_robot_pose():
    '''
    Temporary SLAM pose stub.
    Replace later with real SLAM output.
    '''
    return {
        "robot_x": 10.0,
        "robot_y": 5.0,
        "robot_yaw_rad": 0.0
    }


def get_current_geolocation():
    '''
    Temporary GPS stub.
    Replace later with real GPS input.
    '''
    return {
        "latitude": 29.203451,
        "longitude": 25.519833
    }


def main():
    tree_mapper = TreeMapper(assumed_tree_distance_m=2.0)
    mission_manager = MissionManager()
    detector = TreeDetector(
        model_path=r"runs\detect\runs\palm_tree_bootstrap3\weights\best.pt",
        confidence_threshold=0.5
    )

    mission_id = mission_manager.create_mission(
        mission_name="Detection + SLAM + GPS Test",
        area_name="Test Area",
        notes="Software-only integration test with TreeMapper"
    )

    print(f"Mission started: {mission_id}")

    image_path = r"dataset\images\val\HT3001_10.jpg"
    detection_result = detector.detect_tree(image_path)

    print("Detection result:", detection_result)

    if detection_result["has_tree"]:
        pose = get_current_robot_pose()
        gps = get_current_geolocation()

        result = tree_mapper.process_tree_detection(
            robot_x=pose["robot_x"],
            robot_y=pose["robot_y"],
            robot_yaw_rad=pose["robot_yaw_rad"],
            gps_lat=gps["latitude"],
            gps_lon=gps["longitude"],
            mission_id=mission_id,
            confidence=detection_result["confidence"]
        )

        print("Tree detected and mapped:")
        print(result)
    else:
        print("No tree detected. No tree ID assigned.")

    mission_manager.end_mission(mission_id)
    print("Mission ended.")


if __name__ == "__main__":
    main()
