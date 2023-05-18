'''This is the "mymodule.py" module and it provides
    one function called "print_lol" which prints lists
    may or may not include nested lists.
'''
import sys

def print_lol(the_list, leaves, fn = sys.stdout):
    '''This function takes two positional arguments called "the_list"
       and "leaves", respectively. "the_list" is any python list (probably
       nested list) and each item in the list is (recursively) printed to
       the screen on its own line indented according to "leaves"
    '''
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, leaves + 1, fn)
        else:
            for space_stop in range(leaves):
                print(' ', end = '', file = fn)
            print(each_item, file = fn)
