#!/usr/bin/env python3

# This is not part of the tutorial. Please ignore.

import os

def __run(cmd):
    print(cmd)
    os.system(cmd)

def __get_last_line(file_path):
    with open(file_path, "r") as f:
        last = None
        for line in f:
            line = line.strip()
            if line:
                last = line
    return last

def __get_coeffs(file_path):
    coeffs = __get_last_line(file_path)
    coeffs = coeffs.strip().split()
    cm = coeffs[1]
    cd = coeffs[2]
    cl = coeffs[3]
    return (cm, cd, cl, coeffs[0])

def __get_int_folders():
    paths = []
    base_dir = "./case/"
    for x in os.listdir(base_dir):
        if x.isdigit() and x != "0":
            paths.append(base_dir + "/" + x)
    return paths

def __clean_case():
    int_folders = __get_int_folders()
    for f in int_folders:
        __run("rm -r " + f)
    __run("rm -rf ./case/postProcessing")
    __run("rm -rf case/constant/polyMesh")
    __run("rm -f main.msh")

def __change_config(field, value):
    parameters_path = "./mesh/parameters.geo"
    tmp_path = "./mesh/parameters.geo.tmp"
    with open(tmp_path, "w") as w:
        with open(parameters_path, "r") as r:
            for line in r:
                line = line.strip()
                if field in line:
                    line = line.split()
                    line[2] = str(value) + ";"
                    line = " ".join(line)
                w.write(line + "\n")
    __run("mv " + tmp_path + " " + parameters_path)

def __run_aoa(aoa):
    __clean_case()
    __change_config("globalAoa", aoa)
    height = 0.2
    if aoa < 0:
        height = -0.2
    __change_config("bendHeight", height)
    __run("./run.sh")

output_path = "results.txt"
os.system("touch " + output_path)

fine_positive = [x for x in range(1, 30)]
fine_negative = [x for x in range(-1, -30, -1)]
fine = [x for x in range(-29, 30)]
coarse_positive = [x for x in range(30, 190, 5)]
coarse_negative = [x for x in range(-30, -190, -5)]
coarse = coarse_positive + coarse_negative
lift_test = [x for x in range(10, 21)]
non_test = coarse_negative + [x for x in range(-29, 10)] + [x for x in range(21, 30)] + coarse_positive
all_angles = coarse_negative + fine + coarse_positive
for aoa in all_angles:
    # problematic AOAs.
    if aoa == 0:
        aoa += 0.1
    if aoa == 90:
        aoa += 1
    if aoa == 130:
        aoa += 1
    if aoa == 140:
        aoa += 1
    if aoa == 115:
        aoa += 1
    __clean_case()
    __run_aoa(aoa)
    coeffs = __get_coeffs("./case/postProcessing/forceCoeffs1/0/forceCoeffs.dat")
    with open(output_path, "a") as f:
        f.write(str(aoa) + "\t" + "\t".join(coeffs) + "\n")
__clean_case()
