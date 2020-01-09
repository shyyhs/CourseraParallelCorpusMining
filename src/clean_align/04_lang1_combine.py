import os
import random
from langdetect import detect
import sys 
import glob
import re
from os.path import basename, dirname

lang1 = "ja"
input_folder = "./03_length_clean"
output_folder = "./04_lang1_combine"
try:
    lang1 = sys.argv[1]
    input_folder = sys.argv[2]
    output_folder = sys.argv[3]
except:
    print ("notebook")

if (os.path.exists(input_folder) == False):
    print ("No input folder")
    exit(0)

if (os.path.exists(output_folder) == False):
    os.makedirs(output_folder)


def get_lang(name):
    res = os.path.basename(name).split('.')                                     
    if (len(res)<3):
        return -1
    return res[1]



def write_file(file_path, f):
    file_title = basename(file_path)
    special_line = "<BOD> {}\n".format(file_title)
    f.write(special_line)
    with open(file_path, "r") as f1:
        lines = f1.readlines()
        for line in lines:
            line = line.strip()
            if (len(line)>0):
                line += '\n'
                f.write(line)


combine_file_name = "{}/{}.txt".format(output_folder, lang1)
names = glob.glob("{}/*.txt".format(input_folder))

with open(combine_file_name, "w") as f:
    for name in names:
        if (get_lang(name) == lang1):
            write_file(name, f)




