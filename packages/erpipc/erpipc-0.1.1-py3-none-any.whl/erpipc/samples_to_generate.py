import numpy as np
import datetime
import random
from .initial_structure import initial_stru
from .ions_jumping_process import ions_jump

def sample_generation(jump_num,rate_hopping_a, rate_hopping_b,rate_hopping_c,coor_doped_label,ions_logic_coor,initial_cell_coor1,NX,NY,NZ):
    '''
        Record information during the walkers migration. Returns each step of the walkers ' migration time, each new coordinate.
            Parameters:
                jump_num(int): Total migration steps of walkers
                rate_hopping_a(float): The migration rate of A bond
                rate_hopping_b(float): The migration rate of B bond
                rate_hopping_c(float): The migration rate of C bond
                coor_doped_label(int): The markers corresponding to the logical coordinates of the skeleton
                ions_logic_coor(list):Walkers logical coordinates
                initial_cell_coor1(list)：initial coordinate
                NX(int)：matrix size
                NY(int)：matrix size
                NZ(int)：matrix size

    '''
    all_ion_tao = []
    all_ions_phycoor = []
    logic_ions =[]


    all_initial_phy = ions_logic_coor
    all_ions_phycoor.append(all_initial_phy)
    # logic_ions：Logical coordinates in all ion hopping processes
    logic_ions.append(ions_logic_coor)
    for i in range(0,jump_num):
        if i == 0:
            i_sample = ions_jump(rate_hopping_a, rate_hopping_b,rate_hopping_c,coor_doped_label,ions_logic_coor,initial_cell_coor1,NX,NY,NZ)

        else:
            i_sample = ions_jump(rate_hopping_a, rate_hopping_b, rate_hopping_c, coor_doped_label, ss,qq,NX,NY,NZ)

        ss = i_sample[0] 
        qq = i_sample[1] 

        all_ion_tao.append(i_sample[2])
        all_ions_phycoor.append(i_sample[3])
    # all_ion_tao1：Ion each step
    all_ion_tao1 = np.array(all_ion_tao)
    # all_ions_phycoor1：Physical coordinates in all ion hopping processes
    all_ions_phycoor1 = np.array(all_ions_phycoor)
    

    return all_ions_phycoor1,all_ion_tao1

if __name__ == '__main__':
    time1 = datetime.datetime.now()
    N = 5
    NX = NY = NZ = N
    P = 0.3
    jump_num = 5
    ion_num = 3
    tao_a = 2
    tao_b = 20000
    tao_c = 5000
    rate_hopping_a = float(1 / tao_a)
    rate_hopping_b = float(1 / tao_b)
    rate_hopping_c = float(1 / tao_c)

    aa = initial_stru(P, NX, NY, NZ,ion_num)

    print('第一个函数没问题')

    cc = sample_generation(jump_num,rate_hopping_a, rate_hopping_b,rate_hopping_c,aa[0],aa[1],aa[2],NX,NY,NZ)
    time2 = datetime.datetime.now()
    print('结构初始化时间间隔：', time2 - time1)


