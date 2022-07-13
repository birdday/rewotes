import numpy as np


class ConvTracker:

    def __init__(self):
        self.cycle_number = int(0)  # Uses 0 indexing
        self.energy_cutoff = 0.01   # Units = meV
        self.mesh = [1,1,1]         # k-point mesh
