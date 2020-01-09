import os
import sys
import glob
from os.path import basename, dirname

lang1 = "en"
lang2 = "ja"

ids_folder = "./06_ids"
cleaned_folder = "./07_parallel_by_ids"

train_folder = "./08_mkdataset/train"
train_lst = "./08_mkdataset/train_lst.txt"

combined_folder = "./08_mkdataset/combine"
analysis_file = "./08_mkdataset/analysis.txt"

if (os.path.exists(train_folder) == False):
    os.makedirs(train_folder)

if (os.path.exists(combined_folder) == False):
    os.makedirs(combined_folder)

def get_ids_file(name):
    name = name + '.ids.txt'
    name = os.path.join(ids_folder, name)
    return name


def get_cleaned_ja_file(name):
    name = name + '.ja.txt'
    name = os.path.join(cleaned_folder, name)
    return name

def get_cleaned_en_file(name):
    name = name + '.en.txt'
    name = os.path.join(cleaned_folder, name)
    return name


def get_similarity(ids_file):
    with open(ids_file, "r") as f:
        lines = f.readlines()
    tot_len = len(lines)
    if (tot_len == 0):
        print (ids_file)
        return -1
    similarity = 0
    for line in lines:
        line_similarity = float(line.strip().split()[2])
        similarity += line_similarity
    return similarity/tot_len

def get_file_len(name):
    with open(name, "r") as f:
        lines = f.readlines()
    return len(lines)

def combine(folder1, lang1, lang2, folder2, tag):
    # test_folder en ja combined_folder test
    en_names = glob.glob("{}/*.{}.txt".format(folder1, lang1))
    en_names.sort()
    ja_names = glob.glob("{}/*.{}.txt".format(folder1, lang2))
    ja_names.sort()
    en_combined_file = os.path.join(folder2, "{}.{}".format(tag, lang1))
    ja_combined_file = os.path.join(folder2, "{}.{}".format(tag, lang2))
    for en_name, ja_name in zip(en_names, ja_names):
        en_base = basename(en_name).split('.')[0]
        ja_base = basename(ja_name).split('.')[0]
        if (en_base != ja_base):
            print (en_base, ja_base)
            exit(0)
    with open(en_combined_file, "w") as en_file:
        for name in en_names:
            with open(name, "r") as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip() + '\n'
                en_file.write(line)
    with open(ja_combined_file, "w") as ja_file:
        for name in ja_names:
            with open(name, "r") as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip() + '\n'
                ja_file.write(line)

names = glob.glob("{}/*.txt".format(ids_folder))
base_names = [basename(name).split('.')[0] for name in names]
base_names.sort()

similarity_lst = []
for i, name in enumerate(base_names):
    ids_file = get_ids_file(name)
    cleaned_ja_file = get_cleaned_ja_file(name)
    similarity = get_similarity(ids_file)
    file_len = get_file_len(cleaned_ja_file)
    
    similarity_lst.append((name, file_len, similarity))
similarity_lst.sort(key = lambda x: -x[2])

train_line = 0
i = 0
with open(train_lst, "w") as f:
    while (1):
        try:
            current_file, file_len, similarity = similarity_lst[i]
        except:
            break
        if (similarity <= 0): break
        f.write(current_file+'\n')
        ja_file = get_cleaned_ja_file(current_file)
        en_file = get_cleaned_en_file(current_file)
        command = "cp {} {}".format(ja_file, train_folder)
        os.system(command)
        command = "cp {} {}".format(en_file, train_folder)
        os.system(command)
        train_line += file_len
        i+=1

with open(analysis_file, "w") as f:
    f.write("# of train line: {}\n".format(train_line))

combine(train_folder, lang1, lang2, combined_folder, "train")

