import os

# This file is for processing data in the folder "testinstances" to pass into main

# Windows usage
def read_instance():
    data_dir = os.getcwd()+'\\testinstances'
    file = open(data_dir+'\\s_t01.txt', 'r')
    
    data = file.read()
    
    file.close()