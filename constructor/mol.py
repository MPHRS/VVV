from constructor import MolGraph
from bondset import Bondtype


class Chain(MolGraph):
    """
    Chain molecular structure inherited from MolGraph
    
    Args:
        MolGraph (_type_): see constructor.MolGraph
    Initial attribute:
        self.n (int): chain length
    """
    def __init__(self, n: int) -> None:
        if n < 1:
            raise ValueError(f'(n = {n}) set is invalid ')
        self.n = n
        bonds: Bondtype = []
        for i in range(self.n-1):
            bonds.append((i, i+1))
        super().__init__(bonds)
        
class Dendron(MolGraph):
    """
    Dendrit molecular structure inherited from MolGraph
    
    Args:
        MolGraph (_type_): see constructor.MolGraph
    Initial attributes:
        self.n (int): spacer length
        self.g (int): number of generations in dendron
    """
    def __init__(self, n: int, g: int = 0, q: int = 2) -> None:
        if q <= 1 or g < 0 or n < 1:
            raise ValueError(f'(n = {n}, g = {g}, q = {q}) set is invalid ')
        self.n = n
        self.g = g
        self.q = q
        bonds: Bondtype = []
        self.num_spacers: int = (self.q**(self.g) - 1) // (self.q - 1)
        for i in range(self.n):
            bonds.append((i, i+1))
        id0 = 0
        current_id = self.n
        for s in range(self.num_spacers):
            id0 += self.n
            for i in range(self.q):
                for j in range(self.n):
                    current_id += 1
                    if j == 0:
                        bonds.append((id0, current_id))
                    else:
                        bonds.append((current_id-1, current_id))
        super().__init__(bonds, sort = False)
        #super().__init__(bonds)
            
if __name__ == '__main__':
    chain = Chain(n=5)
    print(chain.bonds)
    dendron = Dendron(n=1, g = 2, q = 2)
    print(dendron.bonds)    
    