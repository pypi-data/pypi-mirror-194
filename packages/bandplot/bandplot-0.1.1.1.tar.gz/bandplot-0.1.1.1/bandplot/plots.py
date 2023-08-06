import matplotlib.pyplot as plt

def Noneispin(EXPORT, figsize, vertical, arr, bands, ticks, labels, linestyle, legend, location, color):
    plt.figure(figsize=figsize)
    if len(color) == 0:
        color = ['r']

    plt.plot(arr, bands.T, color=color[0], linewidth=0.8, linestyle=linestyle[0])
    plt.tick_params(axis='y', which='minor', color='gray')

    plt.axhline(linewidth=0.5, linestyle=(0, (3, 2, 1, 2, 1, 2)), c='gray')
    if len(ticks) > 2:
        ticks[0],ticks[-1] = arr[0],arr[-1]
        for i in ticks[1:-1]:
            plt.axvline(i, linewidth=0.5, linestyle=(0, (3, 2, 1, 2, 1, 2)), c='gray')

    plt.xticks(ticks,labels)
    plt.legend(legend, frameon=False, prop={'size':'medium'}, loc=location)
    plt.xlim(arr[0], arr[-1])
    plt.ylim(vertical)
    plt.ylabel('Energy (eV)')
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def Ispin(EXPORT, figsize, vertical, arr, bands, ticks, labels, linestyle, legend, location, color):
    plt.figure(figsize=figsize)
    if len(color) < 2:
        color = ['r', 'k']

    if len(linestyle) < 2:
        linestyle = ['-', '-.']

    p_up = plt.plot(arr, bands[0].T, color=color[0], linewidth=0.8, linestyle=linestyle[0])
    p_do = plt.plot(arr, bands[1].T, color=color[1], linewidth=0.8, linestyle=linestyle[1])
    plt.legend([p_up[0], p_do[0]], ['up', 'down'], frameon=False, prop={'style':'italic', 'size':'medium'}, alignment='left', loc=location, title=legend[0], title_fontproperties={'size':'medium'})
    plt.tick_params(axis='y', which='minor', color='gray')
    plt.axhline(linewidth=0.5, linestyle=(0, (3, 2, 1, 2, 1, 2)), c='gray')
    if len(ticks) > 2:
        ticks[0],ticks[-1] = arr[0],arr[-1]
        for i in ticks[1:-1]:
            plt.axvline(i, linewidth=0.5, linestyle=(0, (3, 2, 1, 2, 1, 2)), c='gray')

    plt.xlim(arr[0], arr[-1])
    plt.ylim(vertical)
    plt.xticks(ticks,labels)
    plt.ylabel('Energy (eV)')
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def Dispin(EXPORT, figsize, vertical, arr, bands, ticks, labels, linestyle, legend, location, color):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    fig.subplots_adjust(wspace=0.0)
    if len(color) < 2:
        color = ['r', 'k']

    if len(linestyle) < 2:
        linestyle = ['-', '-.']

    ax1.plot(arr, bands[0].T, color=color[0], linewidth=0.8, linestyle=linestyle[0])
    ax2.plot(arr, bands[1].T, color=color[1], linewidth=0.8, linestyle=linestyle[1])
    ax1.legend(['up'], frameon=False, prop={'style':'italic', 'size':'medium'}, alignment='left', loc=location, title=legend[0], title_fontproperties={'size':'medium'})
    ax2.legend(['down'], frameon=False, prop={'style':'italic', 'size':'medium'}, alignment='left', loc=location)
    ax1.tick_params(axis='y', which='minor', color='gray')
    ax2.tick_params(axis='y', which='minor', color='gray')

    ax1.axhline(linewidth=0.5, linestyle=(0, (3, 2, 1, 2, 1, 2)), c='gray')
    ax2.axhline(linewidth=0.5, linestyle=(0, (3, 2, 1, 2, 1, 2)), c='gray')
    ax2.set_yticklabels([])
    if len(ticks) > 2:
        ticks[0],ticks[-1] = arr[0],arr[-1]
        for i in ticks[1:-1]:
            ax1.axvline(i, linewidth=0.5, linestyle=(0, (3, 2, 1, 2, 1, 2)), c='gray')
            ax2.axvline(i, linewidth=0.5, linestyle=(0, (3, 2, 1, 2, 1, 2)), c='gray')

    ax1.set_xlim(arr[0], arr[-1])
    ax1.set_ylim(vertical)
    ax2.set_xlim(arr[0], arr[-1])
    ax2.set_ylim(vertical)
    ax1.set_xticks(ticks,labels[:-1]+[''])
    ax2.set_xticks(ticks,labels)
    ax1.set_ylabel('Energy (eV)')
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def NoneispinWd(EXPORT, figsize, vertical, horizontal, arr, bands, ticks, labels, darr, dele, index_f, elements, width_ratios, linestyle, legend, location, color):
    fig, (ax1, ax2) = plt.subplots(1, 2, width_ratios=[1-width_ratios, width_ratios], figsize=figsize)
    fig.subplots_adjust(wspace=0.0)
    if len(color) == 0:
        color = ['r']

    ax1.plot(arr, bands.T, color=color[0], linewidth=0.8, linestyle=linestyle[0])
    num = len(index_f)
    if num + 1 > len(color):
        color = color + [''] * (num + 1 - len(color))

    if num + 1 > len(linestyle):
        linestyle = linestyle + ['-'] * (num + 1 - len(linestyle))

    for i in range(num):
        if color[i+1]:
            ax2.plot(dele[index_f[i][0]].T[index_f[i][1]], darr[index_f[i][0]], linewidth=0.8, linestyle=linestyle[i+1], color=color[i+1])
        else:
            ax2.plot(dele[index_f[i][0]].T[index_f[i][1]], darr[index_f[i][0]], linewidth=0.8, linestyle=linestyle[i+1])

    ax1.legend(legend, frameon=False, prop={'size':'small'}, loc=location)
    ax1.tick_params(axis='y', which='minor', color='gray')
    ax2.minorticks_on()
    ax2.tick_params(axis='both', which='minor', color='gray')
    ax2.set_yticklabels([])
    ax2.legend(elements, frameon=False, prop={'size':'small'}, alignment='left', loc=location, title="Density of states", title_fontproperties={'size':'small'})
    ax1.axhline(linewidth=0.5, linestyle=(0, (3, 2, 1, 2, 1, 2)), c='gray')
    ax2.axhline(linewidth=0.5, linestyle=(0, (3, 2, 1, 2, 1, 2)), c='gray')
    ax2.axvline(linewidth=0.5, linestyle=(0, (3, 2, 1, 2, 1, 2)), c='gray')
    if len(ticks) > 2:
        ticks[0],ticks[-1] = arr[0],arr[-1]
        for i in ticks[1:-1]:
            ax1.axvline(i,linewidth=0.5,linestyle=(0, (3, 2, 1, 2, 1, 2)),c='gray')

    ax1.set_xlim(arr[0], arr[-1])
    ax1.set_ylim(vertical)
    ax2.set_xlim(horizontal)
    ax2.set_ylim(vertical)
    ax1.set_xticks(ticks,labels)
    ax2.tick_params(axis='x', labelsize='x-small', labelcolor='dimgray', labelrotation=-90, pad=1.5)
    ax1.set_ylabel('Energy (eV)')
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def IspinWd(EXPORT, figsize, vertical, horizontal, arr, bands, ticks, labels, darr, dele, index_f, elements, width_ratios, linestyle, legend, location, color):
    fig, (ax1, ax2) = plt.subplots(1, 2, width_ratios=[1-width_ratios, width_ratios], figsize=figsize)
    fig.subplots_adjust(wspace=0.0)
    if len(color) < 2:
        color = ['r', 'k']

    if len(linestyle) < 2:
        linestyle = ['-', '-.']

    p_up = ax1.plot(arr, bands[0].T, color=color[0], linewidth=0.8, linestyle=linestyle[0])
    p_do = ax1.plot(arr, bands[1].T, color=color[1], linewidth=0.8, linestyle=linestyle[1])
    ax1.legend([p_up[0], p_do[0]], ['up', 'down'], frameon=False, prop={'style':'italic', 'size':'small'}, alignment='left', loc=location, title=legend[0], title_fontproperties={'size':'small'})
    num = len(index_f)
    if num + 2 > len(color):
        color = color + [''] * (num + 2 - len(color))

    if num + 2 > len(linestyle):
        linestyle = linestyle + ['-'] * (num + 2 - len(linestyle))

    for i in range(num):
        if color[i+2]:
            ax2.plot(dele[index_f[i][0]].T[index_f[i][1]], darr[index_f[i][0]], linewidth=0.8, linestyle=linestyle[i+2], color=color[i+2])
        else:
            ax2.plot(dele[index_f[i][0]].T[index_f[i][1]], darr[index_f[i][0]], linewidth=0.8, linestyle=linestyle[i+2])

    ax1.tick_params(axis='y', which='minor', color='gray')
    ax2.minorticks_on()
    ax2.tick_params(axis='both', which='minor', color='gray')
    ax2.axvline(linewidth=0.5, linestyle=(0, (3, 2, 1, 2, 1, 2)), c='gray')
    ax2.set_yticklabels([])
    ax2.legend(elements, frameon=False, prop={'size':'small'}, alignment='left', loc=location, title="Density of states", title_fontproperties={'size':'small'})
    ax1.axhline(linewidth=0.5, linestyle=(0, (3, 2, 1, 2, 1, 2)), c='gray')
    ax2.axhline(linewidth=0.5, linestyle=(0, (3, 2, 1, 2, 1, 2)), c='gray')
    if len(ticks) > 2:
        ticks[0],ticks[-1] = arr[0],arr[-1]
        for i in ticks[1:-1]:
            ax1.axvline(i,linewidth=0.5, linestyle=(0, (3, 2, 1, 2, 1, 2)), c='gray')

    ax1.set_xlim(arr[0], arr[-1])
    ax1.set_ylim(vertical)
    ax2.set_xlim(horizontal)
    ax2.set_ylim(vertical)
    ax1.set_xticks(ticks,labels)
    ax2.tick_params(axis='x', labelsize='x-small', labelcolor='dimgray', labelrotation=-90, pad=1.5)
    ax1.set_ylabel('Energy (eV)')
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def DispinWd(EXPORT, figsize, vertical, horizontal, arr, bands, ticks, labels, darr, dele, index_f, elements, width_ratios, linestyle, legend, location, color):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, width_ratios=[0.5*(1-width_ratios), 0.5*(1-width_ratios), width_ratios], figsize=figsize)
    fig.subplots_adjust(wspace=0.0)
    if len(color) < 2:
        color = ['r', 'k']

    if len(linestyle) < 2:
        linestyle = ['-', '-.']

    ax1.plot(arr, bands[0].T, color=color[0], linewidth=0.8, linestyle=linestyle[0])
    ax2.plot(arr, bands[1].T, color=color[1], linewidth=0.8, linestyle=linestyle[1])
    ax1.legend(['up'], frameon=False, prop={'style':'italic', 'size':'small'}, alignment='left', loc=location, title=legend[0], title_fontproperties={'size':'small'})
    ax2.legend(['down'], frameon=False, prop={'style':'italic', 'size':'small'}, alignment='left', loc=location)
    ax1.tick_params(axis='y', which='minor', color='gray')
    ax2.tick_params(axis='y', which='minor', color='gray')
    ax3.minorticks_on()
    ax3.tick_params(axis='both', which='minor', color='gray')
    num = len(index_f)
    if num + 2 > len(color):
        color = color + [''] * (num + 2 - len(color))

    if num + 2 > len(linestyle):
        linestyle = linestyle + ['-'] * (num + 2 - len(linestyle))

    for i in range(num):
        if color[i+2]:
            ax3.plot(dele[index_f[i][0]].T[index_f[i][1]], darr[index_f[i][0]], linewidth=0.8, linestyle=linestyle[i+2], color=color[i+2])
        else:
            ax3.plot(dele[index_f[i][0]].T[index_f[i][1]], darr[index_f[i][0]], linewidth=0.8, linestyle=linestyle[i+2])

    ax3.axvline(linewidth=0.5, linestyle=(0, (3, 2, 1, 2, 1, 2)), c='gray')
    ax2.set_yticklabels([])
    ax3.set_yticklabels([])
    ax3.legend(elements, frameon=False, prop={'size':'small'}, alignment='left', loc=location, title="Density of states", title_fontproperties={'size':'small'})

    ax1.axhline(linewidth=0.5, linestyle=(0, (3, 2, 1, 2, 1, 2)), c='gray')
    ax2.axhline(linewidth=0.5, linestyle=(0, (3, 2, 1, 2, 1, 2)), c='gray')
    ax3.axhline(linewidth=0.5, linestyle=(0, (3, 2, 1, 2, 1, 2)), c='gray')
    if len(ticks) > 2:
        ticks[0],ticks[-1] = arr[0],arr[-1]
        for i in ticks[1:-1]:
            ax1.axvline(i,linewidth=0.5,linestyle=(0, (3, 2, 1, 2, 1, 2)),c='gray')
            ax2.axvline(i,linewidth=0.5,linestyle=(0, (3, 2, 1, 2, 1, 2)),c='gray')

    ax1.set_xlim(arr[0], arr[-1])
    ax1.set_ylim(vertical)
    ax2.set_xlim(arr[0], arr[-1])
    ax2.set_ylim(vertical)
    ax3.set_xlim(horizontal)
    ax3.set_ylim(vertical)
    ax1.set_xticks(ticks,labels[:-1]+[''])
    ax2.set_xticks(ticks,labels)
    ax3.tick_params(axis='x', labelsize='x-small', labelcolor='dimgray', labelrotation=-90, pad=1.5)
    ax1.set_ylabel('Energy (eV)')
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def pdosfiles(EXPORT, figsize, vertical, horizontal, darr, dele, index_f, elements, linestyle, legend, location, exchange, color):
    plt.figure(figsize=figsize)
    plt.minorticks_on()
    plt.tick_params(axis='both', which='minor', color='gray')
    num = len(index_f)
    if num > len(color):
        color = color + [''] * (num - len(color))

    if num > len(linestyle):
        linestyle = linestyle + ['-'] * (num - len(linestyle))

    if exchange:
        for i in range(num):
            if color[i]:
                plt.plot(darr[index_f[i][0]], dele[index_f[i][0]].T[index_f[i][1]], linewidth=0.8, linestyle=linestyle[i], color=color[i])
            else:
                plt.plot(darr[index_f[i][0]], dele[index_f[i][0]].T[index_f[i][1]], linewidth=0.8, linestyle=linestyle[i])

        plt.tick_params(axis='y', labelsize='medium', labelcolor='dimgray')
        plt.xlim(vertical)
        plt.ylim(horizontal)
        plt.xlabel('Energy (eV)')
        plt.ylabel('Density of states, electrons/eV')
    else:
        for i in range(num):
            if color[i]:
                plt.plot(dele[index_f[i][0]].T[index_f[i][1]], darr[index_f[i][0]], linewidth=0.8, linestyle=linestyle[i], color=color[i])
            else:
                plt.plot(dele[index_f[i][0]].T[index_f[i][1]], darr[index_f[i][0]], linewidth=0.8, linestyle=linestyle[i])

        plt.tick_params(axis='x', labelsize='medium', labelcolor='dimgray')
        plt.ylim(vertical)
        plt.xlim(horizontal)
        plt.ylabel('Energy (eV)')
        plt.xlabel('Density of states, electrons/eV')

    plt.axvline(linewidth=0.5, linestyle=(0, (3, 2, 1, 2, 1, 2)), c='gray')
    plt.axhline(linewidth=0.5, linestyle=(0, (3, 2, 1, 2, 1, 2)), c='gray')
    plt.legend(elements, frameon=False, prop={'size':'medium'}, loc=location, title=legend[0], title_fontproperties={'size':'medium'})
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')
