import os
from os.path import basename, dirname
import sys
import string
import glob

import numpy as np

from nltk.translate.bleu_score import SmoothingFunction
from nltk.translate import bleu
from nltk import word_tokenize

from scipy import spatial
import gensim
from gensim.models import Word2Vec

word2vec_path = "/share03/song/word2vec/en/model.txt"
model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_path, unicode_errors='ignore')
print ("word2vec model loaded")

en_folder =  "./03_length_clean"
trans_en_folder = "./05_separate_docs" 
output_folder = "./06_ids"

if (os.path.exists(en_folder) == 0):
    print ("No en folder!")
    exit(0)
    
if (os.path.exists(trans_en_folder) == 0):
    print ("No trans_en folder!")
    exit(0)

if (os.path.exists(output_folder) == 0):
    os.makedirs(output_folder)
    
names = glob.glob("{}/*.en.txt".format(en_folder))
new_names = [''.join(basename(name).strip().split('.')[:-2]) for name in names]

new_names.sort()
print (len(new_names))

def get_cos(sentence):
    res = np.zeros(100)
    num_of_words = len(sentence)
    for word in sentence:
        try:
            res += model[word]
        except:
            num_of_words -= 1
    res/=num_of_words
    return res

def get_cos_similarity(hy, ref):
    hy_cos = get_cos(hy)
    ref_cos = get_cos(ref)
    similarity = 1 - spatial.distance.cosine(hy_cos, ref_cos)
    return similarity

def check_position_similarity(i, trans_len, j, en_len):
    relative_trans_loc = float(i)/trans_len
    relative_en_loc = float(j)/en_len
    relative_err = abs(relative_trans_loc - relative_en_loc)
    
    return relative_err
    
    if (relative_err < 0.3):
        return True
    else:
        return False

dp = []
flag = []
decide = [] # 1: match i with j, 2:j go next 3:i go next
match = []
cos_mat = []
trans_len = 0
en_len = 0
len_trans_en = []
len_en = []
en_tokenized_lines = []
trans_en_tokenized_lines = []

def length_check(leni, lenj):
    if (float(leni)/lenj < 0.5 or float(lenj)/leni < 0.5):
        return False
    else:
        return True

def get_words_num(sentence):
    return (len(sentence))
    
def dp(i ,j):
    if (i>=trans_len or j>=en_len):
        return 0
    if (flag[i][j] == 1):
        return f[i][j]
    flag[i][j] = 1
    if (cos_mat[i][j] > 0.92):
        if (length_check(len_trans_en[i], len_en[j])):
            select_i_j = dp(i+1, j+1) + cos_mat[i][j]
        else:
            select_i_j = -1
    else:
        select_i_j = -1
        
    select_i_afterj = dp(i, j+1)
    select_afteri_j = dp(i+1, j)
    if (select_i_j > select_i_afterj and select_i_j > select_afteri_j):
        f[i][j] = select_i_j
        decide[i][j] = 1
    elif (select_i_afterj > select_afteri_j):
        f[i][j] = select_i_afterj
        decide[i][j] = 2
    else:
        f[i][j] = select_afteri_j
        decide[i][j] = 3
    
    return f[i][j]
    
def align(en_lines, trans_en_lines, ids_file):
    # initialize dp array
    global f, flag, decide, cos_mat, trans_len, en_len, match, len_en
    global len_trans_en, en_tokenized_lines, trans_en_tokenized_lines
    trans_len = len(trans_en_lines)
    en_len = len(en_lines)
    f = [[0 for i in range(en_len)] for j in range(trans_len)]
    flag = [[0 for i in range(en_len)] for j in range(trans_len)]
    decide = [[0 for i in range(en_len)] for j in range(trans_len)]
    cos_mat = [[0 for i in range(en_len)] for j in range(trans_len)]
    match = [-1 for j in range(trans_len)]
    len_trans_en = []
    len_en = []
    
    en_tokenized_lines = []
    for line in en_lines:
        new_line = ''
        for c in line:
            if (ord(c)<128):
                new_line += string.lower(c)
        new_line = word_tokenize(new_line)
        len_en.append(get_words_num(new_line))
        en_tokenized_lines.append(new_line)

    trans_en_tokenized_lines = []
    for line in trans_en_lines:
        new_line = ''
        for c in line:
            if (ord(c)<128):
                new_line += string.lower(c)
        new_line = word_tokenize(new_line)
        len_trans_en.append(get_words_num(new_line))
        trans_en_tokenized_lines.append(new_line)

    en_len = len(en_tokenized_lines)
    trans_len = len(trans_en_tokenized_lines)

    for i in range(trans_len):
        hy = trans_en_tokenized_lines[i]
        max_cos = 0
        idx = -1
        for j in range(en_len):
            ref = en_tokenized_lines[j]
            cos_mat[i][j] = get_cos_similarity(hy, ref)

    dp(0, 0)
    i = 0
    j = 0
    while (i<trans_len and j<en_len):
        if (decide[i][j] == 1):
            match[i] = j
            i+=1
            j+=1
        elif (decide[i][j] == 2):
            j+=1
        else:
            match[i] = -1
            i+=1
            
    for i in range(trans_len):
        if (match[i] >= 0):
            output = "{} {} {}\n".format(i,match[i],cos_mat[i][match[i]])
            ids_file.write(output)

for i, name in enumerate(new_names):
    en_name = os.path.join(en_folder, name + '.en.txt')
    trans_en_name = os.path.join(trans_en_folder, name + '.trans_en.txt')
    ids_name = os.path.join(output_folder, name + '.ids.txt')

    print (i, name)
    with open(en_name, "r") as f:
        en_lines = f.readlines()
    with open(trans_en_name, "r") as f:
        trans_en_lines = f.readlines()
    with open(ids_name, "w") as f:
        align(en_lines, trans_en_lines, f)

