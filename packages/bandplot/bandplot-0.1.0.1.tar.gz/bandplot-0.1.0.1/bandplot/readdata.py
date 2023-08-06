import numpy as np
import re, glob

def klabels(KLABELS):
    with open(KLABELS, "r") as main_file:
        lines = main_file.read()

    lines=lines.split('\n')[1:]
    LABELS=[]
    for i in lines:
        if len(i.split()) == 0:
            break
        LABELS=LABELS+[i.split()]

    if len(LABELS) > 1:
        ticks=[float(i[1]) for i in LABELS]
        labels=[i[0] for i in LABELS]

    return ticks, labels

def s_dosfile(DOS):
    dosfiles = []
    for i in DOS:
        dosfiles = dosfiles + glob.glob(i)

    return dosfiles

def dos(DOS):
    ARR = []
    ELE = []
    s_elements = []
    for pdos in DOS:
        with open(pdos, "r") as main_file:
            lines = main_file.readlines()

        arr = []
        ele = []
        for i in lines[1:]:
            str = i.split()
            if len(str) > 0:
                j = [float(k) for k in str]
                arr.append(j[0])
                ele.append(j[1:])

        ARR.append(np.array(arr))
        ELE.append(np.array(ele).reshape(len(arr),-1))
        s_elements.append([re.sub('.dat|^[A-Za-z]+_', '', pdos)] + lines[0].split()[1:])

    return ARR, ELE, s_elements

def select(s_elements, partial):
    partial = [i for i in partial if i.split()]
    num = len(s_elements)
    if partial:
        if partial[0] == 'all':
            index = []
            for i in range(num):
                for j in range(len(s_elements[i])):
                    if j > 0:
                        index.append((i,j))
        else:
            index = []
            for str0 in partial:
                if str0.islower():
                    str = str0.split(',')
                    for index_i in range(num):
                        for i, j in enumerate(s_elements[index_i]):
                            for s in str:
                                if j == s and i > 0:
                                    index.append((index_i, i))
                else:
                    str = [i for i in str0.split('-') if i.split()]
                    if len(str) == 1:
                        index_i = -1
                        for i, j in enumerate([k[0] for k in s_elements]):
                            if j == str[0]:
                                index_i = i
                        if index_i >= 0:
                            for i in range(len(s_elements[index_i])):
                                if i > 0:
                                    index.append((index_i,i))
                    elif len(str) == 2:
                        index_i = -1
                        for i, j in enumerate([k[0] for k in s_elements]):
                            if j == str[0]:
                                index_i = i
                        if index_i >= 0:
                            for i, j in enumerate(s_elements[index_i]):
                                for s in str[1].split(','):
                                    if j == s and i > 0:
                                        index.append((index_i, i))
    else:
        index = []
        for i in range(num):
            index.append((i, -1))

    labels_elements = []
    for i in index:
        labels_elements.append(s_elements[i[0]][0] + '-$' + s_elements[i[0]][i[1]] + '$')

    index_f = []
    for s in index:
        if s[1] > 0:
            index_f.append((s[0],s[1]-1))
        else:
            index_f.append(s)

    return index_f, labels_elements

def bands(PLOT):
    with open(PLOT, "r") as main_file:
        lines = main_file.readlines()

    str0 = lines[0].split()
    if len(str0) == 2 and str0[1] == "Energy-Level(eV)":
        nkps = re.sub(':', ' ', lines[1]).split()
        m, n = int(nkps[-2]), int(nkps[-1])
        arr = np.zeros(m)
        bands = np.zeros((n,m))
        reverse = False
        for i in lines[2:]:
            str = i.split()
            if i[0] == '#':
                j = int(str[-1])
                k = 0
            elif len(str) > 0:
                if j == 1:
                    arr[k], bands[0,k] = float(str[0]), float(str[1])
                    k += 1
                else:
                    N = j - 1
                    if k == 0:
                        if float(str[0]) == 0:
                            reverse = False
                        else:
                            reverse = True
                    if reverse:
                        K = m-k-1
                    else:
                        K = k
                    bands[N,K] = float(str[1])
                    k += 1
            else:
                pass

        return arr, bands, "Noneispin"
    elif len(str0) == 3 and str0[1] == "Spin-Up(eV)" and str0[2] == "Spin-down(eV)":
        nkps = lines[1].split()
        m, n = int(nkps[-2]), int(nkps[-1])
        arr = np.zeros(m)
        bands = np.zeros((2,n,m))
        reverse = False
        for i in lines[2:]:
            str = i.split()
            if i[0] == '#':
                j = int(str[-1])
                k = 0
            elif len(str) > 0:
                if j == 1:
                    arr[k], bands[0,0,k], bands[1,0,k] = float(str[0]), float(str[1]), float(str[2])
                    k += 1
                else:
                    N = j - 1
                    if k == 0:
                        if float(str[0]) == 0:
                            reverse = False
                        else:
                            reverse = True
                    if reverse:
                        K = m-k-1
                    else:
                        K = k
                    bands[0,N,K], bands[1,N,K] = float(str[1]), float(str[2])
                    k += 1
            else:
                pass

        return arr, bands, "Ispin"
    else:
        pass

def symbols(POSCAR):
    with open(POSCAR, "r") as main_file:
        lines = main_file.readlines()

    symbol = lines[5].split()
    factor = [int(i) for i in lines[6].split()]

    return symbol, factor


