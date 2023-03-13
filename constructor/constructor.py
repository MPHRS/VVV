from typing import Dict, Final, List, Optional, Tuple

import numpy as np
from bondset import Bondtype
from check_graph import CheckGraph
from exceptions import (FixedDictError, FixedOutBoxError, FixedRootError,
                        GapsMolGraphError, MolGraphConnectionError,
                        MolGraphSimplicityError, EmptyGraphError)
from periodic_box import Box

BOND_LENGTH: Final[float] = (1./3.) ** (1./3.)

def rnd_vector(length: float = BOND_LENGTH) -> np.ndarray:
    """
    Generates a random 3D vector of a given length

    Args:
        length (float, optional): Defaults to LENGTH_BOND = (1/3)^(1/3) ~ 0.693..

    Returns:
        np.ndarray: random 3D vector of any given length
    """
    v = np.random.uniform(-1.0, 1.0, 3)
    v /= np.sqrt(np.sum(v**2)) * length
    return v


class MolGraph():
    """
    Creation, building and processing of a molecular graph
        Graph must be simple and fully-connected

    Attributes:
        self.num_bonds (int): number of bonds (edges) <- input
        self.num_beads (int): number of beads (nodes)
        self.cyclical (bool): True if graph is cyclical, False otherwise
        self.directed (bool): True if graph is directed, False otherwise
    """
    def __init__(self, bonds: Bondtype, sort: bool = True) -> None:
        """
        Args:
            bonds (List[Tuple[int,int]]): list of bonded node ids 
            sort (bool, optional): Should the graph be sorted? Defaults to True.

        Raises:
            GapsMolGraphError: Gaps in indexation
            MolGraphSimplicityError: Graph is not simple
            MolGraphConnectionError: Graph is not connected
        """
        # Sorting the list of bonds and id in bonds
        if sort:
            self.bonds = sorted([(min(bond), max(bond)) for bond in bonds])
        # Check graph for critical exceptions
        if not self.bonds:
            raise EmptyGraphError
        if not CheckGraph.is_not_gaps(self.bonds):
            raise GapsMolGraphError
        if not CheckGraph.is_simple(self.bonds):
            raise MolGraphSimplicityError
        if not CheckGraph.is_connected(self.bonds):
            raise MolGraphConnectionError
        # Searchig for max index in the bond list
        self.num_beads: int = max([max(bond[0],bond[1]) for bond in bonds]) + 1
        self.num_bonds: int = len(self.bonds)
        # Basic properties for building a graph
        self.cyclical: bool = (self.num_bonds >= self.num_beads)
        self.directed: bool = CheckGraph.is_directed(self.bonds)

    def __str__(self):
        return f"""
            Num_beads = {self.num_beads} 
            Num_bonds = {self.num_bonds}
            Cyclical = {self.cyclical}
            Directed = {self.directed}            
            """

    def get_coords(self, fixed_coords: Optional[Dict[int, Tuple[float,float,float]]],
                   box: Box, 
                   bond_length: float = BOND_LENGTH, 
                   periodic: bool = True) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        
        x = np.zeros(self.num_beads)
        y = np.zeros(self.num_beads)
        z = np.zeros(self.num_beads)

        only_id0_fixed: bool = False
        if fixed_coords:
            if 0 in fixed_coords:
                if len(fixed_coords) == 1:
                    only_id0_fixed = True
            else:
                raise FixedRootError
            if any([(i < 0 and i >= self.num_beads) for i in fixed_coords]):
                raise FixedDictError 
            for id in fixed_coords:
                x[id], y[id], z[id] = fixed_coords[id]
                if not box.check_in_box(x[id], y[id], z[id]):
                    raise FixedOutBoxError
        else:
            x[0] = np.random.uniform(-box.x / 2, box.x / 2)
            y[0] = np.random.uniform(-box.y / 2, box.y / 2)
            z[0] = np.random.uniform(-box.z / 2, box.z / 2)
            only_id0_fixed = True

        if only_id0_fixed and self.directed and (not self.cyclical):
            for bond in self.bonds:             
                label_to_break = True
                while label_to_break:
                    v = rnd_vector(length=bond_length)
                    xt = x[bond[0]] + v[0]
                    yt = y[bond[0]] + v[1]
                    zt = z[bond[0]] + v[2]
                    if not box.check_in_box(xt, yt, zt):
                        if periodic:
                            xt, yt, zt = box.periodic_correct(xt, yt, zt)
                        else:
                            label_to_break = False
                    if label_to_break:
                        x[bond[1]] = xt
                        y[bond[1]] = yt
                        z[bond[1]] = zt 
                        break
        else:
            pass
    
        return x, y, z
    
class Chain(MolGraph):
    def __init__(self, n_beads: int):
        self.n_beads = n_beads
        self.bonds: Bondtype = [(0, 1), (1, 2)]
        super().__init__(self.bonds)

    

if __name__ == '__main__':
    box = Box(10, 10, 10)
    graph = MolGraph([(0, 1), (1, 2)])
    #graph.get_coords(fixed_coords={0: (1,2,3), 1: (2,3,9), 2: (0,0,0)}, box=box)
    chain = Chain(n_beads=2)
    print(chain.cyclical, chain.num_beads)
    print(chain.get_coords(fixed_coords=None, box=box, periodic=False))
    
    