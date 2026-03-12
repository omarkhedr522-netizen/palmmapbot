class CoveragePlanner:
    def __init__(self, lane_spacing=2.0):
        self.lane_spacing = lane_spacing

    def generate_rectangular_coverage(self, width, height, start_x=0.0, start_y=0.0):
        '''
        Generate a simple lawnmower / boustrophedon coverage path
        for a rectangular farm area.
        '''
        waypoints = []

        y = start_y
        row_index = 0

        while y <= start_y + height:
            if row_index % 2 == 0:
                # left to right
                waypoints.append({
                    "x": start_x,
                    "y": y,
                    "yaw": 0.0
                })
                waypoints.append({
                    "x": start_x + width,
                    "y": y,
                    "yaw": 0.0
                })
            else:
                # right to left
                waypoints.append({
                    "x": start_x + width,
                    "y": y,
                    "yaw": 3.14159
                })
                waypoints.append({
                    "x": start_x,
                    "y": y,
                    "yaw": 3.14159
                })

            y += self.lane_spacing
            row_index += 1

        return waypoints
