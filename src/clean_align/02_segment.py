import os
from os.path import basename, dirname
import random
from langdetect import detect
import sys 
import glob
import re

try:
    lang1 = sys.argv[1]
    lang2 = sys.argv[2]
    input_folder = sys.argv[3]
    output_folder = sys.argv[4]
except:
    print("notebook")

lang1 = "en"
lang2 = "ja"
input_folder = "./01_lang_clean"
output_folder = "./02_segment"

if (os.path.exists(input_folder) == False):
    print ("Foldername doesn't exist!")
if (os.path.exists(output_folder) == False):
    os.makedirs(output_folder)

def clean(line):
    line = re.sub(' +', ' ', line).strip()
    line = re.sub(u'(\[.*\])|(<.*>)', '', line)
    line = re.sub(' +', ' ', line).strip()
    return line

def get_lang(name):
    res = os.path.basename(name).split('.')
    if (len(res)<3):
        return -1
    return res[1]

def arrange_sentence(name, new_name):
    lang = get_lang(name)
    
    punc = ['。','？', '?', '！','!','.']
#    if ((get_lang(name) == 'ja') or (get_lang(name) == 'zh-CN')):
#        punc = ['。','？', '?', '!','.']
#    else:
#        punc = ['.', '?','!']

    with open(name, "r") as f:
        lines = [line for line in f.readlines()]
        
    line_num = len(lines)                                                       
    dotnum = 0
    periodnum = 0
    for line in lines:
        for c in line:
            if (c=='.' or c=='?'):
                dotnum+=1
            if (c=='。'):
                periodnum+=1

    if (lang == 'ja'):
        if (float(periodnum)/line_num<0.3):
            #print (lines[0])
            return
    if (lang == 'en' and float(dotnum)/line_num<0.3):
        #print (lines[0])
        return
    
    with open(new_name, "w") as f:
        current_sentence = ""
        for line in lines:
            line = line.strip()+'\n'
            for j, c in enumerate(line):
                if (c==u"\u200B" or c=='\n'):
                    continue
                current_sentence += c
                if (lang == 'ja'):
                    if (c not in punc):
                        continue
                if (lang == 'en'):
                    if (j==len(line)-1):
                        print (line)
                    if ((c not in punc) or (not ((line[j+1] == ' ') or (line[j+1] == '\n')))):
                        continue
                current_sentence = clean(current_sentence)
                if (len(current_sentence) > 0):
                    current_sentence += '\n'
                    f.write(current_sentence)
                current_sentence = ""
            if (lang != 'ja' and lang!='zh-CN'):
                current_sentence += ' '
        current_sentence = clean(current_sentence)
        if (len(current_sentence) > 0):
            current_sentence += '\n'
            f.write(current_sentence)
        current_sentence = ""


names = glob.glob("{}/*.txt".format(input_folder))
print (len(names))

for i, name in enumerate(names):
    new_name = os.path.join(output_folder, basename(name))
    arrange_sentence(name, new_name)
    if (i%100 ==0):
        print(i)
