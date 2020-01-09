import os
import sys
command_lst = sys.argv[1]

with open(command_lst,"r") as f:
    commands = f.readlines()

for command in commands:
    print (command)
    try:
        os.system(command)
    except:
        pass
