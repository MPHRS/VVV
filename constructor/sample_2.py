import numpy as np
from bondset import Bondtype
from dpd_files import print_bonds, print_coord, print_ent_file
from mol import Brush
from periodic_box import Box
import os
import shutil
import time
from scan_track.scan_track import ReadTrack
from scan_track.clusterization import stratification, neighbourhood


def main(m, n, l_end_ch, pd):
    """
    num_ch =  number of chains
    box_size = box size
    m =  spacer length
    pd = polymerization degree
    n = side chain length
    q = number of side chains grafting into one point
    n_end_ch = number of ending chains
    l_end_ch = length of ending chains
    """
    num_ch = 400 #number of chains    TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTese
    q = 1 #number of side chains grafting into one point
    n_end_ch = 2 #number of ending chains
    box_size = (num_ch*(pd * m + m * n * q + n_end_ch * l_end_ch) / 3) ** (1 / 3)
    box = Box(x=box_size, y=box_size, z=box_size)
    x = np.array([])
    y = np.array([])
    z = np.array([])
    b_type = np.array([], dtype=int)
    bonds: Bondtype = []
    b_type = []
    brush = Brush(pd=pd, m=m, n=n, q=q, n_end_ch=n_end_ch, l_end_ch=l_end_ch)
    cur = 1
    for i in range(num_ch):
        (x_t, y_t, z_t) = brush.get_coords(box=box)
        for tp in brush.types:
            b_type.append(tp)
        b = [(bond[0] + cur, bond[1] + cur) for bond in brush.bonds]
        bonds += b
        cur += brush.num_beads 
        x = np.hstack([x, x_t])
        y = np.hstack([y, y_t])
        z = np.hstack([z, z_t])
       
    print_coord(box, x, y, z, b_type)
    print_bonds(box=box, num_atoms=len(x), bonds=bonds)
    print_ent_file(x=x, y=y, z=z, b_type=b_type)




if __name__ == '__main__':
    with open("CONTR", "r") as contr:
        lines = contr.readlines()
    num_step = int(lines[4].split("|")[0].strip())
    num_snapshot = int(lines[5].split("|")[0].strip())
    num_of_snapshots = num_step//num_snapshot
    all_n = [4, 8, 12, 16, 20]
    all_l_end_ch = [2, 4, 8, 16, 20]
    length_of_B_block  = 75
    m_and_pd = {'m':[], 'pd':[]}
    for i in range(1,length_of_B_block + 1):
        for j in range(1,length_of_B_block + 1):
            if i*j == length_of_B_block:
                m_and_pd['m'].append(i)
                m_and_pd['pd'].append(j)    
    if not os.path.isdir('OUTPUT_DATA'):
        os.mkdir('OUTPUT_DATA')
    os.chdir('OUTPUT_DATA')
    number_of_using = 1
    if os.path.exists('Output_README.txt'):
        with open('Output_README.txt', 'r') as f:
            for line in f:
                if line.startswith('*'):
                    number_of_using += 1

    with open('Output_README.txt', 'a') as output_file:
        output_file.write("*************************************************************************\n")
        output_file.write(f"Start {number_of_using} code execution\n")
        for n in all_n:
            simul = [f"Simulation for following parametrs: n= {n},"]
            if not os.path.isdir(f'n=={n}'): 
                os.mkdir(f'n=={n}')
            os.chdir(f'n=={n}')    
            for i in range(len(m_and_pd['m'])):
                m = m_and_pd['m'][i]
                pd = m_and_pd['pd'][i]
                simul.append(f" m={m}, pd={pd},")
                if not os.path.isdir(f'm={m}_pd={pd}'):
                    os.mkdir(f'm={m}_pd={pd}')
                os.chdir(f'm={m}_pd={pd}')
                for l_end_ch in all_l_end_ch:
                    simul.append(f" l_end_ch={l_end_ch}")                                       
                    if not os.path.isdir(f'l_end_ch={l_end_ch}'):
                        os.mkdir(f'l_end_ch={l_end_ch}')
                    os.chdir(f'l_end_ch={l_end_ch}')
                    ll = "".join(simul)
                    clusters = []
                    if os.path.exists('TRACK'):
                        output_file.write(f'{ll} has already been executed\n')
                    else:
                        main(m=m, n=n, l_end_ch=l_end_ch, pd=pd)
                        shutil.copy('../../../../FIELD', 'FIELD')
                        shutil.copy('../../../../CONTR', 'CONTR')
                        shutil.copy('../../../../dpd.exe', 'dpd.exe')
                        start_time = time.time()
                        os.system(command='.\dpd.exe &')
                        while True:
                            time.sleep(5)
                            files = [f for f in os.listdir(os.getcwd()) if f.endswith(".ent")]
                            if len(files) >= num_of_snapshots + 2:
                                break
                        end_time = time.time()
                        start_time_clu = time.time()
                        RT = ReadTrack(os.getcwd())
                        with open("Clusterization.txt", "w")  as cl:
                            while RT.one_step():
                                x, y, z = [], [], []
                                for i in range(RT.num_atoms):
                                    if RT.btype[i] == 1:
                                        x.append(RT.x[i])
                                        y.append(RT.y[i])
                                        z.append(RT.z[i])
                                x, y, z = np.array(x), np.array(y), np.array(z)
                                bonds = neighbourhood(x, y, z, radius=1, box=RT.box)
                                clusters.append(stratification(len(x), bonds))
                                cl.write(f"Number of steps = {RT.time_step} : number of clusters = {len(clusters[-1])}\n")  
                            cl.write("Clusters evolution:\n")
                            for i in clusters:
                                cl.write(f"\n{i}\n")
                        end_time_clu = time.time()
                        output_file.write(f"{ll} has been executed. The time is {(end_time - start_time)/60:.2f} mins.\n")
                        output_file.write(f"(The time for clusterization is {(end_time_clu - start_time_clu)/60:.2f} mins.)\n")                            
                    os.chdir('../')
                    simul.pop()
                os.chdir('../')
                simul.pop()
            os.chdir('../')
            simul.pop()
            
