import argparse, os, re
import matplotlib.pyplot as plt
from pbandplot import plots, readdata

def main():
    parser = argparse.ArgumentParser(description='Plot the phonon band structure from phonopy results.',
                                     epilog='''
Example:
pbandplot -i band.dat -o pband.png -l g m k g -d projected_dos.dat -g "$\pi^2_4$" -e Si C O
''',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-v', "--version",    action="version",    version="pbandplot 0.1.1.2")
    parser.add_argument('-s', "--size",       type=float,          nargs=2, help='figure size: width, height')
    parser.add_argument('-b', "--broken",     type=float,          nargs=2, help='broken axis: start, end')
    parser.add_argument('-r', "--hratios",    type=float,          default=0.2, help='height ratio for broken axis, default 0.2')
    parser.add_argument('-y', "--vertical",   type=float,          nargs=2, help="frequency range (THz)")
    parser.add_argument('-g', "--legend",     type=str,            nargs=1, help="legend labels")
    parser.add_argument('-a', "--location",   type=str.lower,      default='best',
                                                                   choices=['best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left', 'center right', 'lower center', 'upper center', 'center'],
                                                                   help="arrange the legend location, default best")
    parser.add_argument('-k', "--linestyle",  type=str,            nargs='+', default=['-'], help="linestyle: solid; dashed; dashdot; dotted or tuple")
    parser.add_argument('-c', "--color",      type=str,            nargs='+', default=[],
                                                                   help="plot colors: b, blue; g, green; r, red; c, cyan; m, magenta; y, yellow; k, black; w, white")
    parser.add_argument('-i', "--input",      type=str,            default="BAND.dat", help="plot figure from .dat file")
    parser.add_argument('-o', "--output",     type=str,            default="BAND.png", help="plot figure filename")
    parser.add_argument('-l', "--labels",     type=str.upper,      nargs='+', default=[], help='labels for high-symmetry points')
    parser.add_argument('-d', "--dos",        type=str,            help="plot Phonon DOS from .dat file")
    parser.add_argument('-x', "--horizontal", type=float,          nargs=2, help="Phonon density of states")
    parser.add_argument('-n', "--exchange",   action='store_true', help="exchange the x and y axes of Phonon DOS")
    parser.add_argument('-e', "--elements",   type=str,            nargs='+', default=[], help="PDOS labels")
    parser.add_argument('-w', "--wratios",    type=float,          default=0.5, help='width ratio for DOS subplot, default 0.5')
    parser.add_argument('-f', "--font",       type=str,            default='STIXGeneral', help="font to use")

    args = parser.parse_args()

    labels = [re.sub("'|‘|’", '′', re.sub('"|“|”', '″', re.sub('^GA[A-Z]+$|^G$', 'Γ', i))) for i in args.labels]
    elements = [re.sub("'|‘|’", '′', re.sub('"|“|”', '″', i)) for i in args.elements]
    linestyle = []
    for i in args.linestyle:
        if len(i) > 2 and i[0] == '(' and i[-1] == ')':
            linestyle.append(eval(i))
        elif len(i.split('*')) == 2:
            j = i.split('*')
            linestyle = linestyle + [j[0]] * int(j[1])
        else:
            linestyle.append(i)

    pltname = os.path.split(os.getcwd())[-1]
    s_ele = []
    formula = ''
    if os.path.exists('POSCAR-unitcell'):
        symbol, factor = readdata.symbols('POSCAR-unitcell')
        for i in range(len(symbol)):
            s_ele = s_ele + [symbol[i]] * factor[i]
            if factor[i] > 1:
                formula = formula + symbol[i] + '$_'+ str(factor[i]) + '$'
            else:
                formula = formula + symbol[i]

    if not elements and s_ele:
        elements = s_ele

    legend = args.legend
    if not legend:
        if formula:
            legend = [formula]
        else:
            legend = [pltname]

    color  = []
    for i in args.color:
        if len(i.split('*')) == 2:
            j = i.split('*')
            color = color + [j[0]] * int(j[1])
        else:
            color.append(i)

    broken = args.broken
    height_ratio = args.hratios
    if height_ratio >= 1 or height_ratio <= 0:
        height_ratio = 0.2

    width_ratios = args.wratios
    if width_ratios >= 1 or width_ratios <= 0:
        width_ratios = 0.5

    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['ytick.minor.visible'] = True
    plt.rcParams['font.family'] = '%s'%args.font
    plt.rcParams["mathtext.fontset"] = 'cm'

    if os.path.exists(args.input):
        arr, fre, ticks = readdata.bands(args.input)
        if args.dos is None:
            if args.broken is None:
                plots.Nobroken(args.output, args.size, args.vertical, arr, fre, ticks, labels, linestyle, legend, args.location, color)
            else:
                plots.Broken(args.output, args.size, args.vertical, arr, fre, ticks, labels, broken, height_ratio, linestyle, legend, args.location, color)
        elif os.path.exists(args.dos):
            darr, dele = readdata.dos(args.dos)
            if args.broken is None:
                plots.NobrokenWd(args.output, args.size, args.vertical, args.horizontal, arr, fre, ticks, labels, darr, dele, elements, width_ratios, linestyle, legend, args.location, color)
            else:
                plots.BrokenWd(args.output, args.size, args.vertical, args.horizontal, arr, fre, ticks, labels, broken, height_ratio, darr, dele, elements, width_ratios, linestyle, legend, args.location, color)

    else:
        if args.dos and os.path.exists(args.dos):
            darr, dele = readdata.dos(args.dos)
            plots.dosfile(args.output, args.size, args.vertical, args.horizontal, darr, dele, elements, linestyle, legend, args.location, args.exchange, color)
        else:
            print('No .dat file!')


