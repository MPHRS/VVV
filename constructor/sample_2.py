import numpy as np
from bondset import Bondtype
from dpd_files import print_bonds, print_coord, print_fixed
from mol import Brush
from periodic_box import Box

if __name__ == '__main__':
    num_ch = 50 #number of chains
    box_size = (num_ch / 3) ** (1 / 3)

    m = 3 # spacer length
    pd = 2 #polymerization degree
    n = 3 # side chain length
    q = 1 #number of side chains grafting into one point
    n_end_ch = 2 #number of ending chains
    l_end_ch = 2 # length of ending chains 
    
    box = Box(x=box_size, y=box_size, z=box_size)
    x = np.array([])
    y = np.array([])
    z = np.array([])
    b_type = np.array([], dtype=int)
    bonds: Bondtype = []
    fixed_list = []
    b_type = []
    brush = Brush(pd=pd, m=m, n=n, q=q, n_end_ch=n_end_ch, l_end_ch=l_end_ch)
    cur = 1
    for i in range(num_ch):
        cr = ( 0.5 *  box_size * np.random.rand(), 0.5 *  box_size * np.random.rand(), 0.5 *  box_size * np.random.rand())
        (x_t, y_t, z_t) = brush.get_coords(box=box, fixed_coords={ 0: cr })
        fixed_list.append(cr)
        for tp in brush.types.values():
            b_type.append(tp)
        b = [(bond[0] + cur, bond[1] + cur) for bond in brush.bonds]
        bonds += b
        cur += brush.num_beads 
        x = np.hstack([x, x_t])
        y = np.hstack([y, y_t])
        z = np.hstack([z, z_t])   
    print_coord(box, x, y, z, b_type)
    print_bonds(box=box, num_atoms=len(x), bonds=bonds)
    print_fixed(fixed_list)

