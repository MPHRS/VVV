from typing import List, Tuple

import numpy as np
from exceptions import NegativeValueError
from bondset import Bondtype

class CheckGraph():
    """ Pre-check of any molecular graph """

    @staticmethod
    def is_not_gaps(bonds: Bondtype) -> bool: 
        """
        Detects gaps or invalid value in node enum,
        bonds-list can be empty, but node ids must

        i) be enumerated from 0 to max id without gaps,

        ii) contain only non-negative integers

        Args:
            bonds (List[Tuple[int,int]]): list of bonded node ids 

        Raises:
            NegativeValueError: if a negative id is found
        Returns:
            bool: True if there are no gaps, False otherwise
        """    
        nodes = set([bond[0] for bond in bonds] + [bond[1] for bond in bonds])
        if any([i < 0 for i in nodes]):
            raise NegativeValueError
        num_nodes = len(nodes)
        return num_nodes * (num_nodes -1) / 2 == sum(nodes)

    @staticmethod
    def is_simple(bonds: Bondtype) -> bool:
        """
        Checks for the absence of multiple and cyclic edges
        Likes that: (1, 2) and (2, 1), (0, 0), (1, 1) etc.

        Args:
            bonds (List[Tuple[int,int]]): list of bonded node ids

        Returns:
            bool: True it the graph is simple, False otherwise
        """
        new_bonds: Bondtype = bonds + [(bond[1], bond[0]) for bond in bonds]
        return len(new_bonds) == len(set(new_bonds))

    # def is_connected(bonds: List[List[int]]) -> bool:
    #     label = dict()
    #     for bead in bonds:
    #         for i in range(len(bead)):
    #             if not bead[i] in label:
    #                 label[bead[i]] = 0
    #     counter = 0
    #     cluster = dict()
    #     for bond in bonds:
    #         if label[bond[0]] == label[bond[1]]:
    #             if label[bond[0]] == 0:
    #                 counter += 1
    #                 label[bond[0]] = counter
    #                 label[bond[1]] = counter
    #                 cluster[counter] = [bond[0], bond[1]]
    #         else:
    #             if label[bond[0]] == 0 and label[bond[1]] != 0:
    #                 label[bond[0]] = label[bond[1]]
    #                 cluster[label[bond[0]]].append(bond[0])
    #             elif label[bond[1]] == 0 and label[bond[0]] != 0:
    #                 label[bond[1]] = label[bond[0]]
    #                 cluster[label[bond[1]]].append(bond[1])
    #             else:
    #                 minimum = min(label[bond[1]], label[bond[0]])
    #                 maximum = max(label[bond[1]], label[bond[0]])
    #                 cluster[minimum] = cluster[minimum] + cluster[maximum]
    #                 for clust in cluster[maximum]:
    #                     label[clust] = minimum
    #                 cluster.pop(maximum)
    #     return len(cluster) == 1

    # def is_directed(bonds: List[List[int]]) -> bool:
    #     nodes = list(set([bond[0] for bond in bonds] + [bond[1]
    #                  for bond in bonds]))
    #     painted = set()
    #     painted.add(bonds[0][0])
    #     for bond in bonds:
    #         if bond[0] in painted:
    #             painted.add(bond[1])
    #     return len(nodes) == len(list(painted))
    
if __name__ == '__main__':
    bonds0: List[Tuple[int,int]] = []
    bonds1 = [(1, 2), (2, 1), (0, 5), (5, 4)]
    bonds2 = [(1, 2), (3, 3), (1, 5), (5, 4)]
    bonds3 = [(1, 2), (2, 3), (-1, 5), (5, 4)]
    print(CheckGraph.is_simple(bonds0))
    print(CheckGraph.is_simple(bonds1))
    print(CheckGraph.is_simple(bonds2))
    try:
        print(CheckGraph.is_not_gaps(bonds3))
    except NegativeValueError as err:
        print(err)
        