import matplotlib.pyplot as plt

def Broken(arr, fre, ticks, EXPORT, labels, figsize, vertical, broken, height_ratio, legend, color):
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, height_ratios=[height_ratio, 1-height_ratio], figsize=figsize)
    fig.subplots_adjust(hspace=0.0)
    ax1.plot(arr, fre.T, color=color[0], linewidth=0.8, linestyle='-')
    ax2.plot(arr, fre.T, color=color[0], linewidth=0.8, linestyle='-')
    plt.xlim(arr[0], arr[-1])
    if vertical is None:
        vertical = plt.ylim()

    ax1.set_ylim(broken[1], vertical[1])
    ax2.set_ylim(vertical[0], broken[0])
    ax1.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax1.xaxis.set_ticks_position(position='none')
    ax1.tick_params(axis='y', which='minor', color='gray')
    ax1.tick_params(axis='y', labelsize='small', labelcolor='dimgray', labelrotation=-60)
    ax2.tick_params(axis='y', which='minor', color='gray')
    ax2.axhline(linewidth=0.4,linestyle='-.',c='m')
    if len(ticks) > 2:
        ticks[0],ticks[-1] = arr[0],arr[-1]
        for i in ticks[1:-1]:
            ax1.axvline(i,linewidth=0.4,linestyle='-.',c='gray')
            ax2.axvline(i,linewidth=0.4,linestyle='-.',c='gray')

    if len(ticks) > len(labels):
        labels = labels + [''] * (len(ticks) - len(labels))
    elif len(ticks) < len(labels):
        labels = labels[:len(ticks)]

    ax2.legend(legend, frameon=False, prop={'size':'medium'}, loc='best')
    plt.xticks(ticks,labels)
    plt.suptitle('Frequency (THz)', rotation=90, x=0.06, y=0.6, size='medium')
    kwargs = dict(marker=[(-1, -1), (1, 1)], markersize=6,
                  linestyle='', color='k', mec='k', mew=1, clip_on=False)
    ax1.plot([0, 1], [0.02, 0.02], transform=ax1.transAxes, **kwargs)
    ax2.plot([0, 1], [0.98, 0.98], transform=ax2.transAxes, **kwargs)
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def Nobroken(arr, fre, ticks, EXPORT, labels, figsize, vertical, legend, color):
    plt.figure(figsize=figsize)
    plt.plot(arr, fre.T, color=color[0], linewidth=0.8, linestyle='-')
    plt.tick_params(axis='y', which='minor', color='gray')
    plt.axhline(linewidth=0.4,linestyle='-.',c='m')
    if len(ticks) > 2:
        ticks[0],ticks[-1] = arr[0],arr[-1]
        for i in ticks[1:-1]:
            plt.axvline(i,linewidth=0.4,linestyle='-.',c='gray')

    if len(ticks) > len(labels):
        labels = labels + [''] * (len(ticks) - len(labels))
    elif len(ticks) < len(labels):
        labels = labels[:len(ticks)]

    plt.legend(legend, frameon=False, prop={'size':'medium'}, loc='best')
    plt.xticks(ticks,labels)
    plt.xlim(arr[0], arr[-1])
    plt.ylim(vertical)
    plt.ylabel('Frequency (THz)')
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def BrokenWd(arr, fre, ticks, EXPORT, labels, figsize, vertical, broken, height_ratio, darr, dele, elements, horizontal, width_ratios, legend, color):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, height_ratios=[height_ratio, 1-height_ratio], width_ratios=[1-width_ratios, width_ratios], figsize=figsize)
    fig.subplots_adjust(wspace=0.0, hspace=0.0)
    ax1.plot(arr, fre.T, color=color[0], linewidth=0.8, linestyle='-')
    ax3.plot(arr, fre.T, color=color[0], linewidth=0.8, linestyle='-')
    num = dele.shape[-1]
    if len(color) < num + 1:
        ax2.plot(dele,darr,linewidth=0.8)
        ax4.plot(dele,darr,linewidth=0.8)
    else:
        for i in range(num):
            ax2.plot(dele[:,i], darr, linewidth=0.8, color=color[i+1])
            ax4.plot(dele[:,i], darr, linewidth=0.8, color=color[i+1])

    ax1.set_xlim(arr[0], arr[-1])
    ax3.set_xlim(arr[0], arr[-1])
    if vertical is None:
        vertical = ax1.get_ylim()

    ax1.set_ylim(broken[1], vertical[1])
    ax2.set_ylim(broken[1], vertical[1])
    ax3.set_ylim(vertical[0], broken[0])
    ax4.set_ylim(vertical[0], broken[0])
    ax2.set_xlim(horizontal)
    ax4.set_xlim(horizontal)
    ax1.spines['bottom'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax3.spines['top'].set_visible(False)
    ax4.spines['top'].set_visible(False)
    ax1.xaxis.set_ticks_position('none')
    ax2.xaxis.set_ticks_position('none')
    ax1.tick_params(axis='y', which='minor', color='gray')
    ax1.tick_params(axis='y', labelsize='small', labelcolor='dimgray', labelrotation=-60)
    ax3.axhline(linewidth=0.4,linestyle='-.',c='m')
    ax4.axhline(linewidth=0.4,linestyle='-.',c='m')
    ax2.tick_params(axis='y', which='minor', color='gray')
    ax3.tick_params(axis='y', which='minor', color='gray')
    ax4.minorticks_on()
    ax4.tick_params(axis='x', labelsize='small', labelcolor='dimgray', labelrotation=-90, pad=3)
    ax4.tick_params(axis='y', which='minor', color='gray')
    ax1.set_xticklabels([])
    ax2.set_xticklabels([])
    ax2.set_yticklabels([])
    ax4.set_yticklabels([])
    ax2.axhline(linewidth=0.4,linestyle='-.',c='m')
    ax2.axvline(linewidth=0.4,linestyle='-.',c='dimgray')
    ax4.axvline(linewidth=0.4,linestyle='-.',c='dimgray')
    if num > len(elements):
        elements = elements + [''] * (num - len(elements))
    elif num < len(elements):
        elements = elements[:num]

    ax3.legend(legend, frameon=False, prop={'size':'small'}, loc='best')
    ax4.legend(elements, frameon=False, prop={'size':'x-small'}, loc='best', title="Phonon DOS", title_fontproperties={'size':'x-small'})
    if len(ticks) > 2:
        ticks[0],ticks[-1] = arr[0],arr[-1]
        for i in ticks[1:-1]:
            ax1.axvline(i,linewidth=0.4,linestyle='-.',c='gray')
            ax3.axvline(i,linewidth=0.4,linestyle='-.',c='gray')

    if len(ticks) > len(labels):
        labels = labels + [''] * (len(ticks) - len(labels))
    elif len(ticks) < len(labels):
        labels = labels[:len(ticks)]

    ax3.set_xticks(ticks,labels)
    plt.suptitle('Frequency (THz)', rotation=90, x=0.06, y=0.6, size='medium')
    kwargs = dict(marker=[(-1, -1), (1, 1)], markersize=6,
                  linestyle='', color='k', mec='k', mew=1, clip_on=False)
    ax1.plot([0, 1], [0.02, 0.02], transform=ax1.transAxes, **kwargs)
    ax3.plot([0, 1], [0.98, 0.98], transform=ax3.transAxes, **kwargs)
    ax2.plot(1, 0.02, transform=ax2.transAxes, **kwargs)
    ax4.plot(1, 0.98, transform=ax4.transAxes, **kwargs)
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def NobrokenWd(arr, fre, ticks, EXPORT, labels, figsize, vertical, darr, dele, elements, horizontal, width_ratios, legend, color):
    fig, (ax1, ax2) = plt.subplots(1, 2, width_ratios=[1-width_ratios, width_ratios], figsize=figsize)
    fig.subplots_adjust(wspace=0.0)
    ax1.plot(arr, fre.T, color=color[0], linewidth=0.8, linestyle='-')
    num = dele.shape[-1]
    if len(color) < num + 1:
        ax2.plot(dele, darr, linewidth=0.8)
    else:
        for i in range(num):
            ax2.plot(dele[:,i], darr, linewidth=0.8, color=color[i+1])

    ax1.set_xlim(arr[0], arr[-1])
    if vertical is None:
        vertical = ax1.get_ylim()

    ax1.set_ylim(vertical)
    ax2.set_ylim(vertical)
    ax2.set_xlim(horizontal)
    ax1.tick_params(axis='y', which='minor', color='gray')
    ax1.axhline(linewidth=0.4,linestyle='-.',c='m')
    ax2.minorticks_on()
    ax2.tick_params(axis='x', labelsize='small', labelcolor='dimgray', labelrotation=-90, pad=3)
    ax2.tick_params(axis='both', which='minor', color='gray')
    ax2.set_yticklabels([])
    ax2.axhline(linewidth=0.4,linestyle='-.',c='m')
    if num > len(elements):
        elements = elements + [''] * (num - len(elements))
    elif num < len(elements):
        elements = elements[:num]

    ax1.legend(legend, frameon=False, prop={'size':'small'}, loc='best')
    ax2.axvline(linewidth=0.4,linestyle='-.',c='dimgray')
    ax2.legend(elements, frameon=False, prop={'size':'x-small'}, loc='best', title="Phonon DOS", title_fontproperties={'size':'x-small'})
    if len(ticks) > 2:
        ticks[0],ticks[-1] = arr[0],arr[-1]
        for i in ticks[1:-1]:
            ax1.axvline(i,linewidth=0.4,linestyle='-.',c='gray')

    if len(ticks) > len(labels):
        labels = labels + [''] * (len(ticks) - len(labels))
    elif len(ticks) < len(labels):
        labels = labels[:len(ticks)]

    ax1.set_xticks(ticks,labels)
    ax1.set_ylabel('Frequency (THz)')
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def dosfile(EXPORT, figsize, vertical, horizontal, darr, dele, elements, legend, exchange, color):
    plt.figure(figsize=figsize)
    plt.minorticks_on()
    plt.tick_params(axis='x', which='minor', color='gray')
    plt.tick_params(axis='y', which='minor', color='gray')
    num = dele.shape[-1]
    if exchange:
        if len(color) < num:
            plt.plot(darr, dele, linewidth=0.8)
        else:
            for i in range(num):
                plt.plot(darr, dele[:,i], linewidth=0.8, color=color[i])

        plt.xlabel('Frequency (THz)')
        plt.ylabel('Phonon DOS')
        plt.tick_params(axis='y', labelsize='medium', labelcolor='dimgray')
    else:
        if len(color) < num:
            plt.plot(dele, darr, linewidth=0.8)
        else:
            for i in range(num):
                plt.plot(dele[:,i], darr, linewidth=0.8, color=color[i])

        plt.ylabel('Frequency (THz)')
        plt.xlabel('Phonon DOS')
        plt.tick_params(axis='x', labelsize='medium', labelcolor='dimgray')

    plt.axvline(linewidth=0.4,linestyle='-.',c='dimgray')
    plt.axhline(linewidth=0.4,linestyle='-.',c='dimgray')
    if num > len(elements):
        elements = elements + [''] * (num - len(elements))
    elif num < len(elements):
        elements = elements[:num]

    plt.legend(elements, frameon=False, prop={'size':'medium'}, loc='best', title=legend[0], title_fontproperties={'size':'medium'})
    plt.xlim(vertical)
    plt.ylim(horizontal)
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

