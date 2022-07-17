import numpy as np
import re
import warnings



class ConvTracker:

    def __init__(self, owner_id, project_id, material_id, workflow_id, job_endpoints, cutoff=1e-5, energy=[]):
        self.owner_id = owner_id
        self.project_id = project_id
        self.material_id = material_id
        self.workflow_id = workflow_id
        self.job_endpoints = job_endpoints
        self.cutoff = cutoff            # Units = eV
        self.energy = energy            # Array of energies can be passed in to continue a job set.

        self.parse_input()


    def check_convergence(self):
        if len(self.energy) < 2:
            return False
        else:
            return abs(self.energy[-1] - self.energy[-2]) <= self.cutoff

    def update_mesh(self):
        self.mesh = [val+1 for val in self.mesh]


