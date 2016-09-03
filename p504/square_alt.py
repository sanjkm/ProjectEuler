# square_alt.py
# Find the number of quadrilaterals within a 100 x 100 square
# rotated 45 degrees about the x,y axis that contain a perfect square
# number of lattice points

# Given 2 points, return the parameters of the line connecting them
# Will return (m1, m2, b) where y = (m1/m2) x + b

import sys, os, inspect, time
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

# This counts the lattice points, between one inputted line and the x=0 axis
def points_between_line_axis (line1):

    # Count lattice points between the 1st and 4th lines, by
    # counting down by integer y values to zero
    lp_count = 0
    # Checks the y-intercept of the line. If greater than zero, count from it to
    # y=1. Otherwise, count from it to y=-1
    m1,m2,b = line1[0], line1[1], line1[2]
    if b > 0:
        incr = 1
        start_y = 1
    else:
        incr = -1
        start_y = -1
        
    for y_val in range(start_y, int(b), incr):
        if b * m1 < 0:
            x1 = calc_x_given_y (y_val, line1[0], line1[1], line1[2])
            x2 = 0
        else:
            x1 = 0
            x2 = calc_x_given_y (y_val, line1[0], line1[1], line1[2])
            
        if int(x1) == x1:
            within_x1 = max(0, x1 - 1)
        else:
            within_x1 = int(x1)

        if int(x2) == x2:
            within_x2 = min(0, x2 + 1)
        else:
            within_x2 = int(x2)


        
        lp_count += (within_x1 - within_x2)
        
    return lp_count

# This counts the number of lattice points strictly within the quadrilateral
# generated by the 4 points inputted
def quad_lattice_points_count (lp_list, lp_dict):
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
                
    total_count = 1   # this accounts for the origin
    for i in range (len(final_lp_list)):
        if i < len (lp_list) - 1:
            max_pt = max (fabs(sum(final_lp_list[i])), fabs(sum(final_lp_list[i+1])))
            min_pt = min (fabs(sum(final_lp_list[i])), fabs(sum(final_lp_list[i+1])))
            total_count += lp_dict[min_pt, max_pt]
            total_count += (fabs(sum(final_lp_list[i])) - 1)
        else:
            max_pt = max (fabs(sum(final_lp_list[i])), fabs(sum(final_lp_list[0])))
            min_pt = min (fabs(sum(final_lp_list[i])), fabs(sum(final_lp_list[0])))

            total_count += lp_dict[min_pt, max_pt]
            total_count += (fabs(sum(final_lp_list[i])) - 1)

    return total_count

def gen_dictionary_lps (max_num):

    lp_dict = {}
    for i in xrange (1, max_num+1):
        for j in range (i, max_num+1):
            # calculate the line equation
            line1 = calc_line_eq (0,i, j, 0)
            lp_dict[i,j] = points_between_line_axis (line1)

    return lp_dict


max_dim = 100
lp_dict = gen_dictionary_lps (max_dim)

square_count = 0
start_time = time.time()
freq_dict = {}
for x1 in range(1,max_dim+1):
    pt1 = (0, x1)
    for x2 in range(1,max_dim+1):
        pt2 = (x2, 0)
        for x3 in range(1,max_dim+1):
            pt3 = (0, -1*x3)
            for x4 in range(1,max_dim+1):
                pt4 = (-1*x4, 0)
                lp_list = [pt1,pt2,pt3,pt4]
                lp_total = quad_lattice_points_count (lp_list, lp_dict)                
                test = int(lp_total ** 0.5)
                if test * test == lp_total:
                    square_count += 1
#                    print lp_list, lp_total
                    if lp_total in freq_dict:
                        freq_dict[lp_total] += 1
                    else:
                        freq_dict[lp_total] = 1
print square_count, int(time.time()-start_time)

