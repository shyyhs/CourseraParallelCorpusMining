#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from os.path import basename, dirname
import sys
import string
import glob

import numpy as np

from nltk.translate.bleu_score import SmoothingFunction
from nltk.translate import bleu
from nltk import word_tokenize
import nltk
nltk.download('punkt')

from scipy import spatial
import gensim
from gensim.models import Word2Vec

#word2vec_path = "/share03/song/word2vec/en/model.txt"
#model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_path, unicode_errors='ignore')

lang1 = 'ja'
lang2 = 'en'


# In[3]:


lang1_word2vec_path = "/larch/song/lrec/word2vec/{}/model.txt".format(lang1)
lang2_word2vec_path = "/larch/song/lrec/word2vec/{}/model.txt".format(lang2)

lang1_model = gensim.models.KeyedVectors.load_word2vec_format(lang1_word2vec_path, unicode_errors='ignore')
lang2_model = gensim.models.KeyedVectors.load_word2vec_format(lang2_word2vec_path, unicode_errors='ignore')
print ("word2vec model loaded")


# In[39]:


ori_folder =  "./03_length_clean"
trans_lang1_folder = "./05_separate_docs_trans_{}".format(lang1)
trans_lang2_folder = "./05_separate_docs_trans_{}".format(lang2)
output_folder = "./06_ids"
output_folder = './07_parallel_by_ids'

if (os.path.exists(ori_folder) == 0):
    print ("No en folder!")
if (os.path.exists(trans_lang1_folder) == 0) or (os.path.exists(trans_lang2_folder)==0):
    print ("No trans folder!")

if (os.path.exists(output_folder) == 0):
    os.makedirs(output_folder)


# In[48]:


# get vec lists of a sentence
# get connected vec lists of two lists
# get average vec from vec lists
# measure similarity from two vec

def get_vec_list(sentence, model):
    vecs = []
    for word in sentence:
        try:
            vecs.append(model[word])
        except:
            continue
    return vecs

def get_vecs_from_lines(sentences, model):
    vecs = []
    for sentence in sentences:
        vec_list = get_vec_list(sentence, model)
        vecs.append(vec_list)
    return vecs

def connect_vec_list(vec_list1, vec_lists2):
    return (vec_list1 + vec_lists2)

def get_average_vec(vec_list):
    avg_vec = np.zeros(100)
    #avg_vec = np.zeros(len(vec_list[0]))
    for vec in vec_list:
        avg_vec+=vec
    if (len(vec_list)!=0):
        avg_vec/=len(vec_list)
        return avg_vec
    else:
        return np.zeros(100)
    
def get_cos_similarity(hy_vec, ref_vec):
    return (1 - spatial.distance.cosine(hy_vec, ref_vec))

f = []
dp = []
flag = []
decide = [] 
match = []
lang1_len = 0
lang2_len = 0
lang1_vecs = []
lang2_vecs = []
trans_lang1_vecs =[]
trans_lang2_vecs =[]

def dp(i ,j):
    if (i>=lang1_len or j>=lang2_len):
        return 0 
    if (flag[i][j] == 1):
        return f[i][j]
    flag[i][j] = 1
    
    
    select_i_j2 = 0
    select_i2_j = 0
    select_i_j = 0
    select_i_j0 = 0
    select_i0_j = 0
    # 1-2
    if (j+1<lang2_len):
        lang1_vec = get_average_vec(lang1_vecs[i])
        trans_lang1_vec = get_average_vec(connect_vec_list(trans_lang1_vecs[j], trans_lang1_vecs[j+1]))
        lang2_vec = get_average_vec(connect_vec_list(lang2_vecs[j], lang2_vecs[j+1]))
        trans_lang2_vec =  get_average_vec(trans_lang2_vecs[i])
        direction1_sim = get_cos_similarity(lang1_vec, trans_lang1_vec)
        direction2_sim = get_cos_similarity(lang2_vec, trans_lang2_vec)
        average_sim = (direction1_sim + direction2_sim)/2
        select_i_j2 = dp(i+1, j+2) + average_sim
    
    # 2-1
    if (i+1<lang1_len):
        lang2_vec = get_average_vec(lang2_vecs[j])
        trans_lang2_vec = get_average_vec(connect_vec_list(trans_lang2_vecs[i], trans_lang2_vecs[i+1]))
        lang1_vec = get_average_vec(connect_vec_list(lang1_vecs[i], lang1_vecs[i+1]))
        trans_lang1_vec =  get_average_vec(trans_lang1_vecs[j])
        direction1_sim = get_cos_similarity(lang1_vec, trans_lang1_vec)
        direction2_sim = get_cos_similarity(lang2_vec, trans_lang2_vec)
        average_sim = (direction1_sim + direction2_sim)/2
        select_i2_j = dp(i+2, j+1) + average_sim 
    
    # 1-1
    lang1_vec = get_average_vec(lang1_vecs[i])
    trans_lang1_vec = get_average_vec(trans_lang1_vecs[j])
    lang2_vec = get_average_vec(lang2_vecs[j])
    trans_lang2_vec =  get_average_vec(trans_lang2_vecs[i])
    direction1_sim = get_cos_similarity(lang1_vec, trans_lang1_vec)
    direction2_sim = get_cos_similarity(lang2_vec, trans_lang2_vec)
    average_sim = (direction1_sim + direction2_sim)/2
    select_i_j = dp(i+1, j+1) + average_sim
    
    # zero match en sentence
    select_i_j0 = dp(i, j+1)
    
    # zero match ja sentence
    select_i0_j = dp(i+1, j)
    
    
    best_score = -1
    best_index = -1
    #print (i, j)
    #print (select_i_j2, select_i2_j, select_i_j, select_i_j0, select_i0_j)
    for idx, score in enumerate([select_i_j2, select_i2_j, select_i_j, select_i_j0, select_i0_j], 1):
        if (score>best_score):
            best_score = score
            best_index = idx
    f[i][j] = best_score
    decide[i][j] = best_index 
    return f[i][j]
    
def align(lang1_lines, lang2_lines, trans_lang1_lines, trans_lang2_lines):
    # initialize dp array
    global f, flag, decide, match, lang1_len, lang2_len 
    global lang1_vecs, lang2_vecs, trans_lang1_vecs, trans_lang2_vecs
    lang1_len = len(lang1_lines)
    lang2_len = len(lang2_lines)
    f = [[0 for i in range(lang2_len)] for j in range(lang1_len)]
    flag = [[0 for i in range(lang2_len)] for j in range(lang1_len)]
    decide = [[0 for i in range(lang2_len)] for j in range(lang1_len)]
    match = [-1 for j in range(lang1_len)]
    
    # for English
    lang2_tokenized_lines = []
    for line in lang2_lines:
        new_line = word_tokenize(line.strip())
        lang2_tokenized_lines.append(new_line)

    trans_lang2_tokenized_lines = []
    for line in trans_lang2_lines:
        new_line = word_tokenize(line.strip())
        trans_lang2_tokenized_lines.append(new_line)

    lang2_len = len(lang2_tokenized_lines)
    trans_lang2_len = len(trans_lang2_tokenized_lines)
    
    # for Japanese
    lang1_tokenized_lines = []
    for line in lang1_lines:
        new_line = line.strip().split()
        lang1_tokenized_lines.append(new_line)

    trans_lang1_tokenized_lines = []
    for line in trans_lang1_lines:
        new_line = line.strip().split()
        trans_lang1_tokenized_lines.append(new_line)

    lang1_len = len(lang1_tokenized_lines)
    trans_lang1_len = len(trans_lang1_tokenized_lines)
    
    #lang1_len, lang2_len
    #lang1_tokenized_lines, lang2_tokenized_lines
    #trans_lang1_tokenized_lines, trans_lang2_tokenized_lines
    lang1_vecs = get_vecs_from_lines(lang1_tokenized_lines, lang1_model)
    lang2_vecs = get_vecs_from_lines(lang2_tokenized_lines, lang2_model)
    trans_lang1_vecs = get_vecs_from_lines(trans_lang1_tokenized_lines, lang1_model)
    trans_lang2_vecs = get_vecs_from_lines(trans_lang2_tokenized_lines, lang2_model)

    dp(0, 0) # use avg_cos_mat
    
def get_res_from_decide(lang1_lines, lang2_lines, trans_lang1_lines, trans_lang2_lines):
    sentence_pairs = []
    i = 0
    j = 0
    global lang1_len, lang2_len
    while (i<lang1_len and j<lang2_len):
        lang1_sentence = ''
        lang2_sentence = ''
        if (decide[i][j] == 1):
            lang1_sentence = lang1_lines[i].strip()
            lang2_sentence = lang2_lines[j].strip() + ' '+ lang2_lines[j+1].strip()
            i+=1
            j+=2
        elif (decide[i][j] == 2):
            lang1_sentence = lang1_lines[i].strip() + ' '+ lang1_lines[i+1].strip()
            lang2_sentence = lang2_lines[j].strip()
            i+=2
            j+=1
        elif (decide[i][j] == 3):
            lang1_sentence = lang1_lines[i].strip()
            lang2_sentence = lang2_lines[j].strip()
            i+=1
            j+=1
        elif (decide[i][j] == 4):
            j+=1
        elif (decide[i][j] == 5):
            i+=1
        if (lang1_sentence!=''):
            sentence_pairs.append([lang1_sentence, lang2_sentence])
            
    return sentence_pairs

def save_results(sentence_pairs, lang1_file, lang2_file):
    with open(lang1_file, "w") as f1, open(lang2_file, "w") as f2:
        for i, sentence_pair in enumerate(sentence_pairs):
            lang1_sentence, lang2_sentence = sentence_pair
            f1.write(lang1_sentence.strip()+'\n')
            f2.write(lang2_sentence.strip()+'\n')
            #print (i)
            #print (lang1_sentence)
            #print (lang2_sentence)


# In[ ]:


lang1_names = glob.glob("{}/*.{}.txt".format(ori_folder, lang1))
lang2_names = glob.glob("{}/*.{}.txt".format(ori_folder, lang2))
new_names = [''.join(basename(name).strip().split('.')[:-2]) for name in lang1_names]
new_names.sort()
print (len(new_names))
for name_idx, name in enumerate(new_names):
    print (name_idx, name)
    untok_lang1_name = os.path.join(ori_folder, name + '.{}.txt'.format(lang1))
    lang1_name = os.path.join(ori_folder, name + '.{}.txt'.format(lang1)) + '.tok'
    command = "cat {} | jumanpp --segment > {}".format(untok_lang1_name, lang1_name)
    os.system(command)
    
    lang2_name = os.path.join(ori_folder, name + '.{}.txt'.format(lang2))
    
    trans_lang1_name = os.path.join(trans_lang1_folder, name + '.trans_{}.txt'.format(lang1))
    trans_lang2_name = os.path.join(trans_lang2_folder, name + '.trans_{}.txt'.format(lang2))
    #ids_name = os.path.join(output_folder, name + '.ids.txt')
    lang1_output_name = os.path.join(output_folder, "{}.{}.txt".format(name, lang1))
    lang2_output_name = os.path.join(output_folder, "{}.{}.txt".format(name, lang2))

    with open(lang1_name, "r") as f:
        lang1_lines = f.readlines()
    with open(lang2_name, "r") as f:
        lang2_lines = f.readlines()
    with open(trans_lang1_name, "r") as f:
        trans_lang1_lines = f.readlines()
    with open(trans_lang2_name, "r") as f:
        trans_lang2_lines = f.readlines()
    #print (lang1_lines[0])
    #print (lang2_lines[0])
    #print (trans_lang1_lines[0]) 
    #print (trans_lang2_lines[0]) 
    
    #print (len(lang1_lines))
    #print (len(lang2_lines))
    #print (lang1_lines, lang2_lines)
    
    
    align(lang1_lines, lang2_lines, trans_lang1_lines, trans_lang2_lines)
    sentence_pairs = get_res_from_decide(lang1_lines, lang2_lines, trans_lang1_lines, trans_lang2_lines)
    save_results(sentence_pairs, lang1_output_name, lang2_output_name)
    #print (decide)
    #for i, sentence_pair in enumerate(sentence_pairs):
    #    print (i)
    #    lang1_sentence, lang2_sentence = sentence_pair
    #    print (lang1_sentence)
    #    print (lang2_sentence)


# In[ ]:


#def get_vec(sentence, model):
#    res = np.zeros(100)
#    num_of_words = len(sentence)
#    for word in sentence:
#        try:
#            res += model[word]
#        except:
#            num_of_words -= 1
#    res/=num_of_words
#    return res

#def get_vecs_from_lines(lines, model):
#    vecs = []
#    for line in lines:
#        vecs.append(get_vec(line, model))
#    return vecs


#def check_position_similarity(i, trans_len, j, en_len):
#    relative_trans_loc = float(i)/trans_len
#    relative_en_loc = float(j)/en_len
#    relative_err = abs(relative_trans_loc - relative_en_loc)
#    return relative_err


# In[ ]:





