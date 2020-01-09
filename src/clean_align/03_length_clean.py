import os
from os.path import basename, dirname
import sys
import random
import glob
import re
from collections import OrderedDict

from langdetect import detect

lang1 = "en"
lang2 = "ja"
input_folder = "./02_segment"
output_folder = "./03_length_clean"
try:
    lang1 = sys.argv[1]
    lang2 = sys.argv[2]
    input_folder = sys.argv[3]
    output_folder = sys.argv[4]
except:
    print ("notebook")

if (os.path.exists(input_folder) == False):
    print ("There's no input folder")
    exit(0)
if (os.path.exists(output_folder) == False):
    os.makedirs(output_folder)

def get_lang(name):
    res = os.path.basename(name).split('.')                                     
    if (len(res)<3):
        return -1
    return res[1]

names = glob.glob("{}/*.txt".format(input_folder))
print (len(names))

new_names = [basename(name).split('.')[0] for name in names]
new_names = list(OrderedDict.fromkeys(new_names))
new_names.sort()


def check(en_file, ja_file, log):
    with open(en_file, "r") as f:
        en_lines = f.readlines()
    with open(ja_file, "r") as f:
        ja_lines = f.readlines()
    en_line_num = len(en_lines)
    ja_line_num = len(ja_lines)
    if ((en_line_num * 2 < ja_line_num) or (ja_line_num * 2 < en_line_num)):
        out = "{}: {}\n{}: {}\n".format(en_file, en_line_num, ja_file, ja_line_num)
        log.write(out)
        print (out)
        return 0
    return 1


with open("03_length_clean.log".format(lang1, lang2), "w") as log:
    for name in new_names:
        en_name = "{}.{}.txt".format(name, lang1)
        ja_name = "{}.{}.txt".format(name, lang2)
        en_file = os.path.join(input_folder, en_name)
        ja_file = os.path.join(input_folder, ja_name)
        if (os.path.exists(en_file) == 0 or os.path.exists(ja_file) == 0):
            continue
        if check(en_file, ja_file, log):
            new_en_file = os.path.join(output_folder, en_name)
            new_ja_file = os.path.join(output_folder, ja_name)
            command1 = "cp {} {}".format(en_file, new_en_file)
            command2 = "cp {} {}".format(ja_file, new_ja_file)
            os.system(command1)
            os.system(command2)
