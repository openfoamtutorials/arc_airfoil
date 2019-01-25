#!/usr/bin/env python3

import os
import sys

file_path = sys.argv[1]

lines = open(file_path, "r").readlines()
lines = [line.split() for line in lines]
lines = [[float(x) for x in line] for line in lines]
lines.sort()

tmp_path = file_path + ".tmp"
with open(tmp_path, "w") as w:
    line = [str(x) for x in lines[0]]
    w.write("\t".join(line))
    for line in lines[1:]:
        line = [str(x) for x in line]
        w.write("\n" + "\t".join(line))
os.system("mv " + tmp_path + " " + file_path)

