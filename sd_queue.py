#!/usr/bin/env python3

import os

queue = "_prompts/queue.txt"
queue = "_prompts/best.txt"

file1 = open(queue, 'r')
Lines = file1.readlines()

for line in Lines:
    if len(line) == 0 or line[0] == '#':
        continue
    os.system('python sd.py ' + line)
