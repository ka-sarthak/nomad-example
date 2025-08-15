from nomad.actions.utils import get_action_status, start_action
from nomad.datamodel.data import EntryData
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.datamodel.metainfo.basesections.v1 import PureSubstanceSection
from nomad.metainfo import Quantity, SchemaPackage, SubSection

from nomad_example.actions.myaction.models import ExampleWorkflowInput

m_package = SchemaPackage()


class ExampleWorkflow(EntryData):
    """A section to run an example workflow using a PubChem CID."""

    cid = Quantity(
        type=int,
        description='PubChem CID of the compound.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    workflow_id = Quantity(
        type=str,
        description='Unique ID of the workflow.',
    )
    workflow_status = Quantity(
        type=str,
        description='Status of the workflow based on the available workflow ID.',
    )
    pubchem_result = SubSection(
        section_def=PureSubstanceSection,
        description='Data populated based on PubChem API call for given CID.',
    )

    trigger_run_workflow = Quantity(
        type=bool,
        description='Starts an asynchronous run of the example workflow.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.ActionEditQuantity,
            label='Run Example Workflow',
        ),
    )
    trigger_get_workflow_status = Quantity(
        type=bool,
        description='Fetches the status for the available workflow ID.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.ActionEditQuantity,
            label='Get Workflow Status',
        ),
    )

    def run_workflow(self, archive, logger=None):
        """Run the workflow with the provided archive."""
        try:
            if not self.cid:
                logger.warn(
                    'No CID provided for the workflow. Cannot run the workflow.'
                )
                return
            self.pubchem_result = None
            self.workflow_status = None
            self.workflow_id = None
            workflow_name = 'nomad_example.actions.myaction:my_action'
            input_data = ExampleWorkflowInput(
                user_id=archive.metadata.authors[0].user_id,
                upload_id=archive.metadata.upload_id,
                cid=self.cid,
            )
            self.workflow_id = start_action(action_name=workflow_name, data=input_data)
            self.trigger_get_workflow_status = True
        except Exception as e:
            logger.error(f'Error running workflow: {e}')

    def normalize(self, archive, logger=None):
        super().normalize(archive, logger)
        if self.trigger_run_workflow:
            if self.workflow_status == 'RUNNING':
                logger.warn('Workflow is already running. Cannot start a new one.')
            else:
                self.run_workflow(archive, logger)
            self.trigger_run_workflow = False
        if self.trigger_get_workflow_status:
            if self.workflow_id:
                try:
                    status = get_action_status(self.workflow_id)
                    self.workflow_status = status.name
                except Exception as e:
                    logger.error(f'Error getting workflow status: {e}. ')
            self.trigger_get_workflow_status = False


m_package.__init_metainfo__()
