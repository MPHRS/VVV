from typing import (List, Tuple)
import numpy as np
from exceptions import NegativeValueError


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