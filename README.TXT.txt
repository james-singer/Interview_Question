James Singer's Solution to the SciTec Coding Problem
9/29/2023

Written in Python3.9
Only built-in libraries are used

How to run from command line:
The program takes a minimum of 3 command line arguments; the file name, the path to the LLA csv data, and any timestampsyou want the velocity for.

ex: pyhton3 JamesSingerSciTecProblem <path to the .csv> <timestamp1> <timestamp2> etc...

With test timestamps: python3 JamesSingerSciTecProblem <path to the .csv> 1532334000 1532335268

The output is the ECEF velocity component vector in meters per second [X, Y, Z]

I did not hard code the test timestamps, nor did I limit the number of required timestamps so that the program could be easily plugged into another program or script. It should take any timestamp as long as it is within range of the data that was read in. A more in depth explanation of the code can be found in the comments.

Thank you for your consideration! Please email, call, or text with any questions.