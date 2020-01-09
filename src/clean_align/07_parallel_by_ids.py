import os
from os.path import basename, dirname
import sys
import string
import numpy as np
import glob

lang1 = "en"
lang2 = "ja"
folder_03 = "./03_length_clean"
folder_06 = "./06_ids"
output_folder = "./07_parallel_by_ids"


if (os.path.exists(folder_03) == False):
    print ("No 03 folder!")
if (os.path.exists(folder_06) == False):
    print ("No 06 folder!")
if (os.path.exists(output_folder) == 0): 
    os.makedirs(output_folder)

names = glob.glob("{}/*.en.txt".format(folder_03))
new_names = [''.join(basename(name).strip().split('.')[:-2]) for name in names]
new_names.sort()
print (len(new_names))


for i, name in enumerate(new_names):
    print (i, name)
    en_file = os.path.join(folder_03, "{}.{}.txt".format(name, lang1))
    ja_file = os.path.join(folder_03, "{}.{}.txt".format(name, lang2))
    ids_file = os.path.join(folder_06, "{}.{}.txt".format(name, "ids")) 
    new_en_file = os.path.join(output_folder, "{}.{}.txt".format(name, lang1))
    new_ja_file = os.path.join(output_folder, "{}.{}.txt".format(name, lang2))
    with open(en_file, "r") as f:
        en_lines = f.readlines() 
    with open(ja_file, "r") as f:
        ja_lines = f.readlines() 
    with open(ids_file, "r") as f:
        ids_lines = f.readlines() 
    with open(new_en_file, "w") as en_f, open(new_ja_file, "w") as ja_f:
        for ids_line in ids_lines:
            ja_ids, en_ids, similarity = ids_line.strip().split(' ')
            ja_ids = int(ja_ids)
            en_ids = int(en_ids)
            en_sentence = en_lines[en_ids].strip()
            ja_sentence = ja_lines[ja_ids].strip()
            en_f.write(en_sentence + '\n')
            ja_f.write(ja_sentence + '\n')
