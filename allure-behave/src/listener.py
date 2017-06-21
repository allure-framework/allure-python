from allure.logger import AllureLogger
from allure.utils import uuid4
from allure.utils import now
from allure.types import LabelType, AttachmentType
from allure.model2 import TestResult
from allure.model2 import TestStepResult
from allure.model2 import TestBeforeResult
from allure.model2 import TestResultContainer
from allure.model2 import Status, Parameter, Label
from allure_behave.utils import scenario_parameters
from allure_behave.utils import scenario_severity
from allure_behave.utils import scenario_tags
from allure_behave.utils import scenario_name
from allure_behave.utils import scenario_history_id
from allure_behave.utils import step_status, step_status_details
from allure_behave.utils import scenario_status, scenario_status_details
from allure_behave.utils import background_status


class AllureListener(object):
    def __init__(self, result_dir):
        self.logger = AllureLogger(result_dir)
        self.current_group_uuid = None
        self.current_before_uuid = None
        self.current_scenario_uuid = None
        self.current_step_uuid = None

    def start_group(self):
        self.current_group_uuid = uuid4()
        group = TestResultContainer(uuid=self.current_group_uuid, name='Background')
        self.logger.start_group(self.current_group_uuid, group)

    def stop_group(self):
        if self.current_group_uuid:
            self.logger.stop_group(self.current_group_uuid)
            self.current_group_uuid = None

    def update_group(self):
        if self.current_group_uuid:
            self.logger.update_group(self.current_group_uuid, children=self.current_scenario_uuid)

    def start_before(self, _, background):
        self.current_before_uuid = uuid4()
        before = TestBeforeResult(name=background.name or 'Background')
        self.logger.start_before_fixture(self.current_group_uuid, self.current_before_uuid, before)

    def stop_before(self, scenario, _):
        status = background_status(scenario)
        self.logger.stop_before_fixture(uuid=self.current_before_uuid, status=status)
        self.current_before_uuid = None

    def start_scenario(self, scenario):
        self.current_scenario_uuid = uuid4()
        test_case = TestResult(uuid=self.current_scenario_uuid, start=now())

        test_case.name = scenario_name(scenario)
        test_case.historyId = scenario_history_id(scenario)
        test_case.description = '\n'.join(scenario.description)

        labels = []
        feature_label = Label(name=LabelType.FEATURE.value, value=scenario.feature.name)
        severity = (Label(name=LabelType.SEVERITY.value, value=scenario_severity(scenario).value))
        labels.append(feature_label)
        labels.append(severity)
        labels += [Label(name=LabelType.TAG.value, value=tag) for tag in scenario_tags(scenario)]

        test_case.parameters = scenario_parameters(scenario)
        test_case.labels = labels

        self.logger.schedule_test(self.current_scenario_uuid, test_case)
        self.update_group()

    def stop_scenario(self, scenario):
        status = scenario_status(scenario)
        status_details = scenario_status_details(scenario)
        self.logger.update_test(self.current_scenario_uuid, stop=now(), status=status, statusDetails=status_details)
        self.logger.close_test(self.current_scenario_uuid)
        self.current_scenario_uuid = None
        self.current_step_uuid = None

    def start_step(self, step):
        self.current_step_uuid = uuid4()
        name = '{keyword} {title}'.format(keyword=step.keyword, title=step.name)
        parent_uuid = self.current_before_uuid or self.current_scenario_uuid
        allure_step = TestStepResult(name=name, start=now())

        self.logger.start_step(parent_uuid, self.current_step_uuid, allure_step)

        if step.text:
            self.logger.attach_data(uuid4(), step.text, name='.text', attachment_type=AttachmentType.TEXT)
        if step.table:
            table = [','.join(step.table.headings)]
            [table.append(','.join(list(row))) for row in step.table.rows]
            self.logger.attach_data(uuid4(), '\n'.join(table), name='.table', attachment_type=AttachmentType.CSV)

    def stop_step(self, result):
        status = step_status(result)
        status_details = step_status_details(result)
        self.logger.stop_step(self.current_step_uuid, stop=now(), status=status, statusDetails=status_details)
