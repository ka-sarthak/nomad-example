from pydantic import Field
from temporalio import workflow
from nomad.actions import TaskQueue

with workflow.unsafe.imports_passed_through():
    from nomad.config.models.plugins import ActionEntryPoint


class MyActionEntryPoint(ActionEntryPoint):
    task_queue: str = Field(
        default=TaskQueue.CPU, description='Determines the task queue for this action'
    )

    def load(self):
        from nomad.actions import Action

        from nomad_example.actions.activities import get_request
        from nomad_example.actions.workflows import ExampleWorkflow

        return Action(
            task_queue=self.task_queue,
            workflow=ExampleWorkflow,
            activities=[get_request],
        )


myaction = MyActionEntryPoint(
    name='MyAction',
    description='My custom action.',
)
