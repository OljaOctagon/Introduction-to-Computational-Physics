import numpy as np
import matplotlib.pyplot as plt
import re
from collections import defaultdict


def read_lmp_dump(lammpsfile):
    numeric_const_pattern = (
        "[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?"
    )
    rx = re.compile(numeric_const_pattern, re.VERBOSE)

    atoms = defaultdict(list)
    box = defaultdict(list)

    lammpsfile = "equilibration.lammpstrj"
    next_time = False
    next_npart = False
    next_box = False
    next_atom = False

    nbox = 3
    box_count = 0
    npart = 0
    atom_count = 0
    with open(lammpsfile, "r") as f:
        for line in f:
            if next_time:
                timestep = rx.findall(line)[0]
                next_time = False

            if next_npart:
                # npart = int(re.findall(r"[-+]?(?:\d*\.*\d+)", line)[0])
                npart = rx.findall(line)[0]
                next_npart = False

            if next_box:
                # boxi = np.array(re.findall(r"[-+]?(?:\d*\.*\d+)", line)).astype(float)
                boxi = np.array(rx.findall(line)).astype(float)
                box[timestep].append(boxi)
                box_count += 1
                if box_count == nbox:
                    next_box = False
                    box_count = 0

            if next_atom:
                # atomi = np.array(re.findall(r"[-+]?(?:\d*\.*\d+)", line)).astype(float)
                atomi = np.array(rx.findall(line)).astype(float)
                atoms[timestep].append(atomi)
                atom_count += 1
                if atom_count == npart:
                    next_atom = False
                    atom_count = 0

            if line.startswith("ITEM: TIMESTEP"):
                next_time = True

            if line.startswith("ITEM: NUMBER OF ATOMS"):
                next_npart = True

            if line.startswith("ITEM: BOX BOUNDS"):
                next_box = True

            if line.startswith("ITEM: ATOMS id type xs ys zs"):
                next_atom = True

    return atoms


atoms = read_lmp_dump("equilibration.lammpstrj")


"""
ITEM: TIMESTEP
201000
ITEM: NUMBER OF ATOMS
1350
ITEM: BOX BOUNDS pp pp pp
-1.0000000000000000e+01 1.0000000000000000e+01
-1.0000000000000000e+01 1.0000000000000000e+01
-5.0000000000000000e-01 5.0000000000000000e-01
ITEM: ATOMS id type xs ys zs
1 1 0.320893 0.703871 0.5
"""
