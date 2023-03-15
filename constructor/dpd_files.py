from typing import List
import numpy as np
from bondset import Bondtype
from mol import Dendron
from periodic_box import Box


def print_coord(box: Box,
                x: np.ndarray,
                y: np.ndarray,
                z: np.ndarray,
                b_type: np.ndarray) -> None:
    if not (len(x) == len(y) == len(z) == len(b_type)):
        raise Exception("x, y, z, b_types have different length")
    num_atoms = len(x)
    fcoord = open('COORD', 'w')
    fcoord.write(f'num_atoms {num_atoms} box_size {box.x} {box.y} {box.z}\n')
    temp = 0
    for x, y, z, t in zip(x, y, z, b_type):
        temp += 1
        fcoord.write(
            f'{temp: <10} {x: <25} {y: <25} {z: <25} {t}\n'.format(temp, x, y, z, t))
    fcoord.close()


def print_bonds(box: Box, num_atoms: int, bonds: Bondtype) -> None:
    fbonds = open('BONDS', 'w')
    num_bonds = len(bonds)
    fbonds.write(
        f'num_bonds {num_bonds} num_atoms {num_atoms} box_size {box.x} {box.y} {box.z}\n')
    for bond in bonds:
        fbonds.write(f'{bond[0]} {bond[1]}\n')
    fbonds.close()


def print_fixed(fixed_list: List[int]):
    ffixed = open('FIXED', 'w')
    ffixed.write(
        f'num_fixed {len(fixed_list)} \n')
    for fix in fixed_list:
        ffixed.write(f'{fix}\n')
    ffixed.close()
