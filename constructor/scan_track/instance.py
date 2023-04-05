from scan_track import ReadTrack
import numpy as np
from clusterization import stratification, neighbourhood, neighbourhood2
from periodic_box import Box

RT = ReadTrack('trajectory_sample')
while RT.one_step():
    print(RT.time_step)
    x, y, z = [], [], []
    for i in range(RT.num_atoms):
        if RT.btype[i] == 1:
            x.append(RT.x[i])
            y.append(RT.y[i])
            z.append(RT.z[i])
    x, y, z = np.array(x), np.array(y), np.array(z)
    bonds1 = neighbourhood(x, y, z, radius=1, box=RT.box)
    print(len(bonds1))
    # bonds2 = neighbourhood2(x, y, z, radius=1, box=RT.box)
    clusters = stratification(len(x), bonds1)
    print(len(clusters))
    # print(len(bonds2))
    
        
    