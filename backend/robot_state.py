class RobotState:
    def __init__(self):
        self.status = "idle"
        self.home_pose = None
        self.current_pose = {
            "x": 0.0,
            "y": 0.0,
            "yaw": 0.0
        }
        self.current_mission_id = None

    def set_status(self, status):
        self.status = status

    def set_home_pose(self, x, y, yaw):
        self.home_pose = {
            "x": x,
            "y": y,
            "yaw": yaw
        }

    def update_pose(self, x, y, yaw):
        self.current_pose = {
            "x": x,
            "y": y,
            "yaw": yaw
        }

    def assign_mission(self, mission_id):
        self.current_mission_id = mission_id

    def clear_mission(self):
        self.current_mission_id = None

    def to_dict(self):
        return {
            "status": self.status,
            "home_pose": self.home_pose,
            "current_pose": self.current_pose,
            "current_mission_id": self.current_mission_id
        }
