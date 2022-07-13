import argparse
import numpy as np
import re
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

    def __init__(self, file, ke_cutoff):
        self.input_file = file          # Path to Quantum Espresso input file
        self.cycle_number = int(0)      # Uses 0 indexing
        self.energy_cutoff = ke_cutoff  # Units = eV
        self.mesh = [1,1,1]             # k-point mesh
        self.ke_vals = []               # Used to track all energies

        self.parse_input()

    def parse_input(self):
        f = open(self.input_file, 'r')
        lines = f.readlines()
        for i, line in enumerate(lines):
            if re.search('K_POINTS', line):
                print(lines[i], lines[i+1])
                break
        f.close()

    def check_convergence(self):
        if len(self.ke_vals) < 2:
            warnings.warn('Not enough recorded energies, returning False.')
            return False
        else:
            return (self.ke_vals[self.cycle_number] - self.ke_vals[self.cycle_number]-1) <= self.energy_cutoff

    def update_mesh(self):
        self.mesh = [val+1 for val in self.mesh]
