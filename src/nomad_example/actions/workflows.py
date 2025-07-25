from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from nomad_example.actions.activities import get_request
    from nomad_example.actions.models import (
        ExampleWorkflowInput,
        GetRequestInput,
    )


@workflow.defn(name='nomad_example.actions.workflows.ExampleWorkflow')
class ExampleWorkflow:
    @workflow.run
    async def run(self, data: ExampleWorkflowInput) -> dict:
        retry_policy = RetryPolicy(
            maximum_attempts=3,
        )
        get_request_input = GetRequestInput(
            url='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/'
            f'cid/{data.cid}/property/Title,SMILES/JSON',
            timeout=10,
        )
        result = await workflow.execute_activity(
            get_request,
            get_request_input,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=retry_policy,
        )
        return result
