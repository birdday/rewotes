from exabyte_api_client.endpoints.jobs import JobEndpoints
from exabyte_api_client.endpoints.projects import ProjectEndpoints
from exabyte_api_client.endpoints.materials import MaterialEndpoints
from exabyte_api_client.endpoints.workflows import WorkflowEndpoints

from kpoint.kpoint import ConvTracker

# Initialize the endpoints
# Replace 'ACCOUNT_ID' and 'AUTH_TOKEN' with your respective tokens.
ENDPOINT_ARGS = ['platform.exabyte.io', 443, 'ACCOUNT_ID', 'AUTH_TOKEN', '2018-10-01', True]
job_endpoints = JobEndpoints(*ENDPOINT_ARGS)
project_endpoints = ProjectEndpoints(*ENDPOINT_ARGS)
material_endpoints = MaterialEndpoints(*ENDPOINT_ARGS)
workflow_endpoints = WorkflowEndpoints(*ENDPOINT_ARGS)

# Get Owner ID, Project ID, (Default) Material ID, and Workflow ID
# Replace "KPOINT_WORKFLOW" with your respective workflow name.
owner_id = ACCOUNT_ID
project_id = project_endpoints.list({"isDefault": True, "owner._id": ACCOUNT_ID})[0]["_id"]
material_id = material_endpoints.list({"isDefault": True, "owner._id": ACCOUNT_ID})[0]["_id"]
workflow_id = workflow_endpoints.list({"name": "KPOINT_WORKFLOW", "owner._id": ACCOUNT_ID})[0]["_id"]

# Create Tracker Class and Run
tracker = ConvTracker(owner_id, project_id, material_id, workflow_id, job_endpoints)
tracker.run(max_iter=20)
