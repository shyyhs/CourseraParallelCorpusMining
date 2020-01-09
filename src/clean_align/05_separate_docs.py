import os
import sys 
import glob
from os.path import basename, dirname

input_folder = "./04_lang1_combine"
output_folder = "./05_separate_docs"
ja = "{}/ja.txt".format(input_folder)
trans_en = "{}/trans_en.txt".format(input_folder)

if (os.path.exists(input_folder) == False):
    print ("No input folder")
    exit(0)

if (os.path.exists(output_folder) == False):
    os.makedirs(output_folder)

with open(ja, "r") as f:
    ja_lines = f.readlines()
with open(trans_en, "r") as f:
    en_lines = f.readlines()

def check_new_doc(ja_line):
    if (ja_line[:5] == "<BOD>"):
        return 1
    else:
        return 0

def new_folder(folder, ja_line):
    ja_line =''.join(basename(ja_line.strip().split(' ')[-1]).split('.')[:-2])+".trans_en.txt"
    ja_line = os.path.join(folder, ja_line)
    return ja_line

f = None                                                                        
for i, (ja_line, en_line) in enumerate(zip(ja_lines, en_lines)):
    if (check_new_doc(ja_line)):
        if (f!=None): f.close()
        new_path = new_folder(output_folder, ja_line)
        print (new_path)
        f = open(new_path, "w")
    else:
        f.write(en_line.strip()+"\n")



