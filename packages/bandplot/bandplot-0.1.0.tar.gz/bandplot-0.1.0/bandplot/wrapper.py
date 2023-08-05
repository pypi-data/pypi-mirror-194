import argparse, os, re, glob
import matplotlib.pyplot as plt
from bandplot import plots, readdata

def main():
    pltname = [os.path.split(os.getcwd())[-1]]
    parser = argparse.ArgumentParser(description='Plot the band structure from vaspkit result.',
                                     epilog='''
Example:
bandplot -i band.dat -o pband.png -l g m k g -d PDOS*
''',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-v', "--version",    action="version", version="bandplot 0.1.0")
    parser.add_argument('-s', "--size",       type=int,   nargs=2)
    parser.add_argument('-y', "--vertical",   default=[-5.0, 5.0], type=float, nargs=2, help="energy range (eV)")
    parser.add_argument('-g', "--legend",     type=str, nargs=1, default=pltname, help="legend labels")
    parser.add_argument('-c', "--color",      type=str, default='red', help="plot color")
    parser.add_argument('-i', "--input",      default="BAND.dat", type=str, help="plot figure from .dat file")
    parser.add_argument('-o', "--output",     default="BAND.png", type=str, help="plot figure filename")
    parser.add_argument('-k', "--klabels",    default="KLABELS",  type=str)
    parser.add_argument('-l', "--labels",     type=str.upper, nargs='+', default=[], help='labels for high-symmetry points')
    parser.add_argument('-d', "--dos",        type=str,   nargs='+', default=[], help="plot DOS from .dat file")
    parser.add_argument('-x', "--horizontal", type=float, nargs=2, help="Density of states, electrons/eV")
    parser.add_argument('-e', "--elements",   type=str,   nargs='+', default=[], help="PDOS labels")
    parser.add_argument('-w', "--wratios",    type=float, help='width ratio for DOS subplot')
    parser.add_argument('-f', "--font",       type=str,   default='STIXGeneral', help="font to use")
    parser.add_argument('-b', "--divided",    action='store_true', help="plot the up and down spin in divided subplot")

    args = parser.parse_args()

    labels = [re.sub("'|‘|’", '′', re.sub('"|“|”', '″', re.sub('^GA[A-Z]+$|^G$', 'Γ', i))) for i in args.labels]
    elements = [re.sub("'|‘|’", '′', re.sub('"|“|”', '″', i)) for i in args.elements]
    legend = args.legend
    color  = args.color

    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['ytick.minor.visible'] = True
    plt.rcParams['font.family'] = '%s'%args.font
    plt.rcParams["mathtext.fontset"] = 'cm'

    if os.path.exists(args.input):
        arr, bands, ispin = readdata.bands(args.input)
        ticks   = []
        klabels = []
        if os.path.exists(args.klabels):
            ticks, klabels = readdata.klabels(args.klabels)

        if len(labels) == 0:
            labels=[re.sub('GAMMA|Gamma|G', 'Γ', re.sub('Undefined|Un|[0-9]', '', i)) for i in klabels]

        diff = len(ticks)-len(labels)
        if diff > 0:
            for i in range(diff):
                labels=labels+['']

        if len(args.dos) == 0:
            if ispin == "Noneispin":
                plots.Noneispin(arr, bands, ticks, args.output, labels, args.size, args.vertical, legend, color)
            elif ispin == "Ispin" and not args.divided:
                plots.Ispin(arr, bands, ticks, args.output, labels, args.size, args.vertical, legend, color)
            elif ispin == "Ispin" and args.divided:
                plots.Dispin(arr, bands, ticks, args.output, labels, args.size, args.vertical, legend, color)
        else:
            dosfile = []
            for i in args.dos:
                dosfile = dosfile + glob.glob(i)

            darr, dele, s_elements = readdata.dos(dosfile)
            if not args.wratios:
                if not args.divided:
                    width_ratios = 0.5
                else:
                    width_ratios = 0.3
            else:
                width_ratios = args.wratios

            if len(elements) == 0:
                elements = [re.sub('.dat|^[A-Za-z]+_', '', i) for i in s_elements]

            if ispin == "Noneispin":
                plots.NoneispinWd(arr, bands, ticks, args.output, labels, args.size, args.vertical, darr, dele, elements, args.horizontal, width_ratios, legend, color)
            elif ispin == "Ispin" and not args.divided:
                plots.IspinWd(arr, bands, ticks, args.output, labels, args.size, args.vertical, darr, dele, elements, args.horizontal, width_ratios, legend, color)
            elif ispin == "Ispin" and args.divided:
                plots.DispinWd(arr, bands, ticks, args.output, labels, args.size, args.vertical, darr, dele, elements, args.horizontal, width_ratios, legend, color)

    else:
        if args.dos:
            dosfile = []
            for i in args.dos:
                dosfile = dosfile + glob.glob(i)

            darr, dele, s_elements = readdata.dos(dosfile)
            if len(elements) == 0:
                elements = [re.sub('.dat|^[A-Za-z]+_', '', i) for i in s_elements]

            plots.dosfiles(args.output, args.size, darr, dele, args.vertical, args.horizontal, legend, elements)

