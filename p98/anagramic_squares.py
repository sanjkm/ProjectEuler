# anagramic_squares.py
# Takes as input a list of 20,000 words
# It first finds the anagrams within the list
# Then, it checks to see which anagrams have letter to digit mappings such
# that both anagrams are squares
# Return the largest such square as final output

# Extracts the word list from the inputted filename
import collections, sys, itertools, time

def fill_word_list (filename):

    with open(filename, 'r') as f:
        for line in f:
            x_no_quotes = line.replace('"', '') # removes quotations
            x1 = x_no_quotes.split(',')

    return x1
#-----------------------------------------------------------------------

# Places each word into a list of lists, where list[i] corresponds to the
# words of length i

def word_len_list_calc (word_list):
    # find longest word in list
    max_len = max(map(len, word_list))

    word_len_list = []

    for word_len in range(max_len+1):
        word_len_list.append([])

    for word in word_list:
        word_len_list[len(word)].append(word)
    return word_len_list

# ------------------------------------------------------------------------
# Finds the anagrams in a word list, assuming all words of the same length
def find_anagrams (word_list):

    # make dictionary mapping each word to its sorted letters
    sort_word_dict = {word: ''.join(sorted(list(word))) for word in word_list}
    counter = collections.Counter (sort_word_dict.values())

    sorted_anagrams = [sort_word for sort_word in sort_word_dict.values()
                       if counter[sort_word] > 1]

    inv_dict = {sort_word:[] for sort_word in sorted_anagrams}
    
    for word in word_list:
        if sort_word_dict[word] in sorted_anagrams:
            sorted_word = sort_word_dict[word]
            inv_dict[sorted_word].append(word)
    return inv_dict.values()
#-----------------------------------------------------------------------------

# Take the list of anagrams of length i and find the anagramic squares in
# the list. It returns the largest square number value found, zero
# if nothing found
def find_anagramic_squares (anagram_list, i):

    square_list = set(__make_squares_list (i))
    largest_square = 0
    for anagram in anagram_list:
        if len(anagram) > 2:
            test_list = itertools.combinations (anagram, 2)
        else:
            test_list = [anagram]
        for test_item in test_list:

            map_list = make_anagram_mapping (test_item)
            square_str = map (str, square_list)
            square_str_list = map (list, square_str)
            permuted_squares = set(map (lambda x: digit_mapping(x, map_list),
                                    square_str_list))
            if len(square_list.intersection(permuted_squares)) > 0:
                for test_num in list(square_list.intersection(permuted_squares)):

                    if check_uniqueness_digit (test_item[0], test_num) == 1:
                        largest_square = max(largest_square,
                                             test_num,
                                             reverse_mapping_list (test_num,
                                                                   map_list))
                        print largest_square, test_item[0], test_item[1]
    return largest_square
    
# Returns a number such that the ith digit of x becomes the
# mapping_list[i]th digit of the output
def digit_mapping (x, mapping_list):
    x_permuted = ['0'] * len(x)

    for i in range(len(mapping_list)):
                   
        x_permuted[mapping_list[i]] = x[i]
        
    return int(''.join(x_permuted))
    
# Outputs a list of all the squares with number of digits equal to digit_len
def __make_squares_list (digit_len):

    square_list = []
    min_num = 10 ** (digit_len - 1)
    max_num = 10 ** digit_len - 1

    i = int(min_num ** 0.5)
    if i ** 2 != min_num:
        i += 1

    while i ** 2 <= max_num:
        square_list.append(i ** 2)
        i += 1
    return square_list

# Inputs are two anagrams. Outputs a list where the ith element is the digit
# number that the ith digit of anagram 1 is mapped to in anagram 2
def make_anagram_mapping (anagram_list):
    ag1, ag2 = list(anagram_list[0]), list(anagram_list[1])
    mapping_list = []
    mapped_dict = {} # ensure if any doubles are in the anagrams
    for i in range(len(ag1)):
        test_char = ag1[i]
        if test_char in mapped_dict:

            orig_index = mapped_dict[test_char]
            map_index = ag2[orig_index+1:].index(test_char)
            map_index += (orig_index + 1)
            mapped_dict[test_char] = map_index
        else:
            map_index = ag2.index(test_char)
            mapped_dict[test_char] = map_index
            
        mapping_list.append(map_index)
    return mapping_list

def check_uniqueness_digit (anagram, anagram_num):
    anagram_list = list(anagram)
    check_dict = {}
    digit_list = list(str(anagram_num))
    index = 0
    for dig in digit_list:
        if dig not in check_dict:
            check_dict[dig] = anagram_list[index]
        else:
            if anagram_list[index] != check_dict[dig]:
                return 0
        index += 1
    return 1

# This reverses mapping_list to discover what number mapped to test_num
def reverse_mapping_list (test_num, mapping_list):

    digit_list = list(str(test_num))
    new_num = ['0']*len(digit_list)
    for i in range(len(mapping_list)):
        mapped_dig = mapping_list[i]
        new_num[i] = digit_list[mapped_dig]
        
    return int(''.join(new_num))
#-----------------------------------------------------------------------------
def main():
    start_time = time.time()
    filename = "words.txt"
    word_list = fill_word_list (filename)
    word_len_list = word_len_list_calc (word_list)

    for i in range(len(word_len_list)-1, 1, -1):

        anagram_list = find_anagrams (word_len_list[i])

        if len(anagram_list) == 0:
            continue
        largest_square = find_anagramic_squares (anagram_list, i)
        if largest_square > 0:
            print largest_square
            break
    print time.time() - start_time
main()
