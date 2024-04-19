"""
This class defines and constructs an Earth Centered, Earth Fixed (ECEF) Coordinate
 object based on the WGS84 Standard. An ECEFSet object contains two member variables;
 a time stamp in seconds since the UNIX Epoch, and a list of coordinates (X,Y,Z).
"""
class ECEFSet:

    def __init__(self, timeStamps, coordinates):
        self.timeStamps = timeStamps  # Type: list of decimals
        self.coordinates = coordinates  # Type: list of tuples of decimals ex: [(x1,y1,z1), (x2,y2,z2), etc...]

    """
    The calculate method function calculates the average velocity components between two timestamps in meters per second.
    Input: starting timestamp, ending timestamp (ECEF object, decimal, decimal)
    Output: velocity in x direction, velocity in y direction, velocity in z direction (list of 3 decimals)
    """
    def calculate_velocity(self, start, end):
        start_index = self.timeStamps.index(start)
        end_index = self.timeStamps.index(end)
        delta_t = self.timeStamps[end_index] - self.timeStamps[start_index]
        delta_x = self.coordinates[end_index][0] - self.coordinates[start_index][0]
        delta_y = self.coordinates[end_index][1] - self.coordinates[start_index][1]
        delta_z = self.coordinates[end_index][2] - self.coordinates[start_index][2]
        return [(delta_x / delta_t), (delta_y / delta_t), (delta_z / delta_t)]

    """
    The interpolate_velocity method function finds the two closest timestamps to a given 'target' timestamp and uses the 
    calculate_velocity method function to find the average velocity components where that target falls.
    Input: target timestamp (int)
    Output: velocity in x direction, velocity in y direction, velocity in z direction (list of 3 decimals)
    """
    def interpolate_velocity(self, target):
        closest_stamp = min(self.timeStamps, key=lambda x: abs(x - target))
        closest_index = self.timeStamps.index(closest_stamp)
        if closest_stamp > target:  # if the 2nd closest timestamp is before to the target
            next_closest_index = closest_index - 1
            final_velocity = self.calculate_velocity(self.timeStamps[next_closest_index], self.timeStamps[closest_index])
        elif closest_stamp < target:  # if the 2nd closest timestamp is after the target
            next_closest_index = closest_index + 1
            final_velocity = self.calculate_velocity(self.timeStamps[closest_index], self.timeStamps[next_closest_index])
        else:  # if the target falls on a timestamp
            next_index = closest_index + 1
            previous_index = closest_index - 1
            final_velocity = self.calculate_velocity(self.timeStamps[previous_index], self.timeStamps[next_index])
        return final_velocity
