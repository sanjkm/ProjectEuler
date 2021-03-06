# path_sum_4_ways.py
# Find the minimal path sum from upper left to bottom right corner of an
# 80 x 80 matrix, where up, right, left, right movement is permitted
import time

from copy import copy

def get_matrix_data (filename):
    data_matrix = []
    with open (filename, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            x1 = line.split(',')
            x2 = map (int, x1)
            data_matrix.append (x2)
    return data_matrix


def valid_move_check (i, j, num_rows, num_cols):
    if i < num_rows and j < num_cols:
        if i >= 0 and j >= 0:
            return 1
    return 0


# This recursive function will determine the minimum path value for the
# element of the matrix inputted. It will do this by calculating min values for all
# possible paths, with the condition that any path greater than already calculated paths are not optimal

def calc_min_path_value (data_matrix, min_path_matrix, curr_row, curr_col,
                         last_move, curr_min_val, min_landing_val, path_buffer, curr_path_val):

    min_path_val = curr_min_val + path_buffer
    valid_move_list = [(1,0), (-1,0), (0,1), (0,-1)]
    num_rows, num_cols = len (data_matrix), len (data_matrix[0])

    final_min_value = 0 # this is the path value plus the min path val of the final slot
    
    # base case - path has landed at an element with a previously calculated min path value
    if min_path_matrix[curr_row][curr_col] > 0:
        return curr_path_val + min_path_matrix[curr_row][curr_col] - data_matrix[curr_row][curr_col]

    # general case - run through valid moves
    for move in valid_move_list:
        
        new_row, new_col = curr_row + move[0], curr_col + move[1]
                                                 
        if valid_move_check (new_row, new_col, num_rows, num_cols):
            if move[0] + last_move[0] != 0 or move[1] + last_move[1] != 0: # reverse of last move
                new_path_val = curr_path_val + data_matrix[new_row][new_col]
                                
                if new_path_val < min_path_val:
                    final_path_val = calc_min_path_value (data_matrix, min_path_matrix, new_row,
                                                                      new_col, move, curr_min_val, min_landing_val, path_buffer, new_path_val)
                    if final_min_value == 0:
                        final_min_value = final_path_val
                    else:
                        final_min_value = min (final_path_val, final_min_value)

    if final_min_value == 0: # No valid moves
        return curr_min_val + min_landing_val
                        
    return final_min_value
    
# This will determine the min path value for each element of the matrix
# The solution to the problem will be the minimum value of the element [0,0]

def assign_values_matrix (data_matrix):

    num_rows = len(data_matrix)
    num_cols = len (data_matrix[0])
    min_path_matrix = []
    gradual_data_matrix = []
    test_row = [0] * len(data_matrix[0])
    
    # Initializes the min_path matrix with zeroes
    for i in range (len (data_matrix)):
        min_path_matrix.append (copy(test_row))
        gradual_data_matrix.append (copy(test_row))

    # We know the bottom corner value is itself
    # We also know the values of the elements that are one move
    # away from the bottom corner, as the min path can only be to go
    # directly to the bottom corner

    bottom_corner_val = data_matrix[num_rows-1][num_cols-1]
    
    min_path_matrix[num_rows-1][num_cols-1] = bottom_corner_val
    gradual_data_matrix[num_rows-1][num_cols-1] = data_matrix[num_rows-1][num_cols-1]
    
    min_path_matrix[num_rows-1][num_cols-2] = bottom_corner_val + data_matrix[num_rows-1][num_cols-2]
    gradual_data_matrix[num_rows-1][num_cols-2] = data_matrix [num_rows-1][num_cols-2]
    
    min_path_matrix[num_rows-2][num_cols-1] = bottom_corner_val + data_matrix[num_rows-2][num_cols-1]
    gradual_data_matrix[num_rows-2][num_cols-1] = data_matrix[num_rows-2][num_cols-1]

    last_min_height_val = min (data_matrix [num_rows-1][num_cols-2], data_matrix[num_rows-2][num_cols-1])
    
    # for height in xrange((num_rows - 2) + (num_cols - 1) - 1, -1, -1):
    for height in xrange((num_rows - 2) + (num_cols - 1) - 1, (num_rows - 2) + (num_cols - 1) - 25, -1):
        if height >= num_rows - 1:
            init_row = num_rows - 1
            init_col = height - init_row
        else:
            init_row = height
            init_col = 0
            
        curr_row, curr_col = init_row, init_col
        init_min_path_val = sum ([sum(row) for row in data_matrix]) # largest possible path value
        min_height_val = init_min_path_val

        while curr_row >=0 and curr_col < num_cols:
            curr_val = data_matrix [curr_row][curr_col]
            
            min_path_val = init_min_path_val
            
            if valid_move_check (curr_row+1, curr_col, num_rows, num_cols):
                path_buffer = min_path_matrix[curr_row+1][curr_col] - last_min_height_val
                test_path_val = curr_val + min_path_matrix[curr_row+1][curr_col]
                if test_path_val < min_path_val:
                    min_path_val = curr_val + data_matrix[curr_row+1][curr_col]
                    min_landing_val = min_path_matrix[curr_row+1][curr_col] - data_matrix[curr_row+1][curr_col]
                    valid_path_buffer = path_buffer
                    
                
            if valid_move_check (curr_row, curr_col+1, num_rows, num_cols):
                
                path_buffer = min_path_matrix[curr_row][curr_col+1] - last_min_height_val
                test_path_val =  curr_val + min_path_matrix[curr_row][curr_col+1]
                if test_path_val < min_path_val:
                    min_path_val = curr_val + data_matrix[curr_row][curr_col+1]
                    min_landing_val = min_path_matrix[curr_row][curr_col+1] - data_matrix[curr_row][curr_col+1]
                    valid_path_buffer = path_buffer
     
                
            curr_path_val = data_matrix[curr_row][curr_col]
            last_move = (0,0)
            
            min_path_matrix[curr_row][curr_col] = calc_min_path_value (data_matrix, min_path_matrix, curr_row, curr_col,
                                                                        last_move, min_path_val, min_landing_val, 1 * valid_path_buffer, curr_path_val)
            gradual_data_matrix[curr_row][curr_col] = data_matrix[curr_row][curr_col]

            min_height_val = min (min_path_matrix[curr_row][curr_col], min_height_val)

            curr_row -= 1
            curr_col += 1


            
        last_min_height_val = min_height_val

    return min_path_matrix, gradual_data_matrix        
        
def main():
    
    start_time = time.time()
    
    filename = "matrix.txt"
    data_matrix = get_matrix_data (filename)
    min_path_matrix, gradual_data_matrix = assign_values_matrix (data_matrix)

    # print min_path_matrix[69:]
    # print gradual_data_matrix[69:]

    print min_path_matrix[1][0], min_path_matrix[0][1], min_path_matrix[0][0], data_matrix[0][0]
    print time.time() - start_time


main()
    
