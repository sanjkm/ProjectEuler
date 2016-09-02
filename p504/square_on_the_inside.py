# square_on_the_inside.py
# Find the number of quadrilaterals within a 100 x 100 square
# rotated 45 degrees about the x,y axis that contain a perfect square
# number of lattice points

# Given 2 points, return the parameters of the line connecting them
# Will return (m1, m2, b) where y = (m1/m2) x + b
import sys, os, inspect
from math import fabs

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, a)

from factors import gcd

# Given 2 points, this outputs the line that connects them in xy space
# Line is returned in form (m1,m2,b) where y = (m1/m2)x + b
def calc_line_eq (x1, y1, x2, y2):
    
    if x2 == x1:
        print "Slope undefined"
        sys.exit()

    com_factor = gcd ([fabs(x2-x1), fabs(y2-y1)])
    
    m1 = (y2 - y1) / com_factor
    m2 = (x2 - x1) / com_factor
    if m2 < 0:
        m1, m2 = -1 * m1, -1 * m2

    m = m1 / (m2 + 0.0)
    b = y1 - m * x1

    return (m1, m2, b)

def calc_x_given_y (y, m1, m2, b):
    return (y - b) * m2 / (m1+0.0)

# This counts the lattice points, given 4 lines that comprise a
# quadrilateral. Lines are inputted clockwise starting in quadrant 1
def points_given_lines (line_list):

    # Count lattice points between the 1st and 4th lines, by
    # counting down by integer y values to zero
    lp_count = 0
    if line_list[0][2] > 0:
        incr = 1
        start_y = 0
    else:
        incr = -1
        start_y = -1
        
    for y_val in range(start_y, int(line_list[0][2]), incr):
        x1 = calc_x_given_y (y_val, line_list[0][0], line_list[0][1], line_list[0][2])
        x2 = calc_x_given_y (y_val, line_list[1][0], line_list[1][1], line_list[1][2])
        # x1 > 0, x2 < 0 by construction
        if int(x1) == x1:
            within_x1 = max(0, x1 - 1)
        else:
            within_x1 = int(x1)
        if int(x2) == x2:
            within_x2 = min (0, x2 + 1)
        else:
            within_x2 = int(x2)
        lp_count += (within_x1 - within_x2 + 1)





        
    return lp_count

# This counts the number of lattice points strictly within the quadrilateral
# generated by the 4 points inputted
def quad_lattice_points_simple (lp_list):
    num_points = 4
    if len(lp_list) != num_points:
        print "Not 4 vertices in the quadrilateral - break"
        sys.exit()
    
    # Setup the lattice points such that they are in clockwise order, starting with
    # with the point with x=0, y>0
    final_lp_list = [0] * num_points
    for lp in lp_list:
        if lp[0] == 0:
            if lp[1] > 0:
                final_lp_list[0] = lp
            else:
                final_lp_list[2] = lp
        else:
            if lp[0] > 0:
                final_lp_list[1] = lp
            else:
                final_lp_list[3] = lp

    # Determine the lines associated with the quadrilateral
    line_list = []
    for i in range(len(final_lp_list)):
        if i == len(final_lp_list) - 1:
            j = 0
        else:
            j = i+1
        line_list.append(calc_line_eq(final_lp_list[i][0], final_lp_list[i][1],
                        final_lp_list[j][0], final_lp_list[j][1]))
        
    total_points = points_given_lines ([line_list[0], line_list[3]])
    total_points += points_given_lines ([line_list[1], line_list[2]])
    return total_points


lp_list = []
pt1, pt2, pt3, pt4 = (0,4), (3,0), (0, -2), (-1,0)
lp_list.append(pt1)
lp_list.append(pt2)
lp_list.append(pt3)
lp_list.append(pt4)
print quad_lattice_points_simple (lp_list)
