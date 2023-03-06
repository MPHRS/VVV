from typing import (List, Tuple)
import numpy as np
from exeptions import NegativeValueError
from exeptions import GapsMolGraphError
from exeptions import MolGraphSimplicityError
from exeptions import MolGraphConnectionError


def periodic(coord, box):
    if abs(coord) > 0.5 * box:
        return coord - np.sign(coord) * box
    return coord


class Box():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def periodic_correct(self, xb, yb, zb):
        xb = periodic(xb, self.x)
        yb = periodic(yb, self.y)
        zb = periodic(zb, self.z)
        return xb, yb, zb


def rnd_vector(length_bond=1.0):
    v = np.random.uniform(-1.0, 1.0, 3)
    v /= np.sqrt(np.sum(v**2)) * length_bond
    return v


class MolGraph():
    def __init__(self, bonds: List[List[int]] = [[0, 1]]):
        # Ordering the list of bonds
        self.bonds = sorted([[min(bond), max(bond)] for bond in bonds])
        if not CheckGraph.is_not_gaps(self.bonds):
            raise GapsMolGraphError
        if not CheckGraph.is_simple(self.bonds):
            raise MolGraphSimplicityError
        if not CheckGraph.is_connected(self.bonds):
            raise MolGraphConnectionError
        self.directed = CheckGraph.is_directed(self.bonds)
        # Searchig for max index in the bond list
        self.num_beads = max([bond[1] for bond in bonds]) + 1
        self.num_bonds = len(self.bonds)
        self.cyclical = (self.num_bonds >= self.num_beads)

    def __str__(self):
        return f"""
            Num_beads = {self.num_beads} 
            Num_bonds = {self.num_bonds}
            Cyclical = {self.cyclical}
            Directed = {self.directed}            
            """

    def get_coord(
            self, x0: float, y0: float, z0: float,
            bond_length: float, box: Box, periodic: bool = True):
        """Creating coordinates according the list 

        Returns:
            3 * ndarray: x,y,z - coordinates 
        """
        x = np.zeros(self.num_beads)
        y = np.zeros(self.num_beads)
        z = np.zeros(self.num_beads)
        x[0] = x0
        y[0] = y0
        z[0] = z0
        if self.directed:
            for bond in self.bonds:
                v = rnd_vector(length_bond=bond_length)
                x[bond[1]] += v[0]
                y[bond[1]] += v[1]
                z[bond[1]] += v[2]
        else:
            pass
        return x, y, z


class CheckGraph():
    def is_not_gaps(bonds: List[List[int]]) -> bool:
        nodes = list(set([bond[0] for bond in bonds] + [bond[1]
                     for bond in bonds]))
        if all([i >= 0 for i in nodes]):
            return len(nodes) == (max(nodes) + 1)
        else:
            raise NegativeValueError

    def is_simple(bonds: List[List[int]]) -> bool:
        new_bonds = [(bond[0], bond[1]) for bond in bonds] + \
            [(bond[1], bond[0]) for bond in bonds]
        return len(new_bonds) == len(list(set(new_bonds)))

    def is_connected(bonds: List[List[int]]) -> bool:
        label = dict()
        for bead in bonds:
            for i in range(len(bead)):
                if not bead[i] in label:
                    label[bead[i]] = 0
        counter = 0
        cluster = dict()
        for bond in bonds:
            if label[bond[0]] == label[bond[1]]:
                if label[bond[0]] == 0:
                    counter += 1
                    label[bond[0]] = counter
                    label[bond[1]] = counter
                    cluster[counter] = [bond[0], bond[1]]
            else:
                if label[bond[0]] == 0 and label[bond[1]] != 0:
                    label[bond[0]] = label[bond[1]]
                    cluster[label[bond[0]]].append(bond[0])
                elif label[bond[1]] == 0 and label[bond[0]] != 0:
                    label[bond[1]] = label[bond[0]]
                    cluster[label[bond[1]]].append(bond[1])
                else:
                    minimum = min(label[bond[1]], label[bond[0]])
                    maximum = max(label[bond[1]], label[bond[0]])
                    cluster[minimum] = cluster[minimum] + cluster[maximum]
                    for clust in cluster[maximum]:
                        label[clust] = minimum
                    cluster.pop(maximum)
        return len(cluster) == 1

    def is_directed(bonds: List[List[int]]) -> bool:
        nodes = list(set([bond[0] for bond in bonds] + [bond[1]
                     for bond in bonds]))
        painted = set()
        painted.add(bonds[0][0])
        for bond in bonds:
            if bond[0] in painted:
                painted.add(bond[1])
        return len(nodes) == len(list(painted))


if __name__ == '__main__':
    box = Box(10, 10, 10)
    bonds_1 = [[0, 1], [1, 2], [2, 4], [2, 3], [2, 5]]
    bonds_2 = [[0, 1], [1, 2], [3, 4], [4, 5], [5, 6]]
    graph = MolGraph(bonds_1)
    print(graph)
    print(graph.num_beads)
    print(graph.bonds)
