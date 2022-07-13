import argparse
import numpy as np
import warnings


# Parse arguments from command line.
# -h, --help is added by default.
parser = argparse.ArgumentParser()
parser.add_argument('input', help="Path to Quantum Espresso input file.", type=str)
parser.add_argument('ke_cutoff', help="Desired kinetic energy cutoff. Default units is eV.", type=float)
parser.add_argument('-u', '--units', help="Set units for ke_cutoff.", type=str)

args = parser.parse_args()
if args.units:
    conversion_factors = {'eV':1, 'meV':1e3, 'Ha':27.2114, 'Ry':13.6057}
    if args.units not in conversion_factors.keys():
        raise argparse.ArgumentTypeError('Units must be one of the following: eV, meV, Ha, or Ry.')
    else:
        print(f'{args.ke_cutoff} {args.units} <--> {args.ke_cutoff*conversion_factors[args.units]} eV')


class ConvTracker:

    def __init__(self):
        self.cycle_number = int(0)  # Uses 0 indexing
        self.energy_cutoff = 0.01   # Units = meV
        self.mesh = [1,1,1]         # k-point mesh
