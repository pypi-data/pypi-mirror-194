import numpy as np

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

def dos(DOS):
    ARR = []
    ELE = []
    elements = []
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
        elements = elements + [pdos+'-'+i for i in lines[0].split()[1:]]

    return ARR, ELE, elements

def bands(PLOT):
    with open(PLOT, "r") as main_file:
        lines = main_file.readlines()

    str0 = lines[0].split()
    if len(str0) == 2 and str0[1] == "Energy-Level(eV)":
        nkps = lines[1].split()
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

