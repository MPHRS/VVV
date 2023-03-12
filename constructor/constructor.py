from typing import List, Tuple

import numpy as np
from check_graph import CheckGraph
from exceptions import (GapsMolGraphError, MolGraphConnectionError,
                        MolGraphSimplicityError)
from periodic_box import Box
from bondset import Bondtype


def rnd_vector(length_bond=1.0):
    v = np.random.uniform(-1.0, 1.0, 3)
    v /= np.sqrt(np.sum(v**2)) * length_bond
    return v


# class MolGraph():
#     def __init__(self, bonds: List[List[int]] = [[0, 1]]):
#         # Ordering the list of bonds
#         self.bonds = sorted([[min(bond), max(bond)] for bond in bonds])
#         if not CheckGraph.is_not_gaps(self.bonds):
#             raise GapsMolGraphError
#         if not CheckGraph.is_simple(self.bonds):
#             raise MolGraphSimplicityError
#         if not CheckGraph.is_connected(self.bonds):
#             raise MolGraphConnectionError
#         self.directed = CheckGraph.is_directed(self.bonds)
#         # Searchig for max index in the bond list
#         self.num_beads = max([bond[1] for bond in bonds]) + 1
#         self.num_bonds = len(self.bonds)
#         self.cyclical = (self.num_bonds >= self.num_beads)

#     def __str__(self):
#         return f"""
#             Num_beads = {self.num_beads} 
#             Num_bonds = {self.num_bonds}
#             Cyclical = {self.cyclical}
#             Directed = {self.directed}            
#             """

#     def get_coord(
#             self, x0: float, y0: float, z0: float,
#             bond_length: float, box: Box, periodic: bool = True):
#         """Creating coordinates according the list 

#         Returns:
#             3 * ndarray: x,y,z - coordinates 
#         """
#         x = np.zeros(self.num_beads)
#         y = np.zeros(self.num_beads)
#         z = np.zeros(self.num_beads)
#         x[0] = x0
#         y[0] = y0
#         z[0] = z0
#         if self.directed:
#             for bond in self.bonds:
#                 v = rnd_vector(length_bond=bond_length)
#                 x[bond[1]] += v[0]
#                 y[bond[1]] += v[1]
#                 z[bond[1]] += v[2]
#         else:
#             pass
#         return x, y, z


if __name__ == '__main__':
    box = Box(10, 10, 10)
    