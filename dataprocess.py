import os

# This file is for processing data in the folder "testinstances" to pass into main

# Windows usage
# Input: a filename including '.txt' (assuming file exists in folder 'testinstances')
# Output: a tuple with [0]puzzle in 1D array, [1]puzzle (frame) size
# Purpose: takes in the current directory and append path to get to folder testinstances to read test files
def read_instance(filename):

    data_dir = os.getcwd()+'\\testinstances'
    file = open(data_dir+'\\'+filename, 'r')
    data = file.read()

    puzzle = []

    size_flag = 0
    for line in data:
        # first line contain size of puzzle (N)
        if size_flag == 0:
            size = int(line)
            size_flag = 1
        # rest appends to a 1D list
        else:
            line = line.rstrip('\n ')
            for x in line:
                puzzle.append(int(x))
    
    file.close()
    return puzzle, size