import os                                                                       
from os.path import basename, dirname
import sys
import random

import glob
import argparse

from langdetect import detect
import re

try:
    lang1 = sys.argv[1]
    lang2 = sys.argv[2]
    input_folder = sys.argv[3]
    output_folder = sys.argv[4]
except:
    print ("notebook")

lang1 = "en"
lang2 = "ja"
input_folder = "./00_file_extraction"
output_folder = "./01_lang_clean"

if (os.path.exists(input_folder) == False):
    print ("Input folder doesn't exist!")
if (os.path.exists(output_folder) == False):
    os.makedirs(output_folder)
    

n = 10

ja_chars = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよアイウエオカキクケコガギグゲゴサシスセソザジズゼゾタチツテ\
トダヂヅデドナニヌネノハヒフヘホバビブベボパピプペポマミムメモヤユヨラリルレロワヲ"
en_chars = "abcdefghijklmnopqrstuvwxyz"

def get_lang_from_name(name):
    res = os.path.basename(name).split('.')
    if (len(res)<3):
        print ("{} contains no lang info".format(name))
        return -1
    return res[1]


def my_detect(sentence):
    en_flag = 0
    ja_num = 0
    en_num = 0
    for c in sentence:
        if c in ja_chars:
            ja_num += 1
        elif c in en_chars:
            en_num += 1
    if (ja_num == 0 and en_num == 0):
        return 0
    
    #if (ja_num!=0 and ja_num*3 <en_num):
    #    print ("Ja ari: {}".format(sentence))
        
    if (ja_num*3 > en_num):
        return 'ja'
    else:
        return 'en'

def detect_combine(sentence):
    my_detect_res = my_detect(sentence)
    detect_res = detect(sentence)
    if (my_detect_res != 'en'):
        return my_detect_res
    else:
        if (detect_res== 0):
            return my_detect_res
        else:
            return detect_res

    
    
def get_lang_from_file(name, detect_func):
    with open(name, "r") as f:
        lines = f.readlines()
    if (len(lines)==0):
        return 0
    lang = {}
    for i in range(n):
        random_sentence = random.choice(lines)
        random_sentence = random_sentence.strip()
        if(len(random_sentence)==0): continue
        
        try:
            detected_lang = detect_func(random_sentence)
        except:
            continue
        lang[detected_lang] = lang.get(detected_lang, 0) + 1
        
    lst = list(lang.items())
    if (len(lst) == 0): return 0
    lst.sort(key = lambda x:-x[1])
    if (lst[0][1] < n*0.8):
        return 0
    return lst[0][0]

names = glob.glob("{}/*.txt".format(input_folder))
print (len(names))

basename_dict = {}
for i, name in enumerate(names):
    lang_from_name = get_lang_from_name(name)
    lang_from_text = get_lang_from_file(name, detect_combine)

    #if (my_lang != detect_lang):
    #    with open(name) as f:
    #        lines = f.readlines()
    #    print (my_lang, detect_lang, combine)
    #    print (lines[:3])

    if (lang_from_name == lang_from_text):
            tag = basename(name).split('.')[0]
            basename_dict[tag] = basename_dict.get(tag, 0) + 1
            if (basename_dict[tag] == 2):
                en_file =os.path.join(input_folder, "{}.{}.txt".format(basename(name).split('.')[0], lang1))
                ja_file =os.path.join(input_folder, "{}.{}.txt".format(basename(name).split('.')[0], lang2))
                en_new_file = os.path.join(output_folder, basename(en_file))
                ja_new_file = os.path.join(output_folder, basename(ja_file))
                command1 = "cp {} {}".format(en_file, en_new_file)              
                command2 = "cp {} {}".format(ja_file, ja_new_file)
                os.system(command1)
                os.system(command2)
    if ((i%100) == 0):
        print (i)
        

