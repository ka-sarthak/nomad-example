from nomad.config.models.plugins import WorkflowEntryPoint


class MyActionEntryPoint(WorkflowEntryPoint):
    def load(self):
        from nomad.orchestrator.base import BaseWorkflowHandler
        from nomad.orchestrator.shared.constant import TaskQueue

        from nomad_example.actions.activities import get_request
        from nomad_example.actions.workflows import ExampleWorkflow

        return BaseWorkflowHandler(
            workflows=[ExampleWorkflow],
            activities=[get_request],
            task_queue=TaskQueue.CPU,
        )


myaction = MyActionEntryPoint(
    name='MyAction',
    description='My custom action.',
)
