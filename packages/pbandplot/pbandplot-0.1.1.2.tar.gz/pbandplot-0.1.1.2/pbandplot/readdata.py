import numpy as np

def bands(PLOT):
    with open(PLOT, "r") as main_file:
        lines = main_file.readlines()
    ticks = [float(i) for i in lines[1].split()[1:]]
    arr = []
    fre = []
    k = 0
    for i in lines[2:]:
        str = i.split()
        if len(str) > 0:
            j = float(str[0])
            if j == 0.0:
                k += 1
            if k == 1:
                arr.append(j)
                fre.append(float(str[1]))
            else:
                fre.append(float(str[1]))
    arr = np.array(arr)
    fre = np.array(fre).reshape(-1,len(arr))
    return arr, fre, ticks

def dos(DOS):
    with open(DOS, "r") as main_file:
        lines = main_file.readlines()
    arr = []
    ele = []
    for i in lines[1:]:
        str = i.split()
        if len(str) > 0:
            j = [float(k) for k in str]
            arr.append(j[0])
            ele.append(j[1:])
    arr = np.array(arr)
    ele = np.array(ele).reshape(len(arr),-1)
    return arr, ele

def symbols(POSCAR):
    with open(POSCAR, "r") as main_file:
        lines = main_file.readlines()
    symbol = lines[5].split()
    factor = [int(i) for i in lines[6].split()]
    return symbol, factor

