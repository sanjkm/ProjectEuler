# counting_alt.py
# Return number of ways to sum positive integers to 100


# Number of ways to sum to j using numbers no less than i
def partition (i,j, part_dict):

    if (i,j) in part_dict:
        return part_dict[(i,j)]

    
    if i == 0 or j == 0:
        return 0
    if j == 2 * i:
        part_dict[(i,j)] = 1
        return 1
    if j < 2 * i:
        return 0
    
    num_sum_pairs = j/2 # num of ways to sum to j with 2 numbers

    total = num_sum_pairs - (i-1)  # number of sum pairs using nums >= i

    test_i = i
    test_j = j - i

    while test_j >= 2 * test_i:
       total += partition(test_i,test_j, part_dict)
       test_i, test_j = test_i+1, test_j-1
       
    part_dict[(i,j)] = total
    return total

part_dict = {}

print partition (1, 100, part_dict)
    
