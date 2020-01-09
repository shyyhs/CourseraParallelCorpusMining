import os
from os.path import basename, dirname
import sys
import random

import glob
import argparse

from langdetect import detect
import re

input_folder = sys.argv[1]
output_folder = sys.argv[2]

if (os.path.exists(input_folder) == False):
    print ("Input folder doesn't exist!")
if (os.path.exists(output_folder) == False):
    os.makedirs(output_folder)

names = glob.glob("{}/*.txt".format(input_folder))
for i, name in enumerate(names):
    if (i%1000 == 0):
        print (i)
    new_name = os.path.join(output_folder, basename(name)) 
    command = "python /share03/song//scripts/nfkc.py {} {}".format(name, new_name)
    os.system(command)
