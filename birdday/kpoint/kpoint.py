import re
import urllib.request
from utils.generic import wait_for_jobs_to_finish


class ConvTracker:

    def __init__(self, owner_id, project_id, material_id, workflow_id, job_endpoints, cutoff=1e-5, energy=[]):
        self.owner_id = owner_id
        self.project_id = project_id
        self.material_id = material_id
        self.workflow_id = workflow_id
        self.job_endpoints = job_endpoints
        self.cutoff = cutoff            # Units = eV
        self.energy = energy            # Array of energies can be passed in to continue a job set.

    def create_submit_job(self, kp, jobs_set=None):
        JOB_NAME = f"kpoint_{kp}"
        config = {
            "owner": {"_id": self.owner_id},
            "_material": {"_id": self.material_id},
            "workflow": {"_id": self.workflow_id},
            "name": JOB_NAME
        }
        job = job_endpoints.create(config)
        if jobs_set is not None:
            job_endpoints.move_to_set(job["_id"], "", jobs_set["_id"])

        # Update K-Point Values
        # This is not an ideal way to set kpoints, but the built in convergence tool did npt work as expected, and adjusting the workflow did not update render.
        job["workflow"]["subworkflows"][0]["units"][0]["input"][0]["rendered"] = job["workflow"]["subworkflows"][0]["units"][0]["input"][0]["rendered"].replace("K_POINTS automatic\n10 10 10 0 0 0", f"K_POINTS automatic\n{kp} {kp} {kp} 0 0 0")
        job_endpoints.update(job["_id"], job)
        job_endpoints.submit(job['_id'])

        return job["_id"]

    def parse_output(self, job_id):
        files = self.job_endpoints.list_files(job_id)
        output_file = [file for file in files if file["name"] ==  'pw_scf.out'][0]
        server_response = urllib.request.urlopen(output_file['signedUrl'])
        output_file_bytes = server_response.read()
        output_file = output_file_bytes.decode(encoding="UTF-8")
        output_as_array = output_file.split("\n")
        total_energy_ry = float(re.split(" +", [row for row in output_as_array if "!    total energy" in row][0])[-2])
        total_energy_ev = total_energy_ry * 13.6056980659

        return total_energy_ev

    def check_convergence(self):
        if len(self.energy) < 2:
            return False
        else:
            return abs(self.energy[-1] - self.energy[-2]) <= self.cutoff

    def run(self, kp_initial=1, max_iter=20):
        JOBS_SET_NAME = "KPoint_Test_Set"
        jobs_set = self.job_endpoints.create_set({"name": JOBS_SET_NAME, "projectId": self.project_id, "owner": {"_id": self.owner_id}})

        for kp in range(kp_initial, max_iter+kp_initial):
            print(f"KPoints = {kp}")
            job_id = self.create_submit_job(kp, jobs_set=jobs_set)
            wait_for_jobs_to_finish(self.job_endpoints, [job_id], poll_interval=10)
            total_energy = self.parse_output(job_id)
            self.energy.extend([total_energy])

            if self.check_convergence():
                break