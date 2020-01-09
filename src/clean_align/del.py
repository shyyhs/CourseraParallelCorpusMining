import os
import sys
import glob
from os.path import basename, dirname

with open("del.lst", "r") as f:
    del_names = [line.strip() for line in f.readlines()]

def get_title(name):
    return basename(name).split('.')[0]
before_folder = "03_length_clean_before"
after_folder = "03_length_clean"
before_names = glob.glob("{}/*.txt".format(before_folder))


for name in before_names:
    title = get_title(name)
    if (title not in del_names):
        new_name = os.path.join(after_folder, basename(name))
        command = "cp {} {}".format(name, new_name)
        print (command)
        os.system(command)

