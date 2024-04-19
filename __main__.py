import csv
import sys
import math as m
import ECEF
from decimal import Decimal as d  # Decimal is used to increase precision over float


"""
The following function reads in a comma separated variable file
type containing LLA data with timestamps (4 columns).
Input: name of the csv file (string)
Output: timestamps (list of decimals) and LLA coordinates (list of tuples of decimals)
"""
def read_csv(fileName):
    read_timeStamps = []
    read_coordinates = []
    with open(fileName, 'r') as LLA_file:
        csv_reader = csv.reader(LLA_file)
        for row in csv_reader:
            read_timeStamps.append(d(row[0]))
            read_coordinates.append((d(row[1]), d(row[2]), d(row[3])))
    return read_timeStamps, read_coordinates


"""
The following function converts Longitude(degrees)/Latitude(degrees)/Altitude(meters) coordinates to 
Earth Centered, Earth Fixed (meters) coordinates using the WGS84 Parameters.
Input: LLA coordinates (list of tuples of decimals)
Output: Coordinates in ECEF (list of tuples of decimals)
"""
def convert_lla_to_ecef(lla):
    a = d(6378137)
    b = d(a * (d(1) - d(298.257223563 ** (-1))))  # Semi-minor Axis is calculated for a higher degree of precision
    e = m.sqrt((a ** 2 - b ** 2) / (a ** 2))
    z_helper = (b ** 2 / a ** 2)
    ecef_coordinates = []
    for j in lla:  # Iterating through each tuple of coordinates
        lat_rads = d(m.radians(j[0]))
        long_rads = d(m.radians(j[1]))
        N = (a / d(m.sqrt(1 - ((e ** 2) * ((m.sin(lat_rads)) ** 2)))))
        X = (N + j[2]) * d(m.cos(lat_rads)) * d(m.cos(long_rads))
        Y = (N + j[2]) * d(m.cos(lat_rads)) * d(m.sin(long_rads))
        Z = (z_helper * N + j[2]) * d(m.sin(lat_rads))
        ecef_coordinates.append((X, Y, Z))
    return ecef_coordinates

"""
sys.argv[1] represents the name of the csv file to be read in
sys.argv[2] represents the times at which velocity is calculated
"""
if __name__ == '__main__':
    timestamps, LLA_coordinates = read_csv(sys.argv[1])
    for i in range(2, len(sys.argv)):
        assert d(sys.argv[i]) > min(timestamps), "Input timestamp is not in range of input data"
        assert d(sys.argv[i]) < max(timestamps), "Input timestamp is not in range of input data"
    ecef_data = ECEF.ECEFSet(timestamps, convert_lla_to_ecef(LLA_coordinates))  # ECEFSet object is declared, data converted, and populated here
    for i in range(2, len(sys.argv)):
        decimal_velocity = ecef_data.interpolate_velocity(d(sys.argv[i]))
        string_velocity = [str(decimal_velocity[0]), str(decimal_velocity[1]), str(decimal_velocity[2])]
        string_velocity = str(string_velocity)
        print("Velocity at ", sys.argv[i], ": ", string_velocity.replace("'", ""))
