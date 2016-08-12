# pentagon_numbers.py
# Find the pair of pentagon nums whose sum and difference are
# both pentagon numbers, and whose difference is minimized
# Pentagon nums generated by sequence function n(3n-1)/2

from bisect import bisect_left

# 24n + 1 perfect square is equivalent to n a pentagon number
# as long as sqrt(24*n + 1) is 5 mod 6
def check_if_pentagon (num):
    test = (24 * num) + 1
    test_root = test ** 0.5
    if int(test_root) == test_root:
        if test_root % 6 == 5:
            return 1
    return 0


def nth_pentagon_num (n):
    return n * (3 * n - 1) / 2

min_diff = 0
consec_diff = 0

# While min difference located is
# larger than difference b/w consecutive p.n
# continue to search for p.n's
i = 1
old_pentagon_num = 0
pentagon_list = []
while min_diff >= consec_diff or min_diff == 0:
    new_pentagon_num = nth_pentagon_num (i)

    for num in pentagon_list:
        if check_if_pentagon (new_pentagon_num - num) == 1:

            # check if sum is a pentagon number
            if check_if_pentagon (new_pentagon_num + num) == 1:

                if min_diff > 0:
                    min_diff = min (min_diff, new_pentagon_num - num)
                else:
                    min_diff = new_pentagon_num - num
                print new_pentagon_num, num, min_diff            
                    
    pentagon_list.append (new_pentagon_num)
    consec_diff = new_pentagon_num - old_pentagon_num
    old_pentagon_num = new_pentagon_num

    # This removes unneeded elements of pentagon list at the beginning
    # As the difference between new elements and those elements is larger
    # than the min_diff, we don't need them anymore
    if min_diff > 0:
        min_val_needed = new_pentagon_num - min_diff
        pos = bisect_left (pentagon_list, min_val_needed)
        if pos > 1:
            pentagon_list = pentagon_list[pos-1:]
    i += 1
    
print min_diff, i, new_pentagon_num
