import matplotlib.pyplot as plt

def Noneispin(arr, bands, ticks, EXPORT, labels, figsize, vertical, legend, color):
    plt.figure(figsize=figsize)
    plt.plot(arr,bands.T,color='%s'%color,linewidth=0.8,linestyle='-')
    plt.tick_params(axis='y', which='minor', color='gray')

    plt.axhline(linewidth=0.8,linestyle='-.',c='dimgray')
    if len(ticks) > 2:
        ticks[0],ticks[-1] = arr[0],arr[-1]
        for i in ticks[1:-1]:
            plt.axvline(i,linewidth=0.4,linestyle='-.',c='gray')

    plt.xticks(ticks,labels)
    plt.legend(legend, frameon=False, prop={'size':'medium'}, loc='best')
    plt.xlim(arr[0], arr[-1])
    plt.ylim(vertical)
    plt.ylabel('Energy (eV)')
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def Ispin(arr, bands, ticks, EXPORT, labels, figsize, vertical, legend, color):
    plt.figure(figsize=figsize)
    p_up = plt.plot(arr,bands[0].T,color='%s'%color,linewidth=0.8,linestyle='-')
    p_do = plt.plot(arr,bands[1].T,color='k',       linewidth=0.9,linestyle=':')
    plt.legend([p_up[0], p_do[0]], ['up', 'down'], frameon=False, prop={'style':'italic', 'size':'medium'}, alignment='left',  loc='best', title=legend[0], title_fontproperties={'size':'medium'})
    plt.tick_params(axis='y', which='minor', color='gray')

    plt.axhline(linewidth=0.8,linestyle='-.',c='dimgray')
    if len(ticks) > 2:
        ticks[0],ticks[-1] = arr[0],arr[-1]
        for i in ticks[1:-1]:
            plt.axvline(i,linewidth=0.4,linestyle='-.',c='gray')

    plt.xlim(arr[0], arr[-1])
    plt.ylim(vertical)
    plt.xticks(ticks,labels)
    plt.ylabel('Energy (eV)')
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def Dispin(arr, bands, ticks, EXPORT, labels, figsize, vertical, legend, color):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    fig.subplots_adjust(wspace=0.0)
    ax1.plot(arr,bands[0].T,color='%s'%color,linewidth=0.8,linestyle='-')
    ax2.plot(arr,bands[1].T,color='k',       linewidth=0.9,linestyle=':')
    ax1.legend(['up'], frameon=False, prop={'style':'italic', 'size':'medium'}, alignment='left',  loc='best', title=legend[0], title_fontproperties={'size':'medium'})
    ax2.legend(['down'], frameon=False, prop={'style':'italic', 'size':'medium'}, alignment='left',  loc='best')
    ax1.tick_params(axis='y', which='minor', color='gray')
    ax2.tick_params(axis='y', which='minor', color='gray')

    ax1.axhline(linewidth=0.8,linestyle='-.',c='dimgray')
    ax2.axhline(linewidth=0.8,linestyle='-.',c='dimgray')
    ax2.set_yticklabels([])
    if len(ticks) > 2:
        ticks[0],ticks[-1] = arr[0],arr[-1]
        for i in ticks[1:-1]:
            ax1.axvline(i,linewidth=0.4,linestyle='-.',c='gray')
            ax2.axvline(i,linewidth=0.4,linestyle='-.',c='gray')

    ax1.set_xlim(arr[0], arr[-1])
    ax1.set_ylim(vertical)
    ax2.set_xlim(arr[0], arr[-1])
    ax2.set_ylim(vertical)
    ax1.set_xticks(ticks,labels)
    ax2.set_xticks(ticks,labels)
    ax1.set_ylabel('Energy (eV)')
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def NoneispinWd(arr, bands, ticks, EXPORT, labels, figsize, vertical, darr, dele, elements, horizontal, width_ratios, legend, color):
    fig, (ax1, ax2) = plt.subplots(1, 2, width_ratios=[1-width_ratios, width_ratios], figsize=figsize)
    fig.subplots_adjust(wspace=0.0)
    ax1.plot(arr,bands.T,color='%s'%color,linewidth=0.8,linestyle='-')
    ax1.legend(legend, frameon=False, prop={'size':'medium'}, alignment='left',  loc='best')
    ax1.tick_params(axis='y', which='minor', color='gray')
    ax2.tick_params(axis='y', which='minor', color='gray')
    for i in range(len(darr)):
        ax2.plot(dele[i],darr[i],linewidth=0.8)

    ax2.axvline(linewidth=0.4,linestyle='-.',c='dimgray')
    ax2.set_yticklabels([])
    ax2.legend(elements, frameon=False, prop={'size':'x-small'}, loc='best', title="Density of states", title_fontproperties={'size':'x-small'})

    ax1.axhline(linewidth=0.8,linestyle='-.',c='dimgray')
    ax2.axhline(linewidth=0.8,linestyle='-.',c='dimgray')
    if len(ticks) > 2:
        ticks[0],ticks[-1] = arr[0],arr[-1]
        for i in ticks[1:-1]:
            ax1.axvline(i,linewidth=0.4,linestyle='-.',c='gray')

    ax1.set_xlim(arr[0], arr[-1])
    ax1.set_ylim(vertical)
    ax2.set_xlim(horizontal)
    ax2.set_ylim(vertical)
    ax1.set_xticks(ticks,labels)
    ax2.tick_params(axis='x', labelsize='x-small', labelcolor='dimgray', labelrotation=-90, pad=1.5)
    ax1.set_ylabel('Energy (eV)')
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def IspinWd(arr, bands, ticks, EXPORT, labels, figsize, vertical, darr, dele, elements, horizontal, width_ratios, legend, color):
    fig, (ax1, ax2) = plt.subplots(1, 2, width_ratios=[1-width_ratios, width_ratios], figsize=figsize)
    fig.subplots_adjust(wspace=0.0)
    p_up = ax1.plot(arr,bands[0].T,color='%s'%color,linewidth=0.8,linestyle='-')
    p_do = ax1.plot(arr,bands[1].T,color='k',       linewidth=0.9,linestyle=':')
    ax1.legend([p_up[0], p_do[0]], ['up', 'down'], frameon=False, prop={'style':'italic', 'size':'medium'}, alignment='left',  loc='best', title=legend[0], title_fontproperties={'size':'medium'})
    ax1.tick_params(axis='y', which='minor', color='gray')
    ax2.tick_params(axis='y', which='minor', color='gray')
    for i in range(len(darr)):
        ax2.plot(dele[i],darr[i],linewidth=0.8)

    ax2.axvline(linewidth=0.4,linestyle='-.',c='dimgray')
    ax2.set_yticklabels([])
    ax2.legend(elements, frameon=False, prop={'size':'x-small'}, loc='best', title="Density of states", title_fontproperties={'size':'x-small'})

    ax1.axhline(linewidth=0.8,linestyle='-.',c='dimgray')
    ax2.axhline(linewidth=0.8,linestyle='-.',c='dimgray')
    if len(ticks) > 2:
        ticks[0],ticks[-1] = arr[0],arr[-1]
        for i in ticks[1:-1]:
            ax1.axvline(i,linewidth=0.4,linestyle='-.',c='gray')

    ax1.set_xlim(arr[0], arr[-1])
    ax1.set_ylim(vertical)
    ax2.set_xlim(horizontal)
    ax2.set_ylim(vertical)
    ax1.set_xticks(ticks,labels)
    ax2.tick_params(axis='x', labelsize='x-small', labelcolor='dimgray', labelrotation=-90, pad=1.5)
    ax1.set_ylabel('Energy (eV)')
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def DispinWd(arr, bands, ticks, EXPORT, labels, figsize, vertical, darr, dele, elements, horizontal, width_ratios, legend, color):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, width_ratios=[0.5*(1-width_ratios), 0.5*(1-width_ratios), width_ratios], figsize=figsize)
    fig.subplots_adjust(wspace=0.0)
    ax1.plot(arr,bands[0].T,color='%s'%color,linewidth=0.8,linestyle='-')
    ax2.plot(arr,bands[1].T,color='k',       linewidth=0.9,linestyle=':')
    ax1.legend(['up'], frameon=False, prop={'style':'italic', 'size':'medium'}, alignment='left',  loc='best', title=legend[0], title_fontproperties={'size':'medium'})
    ax2.legend(['down'], frameon=False, prop={'style':'italic', 'size':'medium'}, alignment='left',  loc='best')
    ax1.tick_params(axis='y', which='minor', color='gray')
    ax2.tick_params(axis='y', which='minor', color='gray')
    ax3.tick_params(axis='y', which='minor', color='gray')
    for i in range(len(darr)):
        ax3.plot(dele[i],darr[i],linewidth=0.8)

    ax3.axvline(linewidth=0.4,linestyle='-.',c='dimgray')
    ax2.set_yticklabels([])
    ax3.set_yticklabels([])
    ax3.legend(elements, frameon=False, prop={'size':'x-small'}, loc='best', title="Density of states", title_fontproperties={'size':'x-small'})

    ax1.axhline(linewidth=0.8,linestyle='-.',c='dimgray')
    ax2.axhline(linewidth=0.8,linestyle='-.',c='dimgray')
    ax3.axhline(linewidth=0.8,linestyle='-.',c='dimgray')
    if len(ticks) > 2:
        ticks[0],ticks[-1] = arr[0],arr[-1]
        for i in ticks[1:-1]:
            ax1.axvline(i,linewidth=0.4,linestyle='-.',c='gray')
            ax2.axvline(i,linewidth=0.4,linestyle='-.',c='gray')

    ax1.set_xlim(arr[0], arr[-1])
    ax1.set_ylim(vertical)
    ax2.set_xlim(arr[0], arr[-1])
    ax2.set_ylim(vertical)
    ax3.set_xlim(horizontal)
    ax3.set_ylim(vertical)
    ax1.set_xticks(ticks,labels)
    ax2.set_xticks(ticks,labels)
    ax3.tick_params(axis='x', labelsize='x-small', labelcolor='dimgray', labelrotation=-90, pad=1.5)
    ax1.set_ylabel('Energy (eV)')
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def dosfiles(EXPORT, figsize, darr, dele, vertical, horizontal, legend, elements):
    plt.figure(figsize=figsize)
    plt.tick_params(axis='y', labelsize='small', labelcolor='dimgray')
    plt.tick_params(axis='y', which='minor', color='gray')
    plt.minorticks_on()
    plt.tick_params(axis='x', which='minor', color='gray')
    for i in range(len(darr)):
        plt.plot(darr[i], dele[i], linewidth=0.8)

    plt.axvline(linewidth=0.8,linestyle='-.',c='dimgray')
    plt.axhline(linewidth=0.4,linestyle='-.',c='dimgray')
    plt.legend(elements, frameon=False, prop={'size':'medium'}, loc='best')
    plt.xlim(vertical)
    plt.ylim(horizontal)
    plt.xlabel('Energy (eV)')
    plt.ylabel('Density of states, electrons/eV')
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')
