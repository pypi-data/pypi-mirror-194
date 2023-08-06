import argparse, os, re
import matplotlib.pyplot as plt
from bandplot import plots, readdata

def main():
    parser = argparse.ArgumentParser(description='Plot the band structure from vaspkit result.',
                                     epilog='''
Example:
bandplot -i band.dat -o pband.png -l g m k g -d PDOS*
''',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-v', "--version",    action="version", version="bandplot "+get_version(os.path.join(os.path.dirname(__file__), "__init__.py")))
    parser.add_argument('-s', "--size",       type=int, nargs=2)
    parser.add_argument('-b', "--divided",    action='store_true', help="plot the up and down spin in divided subplot")
    parser.add_argument('-y', "--vertical",   type=float, nargs=2, help="energy (eV) range")
    parser.add_argument('-g', "--legend",     type=str, nargs=1, help="legend labels")
    parser.add_argument('-a', "--location",   type=str.lower,      default='best',
                                                                   choices=['best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left', 'center right', 'lower center', 'upper center', 'center'],
                                                                   help="arrange the legend location, default best")
    parser.add_argument('-k', "--linestyle",  type=str,            nargs='+', default=['-'], help="linestyle: solid; dashed; dashdot; dotted or tuple")
    parser.add_argument('-c', "--color",      type=str,            nargs='+', default=[],
                                                                   help="plot colors: b, blue; g, green; r, red; c, cyan; m, magenta; y, yellow; k, black; w, white")
    parser.add_argument('-i', "--input",      default="BAND.dat", type=str, help="plot figure from .dat file, default BAND.dat")
    parser.add_argument('-o', "--output",     default="BAND.png", type=str, help="plot figure filename, default BAND.png")
    parser.add_argument('-K', "--klabels",    default="KLABELS",  type=str, help="the filename of KLABELS")
    parser.add_argument('-l', "--labels",     type=str.upper, nargs='+', default=[], help='labels for high-symmetry points, such as X S Y K M')
    parser.add_argument('-d', "--dos",        type=str,   nargs='+', default=[], help="plot DOS from .dat file, or file list")
    parser.add_argument('-x', "--horizontal", type=float, nargs=2, help="Density of states, electrons/eV range")
    parser.add_argument('-n', "--exchange",   action='store_true', help="exchange the x and y axes of DOS")
    parser.add_argument('-p', "--partial",    type=str,   nargs='+', default=[], help='the partial DOS to plot, s p d')
    parser.add_argument('-e', "--elements",   type=str,   nargs='+', default=[], help="PDOS labels")
    parser.add_argument('-w', "--wratios",    type=float, help='width ratio for DOS subplot')
    parser.add_argument('-f', "--font",       type=str,   default='STIXGeneral', help="font to use")

    args = parser.parse_args()

    labels = [re.sub("'|‘|’", '′', re.sub('"|“|”', '″', re.sub('^GA[A-Z]+$|^G$', 'Γ', i))) for i in args.labels]
    elements = [re.sub("'|‘|’", '′', re.sub('"|“|”', '″', i)) for i in args.elements]
    dosfiles = readdata.s_dosfile(args.dos)
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
    formula = ''
    if os.path.exists('POSCAR'):
        symbol, factor = readdata.symbols('POSCAR')
        for i in range(len(symbol)):
            if factor[i] > 1:
                formula = formula + symbol[i] + '$_'+ str(factor[i]) + '$'
            else:
                formula = formula + symbol[i]

    legend = args.legend
    if not legend:
        if formula:
            legend = [formula]
        else:
            legend = [pltname]

    color = []
    for i in args.color:
        j = i.split('*')
        if len(j) == 2:
            color = color + [j[0]] * int(j[1])
        else:
            color.append(i)

    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['ytick.minor.visible'] = True
    plt.rcParams['font.family'] = '%s'%args.font
    plt.rcParams["mathtext.fontset"] = 'cm'

    if os.path.exists(args.input):
        if not args.vertical:
            vertical = [-5.0, 5.0]
        else:
            vertical = args.vertical

        arr, bands, ispin = readdata.bands(args.input)
        ticks   = []
        klabels = []
        if os.path.exists(args.klabels):
            ticks, klabels = readdata.klabels(args.klabels)

        if len(labels) == 0:
            labels=[re.sub('GAMMA|Gamma|G', 'Γ', re.sub('Undefined|Un|[0-9]', '', i)) for i in klabels]

        if len(ticks) > len(labels):
            labels=labels + [''] * (len(ticks) - len(labels))

        if not dosfiles:
            if ispin == "Noneispin":
                plots.Noneispin(args.output, args.size, vertical, arr, bands, ticks, labels, linestyle, legend, args.location, color)
            elif ispin == "Ispin" and not args.divided:
                plots.Ispin(args.output, args.size, vertical, arr, bands, ticks, labels, linestyle, legend, args.location, color)
            elif ispin == "Ispin" and args.divided:
                plots.Dispin(args.output, args.size, vertical, arr, bands, ticks, labels, linestyle, legend, args.location, color)
        else:
            darr, dele, s_elements = readdata.dos(args.dos)
            index_f, labels_elements = readdata.select(s_elements, args.partial)
            if not elements:
                elements = labels_elements
            if not args.wratios:
                if not args.divided:
                    width_ratios = 0.5
                else:
                    width_ratios = 0.3
            else:
                width_ratios = args.wratios

            if ispin == "Noneispin":
                plots.NoneispinWd(args.output, args.size, vertical, args.horizontal, arr, bands, ticks, labels, darr, dele, index_f, elements, width_ratios, linestyle, legend, args.location, color)
            elif ispin == "Ispin" and not args.divided:
                plots.IspinWd(args.output, args.size, vertical, args.horizontal, arr, bands, ticks, labels, darr, dele, index_f, elements, width_ratios, linestyle, legend, args.location, color)
            elif ispin == "Ispin" and args.divided:
                plots.DispinWd(args.output, args.size, vertical, args.horizontal, arr, bands, ticks, labels, darr, dele, index_f, elements, width_ratios, linestyle, legend, args.location, color)

    else:
        if dosfiles:
            darr, dele, s_elements = readdata.dos(dosfiles)
            index_f, labels_elements = readdata.select(s_elements, args.partial)
            if not elements:
                elements = labels_elements

            plots.pdosfiles(args.output, args.size, args.vertical, args.horizontal, darr, dele, index_f, elements, linestyle, legend, args.location, args.exchange, color)
        else:
            print('No .dat file!')

def get_version(rel_path: str) -> str:
    with open(rel_path) as fp:
        lines = fp.readlines()
    for line in lines:
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")
