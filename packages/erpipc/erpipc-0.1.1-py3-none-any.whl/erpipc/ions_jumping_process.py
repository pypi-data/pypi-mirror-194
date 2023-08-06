import numpy as np
import datetime
import random
from .initial_structure import initial_stru


def ions_jump(rate_hopping_a, rate_hopping_b, rate_hopping_c, coor_doped_label,ions_logic_coor,initial_cell_coor1,NX,NY,NZ):
    '''
    The migration process of walkers. Return the actual coordinates of each vacancy, the jump probability of each direction around each vacancy.
        Parameters:
            rate_hopping_a(float): The migration rate of A bond
            rate_hopping_b(float): The migration rate of B bond
            rate_hopping_c(float): The migration rate of C bond
            coor_doped_label(int): Markers corresponding to skeleton logical coordinates
            ions_logic_coor(list): Initialized walkers logic coordinates
            initial_cell_coor1(list): Physical coordinates of all points in the system

         Returns:
            all_logic_coor():
            all_cell_coor():
            all_ion_tao():
            all_next_ion_phycoor1():
    '''

    all_cell_logic_coor = []
    all_ion_tao = []
    dxyz = np.array([[0, 0, 0],[0, 0, 1],[0, 1, 0],[0, 1, 1],[1, 0, 0],[1, 0, 1],[1, 1, 0],[1, 1, 1]])

    all_turn = []
    for i in np.arange(len(ions_logic_coor)):  
        i_cor_all = ions_logic_coor[i]+dxyz
        i_doped = np.zeros((8, ), dtype=int)
        for j in range(8):
            if coor_doped_label[i_cor_all[j][0], i_cor_all[j][1],i_cor_all[j][2]] == 1:
                i_doped[j] = 1
        
        #Determine the occupancy of the vacancy in the six directions.
        i_doped_num = np.zeros((6, ), dtype=int)
        i_doped_num[0] = i_doped[4:8].sum()  
        i_doped_num[1] = i_doped[0:4].sum()  
        i_doped_num[2] = i_doped[1:8:2].sum()  
        i_doped_num[3] = i_doped[0:8:2].sum()  
        i_doped_num[4] = i_doped[0:2].sum() + i_doped[4:6].sum()  
        i_doped_num[5] = i_doped[2:4].sum() + i_doped[6:8].sum()  

        #Interpret the jump rate in different directions
        i_tao = []
        for j in np.arange(len(i_doped_num)):
            if i_doped_num[j] == 0:
                i_tao = np.append(i_tao, rate_hopping_c)  
                
            elif i_doped_num[j] == 4:
                i_tao = np.append(i_tao, rate_hopping_b)  
                
            else:
                i_tao = np.append(i_tao, rate_hopping_a)  
               

        tao_i_sum = i_tao.sum()
        random_decimals = random.uniform(0, 1)
        W_R = tao_i_sum * random_decimals
      
        #walkers algorithm for selecting jumps
        if 0 <= W_R and W_R < i_tao[0]:
            turn_n = 'front'
            choose_n = i_tao[0]
            cell_logic_coor = np.array(
                [np.divmod(ions_logic_coor[i][0] + 1, NX - 1), np.divmod(ions_logic_coor[i][1], NY - 1),
                 np.divmod(ions_logic_coor[i][2], NZ - 1)]).T

        elif i_tao[0] <= W_R and W_R < i_tao[0:2].sum():
            turn_n = 'behind'
            choose_n = i_tao[1]
            cell_logic_coor = np.array(
                [np.divmod(ions_logic_coor[i][0] - 1, NX - 1), np.divmod(ions_logic_coor[i][1], NY - 1),
                 np.divmod(ions_logic_coor[i][2], NZ - 1)]).T

        elif i_tao[0:2].sum() <= W_R and W_R < i_tao[0:3].sum():
            turn_n = 'up'
            choose_n = i_tao[2]
            cell_logic_coor = np.array(
                [np.divmod(ions_logic_coor[i][0], NX - 1), np.divmod(ions_logic_coor[i][1], NY - 1),
                 np.divmod(ions_logic_coor[i][2] + 1, NZ - 1)]).T

        elif i_tao[0:3].sum() <= W_R and W_R < i_tao[0:4].sum():
            turn_n = 'down'
            choose_n = i_tao[3]
            cell_logic_coor = np.array(
                [np.divmod(ions_logic_coor[i][0], NX - 1), np.divmod(ions_logic_coor[i][1], NY - 1),
                 np.divmod(ions_logic_coor[i][2] - 1, NZ - 1)]).T

        elif i_tao[0:4].sum() <= W_R and W_R < i_tao[0:5].sum():
            turn_n = 'left'
            choose_n = i_tao[4]
            cell_logic_coor = np.array(
                [np.divmod(ions_logic_coor[i][0], NX - 1), np.divmod(ions_logic_coor[i][1] - 1, NY - 1),
                 np.divmod(ions_logic_coor[i][2] + 1, NZ - 1)]).T

        elif i_tao[0:5].sum() <= W_R and W_R < i_tao[:].sum():
            turn_n = 'right'
            choose_n = i_tao[5]
            cell_logic_coor = np.array(
                [np.divmod(ions_logic_coor[i][0], NX - 1), np.divmod(ions_logic_coor[i][1] + 1, NY - 1),
                 np.divmod(ions_logic_coor[i][2], NZ - 1)]).T

        # Jump probability of ion jump direction      
        all_turn.append(turn_n)  
        # New logical coordinates of ions
        all_cell_logic_coor.append(cell_logic_coor) 
        # The time step of all ions jumping one flower
        all_ion_tao = np.append(all_ion_tao, 1 / choose_n)  

    all_cell_logic_coor1 = np.array(all_cell_logic_coor)
    all_cell_coor = all_cell_logic_coor1[:,0]
    all_logic_coor = all_cell_logic_coor1[:,1]
    # New ion physical coordinates
    all_next_ion_phycoor1 = all_logic_coor + (NZ-1)*(all_cell_coor+initial_cell_coor1)

    return all_logic_coor, all_cell_coor,all_ion_tao, all_next_ion_phycoor1


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

    bb = ions_jump(rate_hopping_a, rate_hopping_b, rate_hopping_c, aa[0],aa[1], aa[2],NX,NY,NZ)
    print('第二个函数没问题')
    time2 = datetime.datetime.now()
    print('所花时间：', time2 - time1)

