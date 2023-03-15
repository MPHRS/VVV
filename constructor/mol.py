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
    def __init__(self, n: int, g: int = 0) -> None:
        self.n = n
        self.g = g
        bonds: Bondtype = []
        #### your code
        
        ####
        super().__init__(bonds)
            
if __name__ == '__main__':
    chain = Chain(n=5)
    print(chain.bonds)        
        
    