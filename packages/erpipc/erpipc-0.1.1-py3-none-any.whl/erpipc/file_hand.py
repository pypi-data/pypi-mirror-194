import pandas as pd
import itertools
import math

import numpy as np
import random
import multiprocessing
import os, sys
import time
import os

import copy
from multiprocessing import Process



def mkdir(path):
    '''create file'''
    path = path.strip()
    path = path.rstrip("\\")

    # Determine whether the path exists, Existence true, not exist False
    isExists = os.path.exists(path)
    # If not, create a directory
    if not isExists:
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        # If the directory exists, it is not created and prompts that the directory already exists
        print(path + ' 目录已存在')
        return False  

