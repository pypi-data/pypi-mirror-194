import matplotlib.pyplot as plt

def Broken(EXPORT,  figsize, vertical, arr, fre, ticks, labels, broken, height_ratio, linestyle, legend, location, color):
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, height_ratios=[height_ratio, 1-height_ratio], figsize=figsize)
    fig.subplots_adjust(hspace=0.0)
    if len(color) == 0:
        color = ['r']

    ax1.plot(arr, fre.T, color=color[0], linewidth=0.8, linestyle=linestyle[0])
    ax2.plot(arr, fre.T, color=color[0], linewidth=0.8, linestyle=linestyle[0])
    plt.xlim(arr[0], arr[-1])
    if vertical is None:
        vertical = plt.ylim()

    ax1.set_ylim(broken[1], vertical[1])
    ax2.set_ylim(vertical[0], broken[0])
    ax1.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax1.xaxis.set_ticks_position(position='none')
    ax1.tick_params(axis='y', which='minor', color='darkgray')
    ax1.tick_params(axis='y', labelsize='small', labelcolor='dimgray', labelrotation=-60)
    ax2.tick_params(axis='y', which='minor', color='gray')
    ax2.axhline(linewidth=0.4, linestyle='-.', c='gray')
    if len(ticks) > 2:
        ticks[0],ticks[-1] = arr[0],arr[-1]
        for i in ticks[1:-1]:
            ax1.axvline(i, linewidth=0.4, linestyle=(0, (3, 5, 1, 5)), c='gray')
            ax2.axvline(i, linewidth=0.4, linestyle='-.', c='gray')

    if len(ticks) > len(labels):
        labels = labels + [''] * (len(ticks) - len(labels))
    elif len(ticks) < len(labels):
        labels = labels[:len(ticks)]

    ax2.legend(legend, frameon=False, prop={'size':'medium'}, loc=location)
    plt.xticks(ticks,labels)
    plt.suptitle('Frequency (THz)', rotation=90, x=0.06, y=0.6, size='medium')
    kwargs = dict(marker=[(-1, -1), (1, 1)], markersize=6,
                  linestyle='', color='k', mec='k', mew=1, clip_on=False)
    ax1.plot([0, 1], [0.02, 0.02], transform=ax1.transAxes, **kwargs)
    ax2.plot([0, 1], [0.98, 0.98], transform=ax2.transAxes, **kwargs)
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def Nobroken(EXPORT, figsize, vertical, arr, fre, ticks, labels, linestyle, legend, location, color):
    plt.figure(figsize=figsize)
    if len(color) == 0:
        color = ['r']

    plt.plot(arr, fre.T, color=color[0], linewidth=0.8, linestyle=linestyle[0])
    plt.tick_params(axis='y', which='minor', color='gray')
    plt.axhline(linewidth=0.4, linestyle='-.', c='gray')
    if len(ticks) > 2:
        ticks[0],ticks[-1] = arr[0],arr[-1]
        for i in ticks[1:-1]:
            plt.axvline(i, linewidth=0.4, linestyle='-.', c='gray')

    if len(ticks) > len(labels):
        labels = labels + [''] * (len(ticks) - len(labels))
    elif len(ticks) < len(labels):
        labels = labels[:len(ticks)]

    plt.legend(legend, frameon=False, prop={'size':'medium'}, loc=location)
    plt.xticks(ticks,labels)
    plt.xlim(arr[0], arr[-1])
    plt.ylim(vertical)
    plt.ylabel('Frequency (THz)')
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def BrokenWd(EXPORT, figsize, vertical, horizontal, arr, fre, ticks, labels, broken, height_ratio, darr, dele, elements, width_ratios, linestyle, legend, location, color):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, height_ratios=[height_ratio, 1-height_ratio], width_ratios=[1-width_ratios, width_ratios], figsize=figsize)
    fig.subplots_adjust(wspace=0.0, hspace=0.0)
    if len(color) == 0:
        color = ['r']

    ax1.plot(arr, fre.T, color=color[0], linewidth=0.8, linestyle=linestyle[0])
    ax3.plot(arr, fre.T, color=color[0], linewidth=0.8, linestyle=linestyle[0])
    num = dele.shape[-1]
    if num + 1 > len(color):
        color = color + [''] * (num - len(color) + 1)

    if num + 1 > len(linestyle):
        linestyle = linestyle + ['-'] * (num - len(linestyle) + 1)

    for i in range(num):
        if color[i+1]:
            ax2.plot(dele[:,i], darr, linewidth=0.8, linestyle=linestyle[i+1], color=color[i+1])
            ax4.plot(dele[:,i], darr, linewidth=0.8, linestyle=linestyle[i+1], color=color[i+1])
        else:
            ax2.plot(dele[:,i], darr, linewidth=0.8, linestyle=linestyle[i+1])
            ax4.plot(dele[:,i], darr, linewidth=0.8, linestyle=linestyle[i+1])

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
    ax1.tick_params(axis='y', which='minor', color='darkgray')
    ax1.tick_params(axis='y', labelsize='small', labelcolor='dimgray', labelrotation=-60)
    ax3.axhline(linewidth=0.4, linestyle='-.', c='gray')
    ax4.axhline(linewidth=0.4, linestyle='-.', c='gray')
    ax2.tick_params(axis='y', which='minor', color='darkgray')
    ax3.tick_params(axis='y', which='minor', color='gray')
    ax4.minorticks_on()
    ax4.tick_params(axis='x', labelsize='small', labelcolor='dimgray', labelrotation=-90, pad=3)
    ax4.tick_params(axis='both', which='minor', color='gray')
    ax1.set_xticklabels([])
    ax2.set_xticklabels([])
    ax2.set_yticklabels([])
    ax4.set_yticklabels([])
    ax2.axvline(linewidth=0.4, linestyle=(0, (3, 5, 1, 5)), c='gray')
    ax4.axvline(linewidth=0.4, linestyle='-.', c='gray')
    if num > len(elements):
        elements = elements + [''] * (num - len(elements))
    elif num < len(elements):
        elements = elements[:num]

    ax3.legend(legend, frameon=False, prop={'size':'small'}, loc=location)
    ax4.legend(elements, frameon=False, prop={'size':'x-small'}, loc=location, title="Phonon DOS", title_fontproperties={'size':'x-small'})
    if len(ticks) > 2:
        ticks[0],ticks[-1] = arr[0],arr[-1]
        for i in ticks[1:-1]:
            ax1.axvline(i, linewidth=0.4, linestyle=(0, (3, 5, 1, 5)), c='gray')
            ax3.axvline(i, linewidth=0.4, linestyle='-.', c='gray')

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

def NobrokenWd(EXPORT, figsize, vertical, horizontal, arr, fre, ticks, labels, darr, dele, elements, width_ratios, linestyle, legend, location, color):
    fig, (ax1, ax2) = plt.subplots(1, 2, width_ratios=[1-width_ratios, width_ratios], figsize=figsize)
    fig.subplots_adjust(wspace=0.0)
    if len(color) == 0:
        color = ['r']

    ax1.plot(arr, fre.T, color=color[0], linewidth=0.8, linestyle=linestyle[0])
    num = dele.shape[-1]
    if num + 1 > len(color):
        color = color + [''] * (num - len(color) + 1)

    if num + 1 > len(linestyle):
        linestyle = linestyle + ['-'] * (num - len(linestyle) + 1)

    for i in range(num):
        if color[i+1]:
            ax2.plot(dele[:,i], darr, linewidth=0.8, linestyle=linestyle[i+1], color=color[i+1])
        else:
            ax2.plot(dele[:,i], darr, linewidth=0.8, linestyle=linestyle[i+1])

    ax1.set_xlim(arr[0], arr[-1])
    if vertical is None:
        vertical = ax1.get_ylim()

    ax1.set_ylim(vertical)
    ax2.set_ylim(vertical)
    ax2.set_xlim(horizontal)
    ax1.tick_params(axis='y', which='minor', color='gray')
    ax1.axhline(linewidth=0.4, linestyle='-.', c='gray')
    ax2.minorticks_on()
    ax2.tick_params(axis='x', labelsize='small', labelcolor='dimgray', labelrotation=-90, pad=3)
    ax2.tick_params(axis='both', which='minor', color='gray')
    ax2.set_yticklabels([])
    ax2.axhline(linewidth=0.4, linestyle='-.', c='gray')
    if num > len(elements):
        elements = elements + [''] * (num - len(elements))
    elif num < len(elements):
        elements = elements[:num]

    ax1.legend(legend, frameon=False, prop={'size':'small'}, loc=location)
    ax2.axvline(linewidth=0.4,linestyle='-.',c='dimgray')
    ax2.legend(elements, frameon=False, prop={'size':'x-small'}, loc=location, title="Phonon DOS", title_fontproperties={'size':'x-small'})
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

def dosfile(EXPORT, figsize, vertical, horizontal, darr, dele, elements, linestyle, legend, location, exchange, color):
    plt.figure(figsize=figsize)
    plt.minorticks_on()
    plt.tick_params(axis='both', which='minor', color='gray')
    num = dele.shape[-1]
    if num > len(color):
        color = color + [''] * (num - len(color))

    if num > len(linestyle):
        linestyle = linestyle + ['-'] * (num - len(linestyle))

    if exchange:
        for i in range(num):
            if color[i]:
                plt.plot(darr, dele[:,i], linewidth=0.8, linestyle=linestyle[i], color=color[i])
            else:
                plt.plot(darr, dele[:,i], linewidth=0.8, linestyle=linestyle[i])

        plt.xlim(vertical)
        plt.ylim(horizontal)
        plt.xlabel('Frequency (THz)')
        plt.ylabel('Phonon DOS')
        plt.tick_params(axis='y', labelsize='medium', labelcolor='dimgray')
    else:
        for i in range(num):
            if color[i]:
                plt.plot(dele[:,i], darr, linewidth=0.8, linestyle=linestyle[i], color=color[i])
            else:
                plt.plot(dele[:,i], darr, linewidth=0.8, linestyle=linestyle[i])

        plt.ylim(vertical)
        plt.xlim(horizontal)
        plt.ylabel('Frequency (THz)')
        plt.xlabel('Phonon DOS')
        plt.tick_params(axis='x', labelsize='medium', labelcolor='dimgray')

    plt.axvline(linewidth=0.4, linestyle='-.', c='gray')
    plt.axhline(linewidth=0.4, linestyle='-.', c='gray')
    if num > len(elements):
        elements = elements + [''] * (num - len(elements))
    elif num < len(elements):
        elements = elements[:num]

    plt.legend(elements, frameon=False, prop={'size':'medium'}, loc=location, title=legend[0], title_fontproperties={'size':'medium'})
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

