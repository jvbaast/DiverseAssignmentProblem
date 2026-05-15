import algorithm
import generate_data
import numpy as np

# Function for printing arrays
def array_to_string(A):
    res = ""
    for row in A:
        for col in row:
            res += str(col) + " "
        res += "\n"
    return res

# Function for writing arrays to files
def write_array(name, A):
    f = open(name, "w")
    f.write(array_to_string(A).removesuffix("\n"))
    f.close()
    
# Function for writing a DAP instance to a file
def write_file(name, n, G, D):
    f = open(name, "w")
    f.write(str(n) + "\n")
    f.write(array_to_string(G))
    f.write(array_to_string(D).removesuffix("\n"))
    f.close()

# Function for writing a list of points to file
def write_points(name, points):
    f = open(name, "w")
    f.write(str(len(points)))
    for point in points:
        f.write("\n")
        f.write(str(point[0]) + " " + str(point[1]))
    f.close()

# Function for reading a list of points from file
def read_points(name):
    f = open(name, "r")
    n = int(f.readline())
    f.close()
    full_arr = np.loadtxt(name, skiprows=1)
    result = []
    if n == 1:
        result += [(full_arr[0], full_arr[1])]
    else:
        for arr in full_arr:
            result += [(arr[0], arr[1])]
    return n, result

# Function for reading timing results from file
def read_timings(name):
    full_arr = np.loadtxt(name)
    return full_arr.T

# Function for creating an empty file
def create_empty_file(name):
    f = open(name, "w")
    f.close()

# Function for appending a number to a file in a new line
def file_append_num(name, num):
    f = open(name, "a")
    f.write(str(num) + "\n")
    f.close()

# Function for loading a DAP instance from file
def load_file(file_name):
    f = open(file_name, "r")
    n = f.readline()
    f.close()
    full_arr = np.split(np.loadtxt(file_name, skiprows=1), [int(n)])
    G = full_arr[0]
    D = full_arr[1]
    return int(n), G, D