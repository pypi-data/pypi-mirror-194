import numpy as np
import datetime
import random


def initial_stru(P, NX, NY, NZ, ion_num):  
    ''' 
    structure initialization
        Parameters:
            P(float): Inorganic doping concentration
            NX(int): matrix size
            NY(int): matrix size
            NZ(int): matrix size
            ion_num(int): Number of walkers migrated
        Returns:
            coord_doped_label(int):The markers corresponding to the logical coordinates of the skeleton
            ion_logic_coor(list): Initialized walkers logic coordinates
            initial_cell_coor(list): Physical coordinates of all points in the system
    '''

    x, y, z = np.mgrid[0:NX, 0:NY, 0:NZ]
    x1, y1, z1 = np.mgrid[0:NX - 1, 0:NY - 1, 0:NZ - 1]

    # framework_coords: logical coordinates of all skeleton ions in the system
    framework_coords = np.zeros((NX, NY, NZ, 3), dtype=int)
    framework_coords[:, :, :, 0] = x
    framework_coords[:, :, :, 1] = y
    framework_coords[:, :, :, 2] = z

    # site_logic_coord:logical coordinates of the vacancy
    site_logic_coord = np.zeros((NX - 1, NY - 1, NZ - 1, 3),dtype=int)
    site_logic_coord[:, :, :, 0] = x1
    site_logic_coord[:, :, :, 1] = y1
    site_logic_coord[:, :, :, 2] = z1

    # Reshaping site_logic_coord into a one-dimensional array
    vacancysite_logic_coor1 = site_logic_coord.reshape((NX - 1) * (NY - 1) * (NZ - 1), 3)

    # occupy_site_coord:The vacancy number occupied by ions
    occupy_site_coord = np.random.choice((NX - 1) * (NY - 1) * (NZ - 1), ion_num, replace=False)
    ion_logic_coor = vacancysite_logic_coor1[occupy_site_coord]
 

    # occupy_number:Representing the number of skeleton ions doped by inorganic matter
    occupy_number = np.random.choice(NX * NY * NZ, int(P * NX * NY * NZ), replace=False)

    coord_doped_label = np.zeros((NX, NY, NZ, 1), dtype=int)

    cllist = coord_doped_label.reshape((NX * NY * NZ))
    # The corresponding label of cllist is marked as 1 or 0 according to the doped skeleton number.
    cllist[occupy_number] = 1
    initial_cell_coor = np.zeros(ion_num * 3, dtype=int).reshape(ion_num, 3)


    return coord_doped_label, ion_logic_coor,initial_cell_coor  


if __name__ == '__main__':
    time1 = datetime.datetime.now()
    N = 5
    NX = NY = NZ = N
    P = 0.3

    ion_num = 5
    tao_a = 2
    tao_b = 20000
    tao_c = 5000
    rate_hopping_a = float(1 / tao_a)
    rate_hopping_b = float(1 / tao_b)
    rate_hopping_c = float(1 / tao_c)

    aa = initial_stru(P, NX, NY, NZ, ion_num)

    print('第一个函数没问题')

    time2 = datetime.datetime.now()
    print('所花时间：', time2 - time1)
