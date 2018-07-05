import allure_commons
from allure_commons.utils import now
from allure_commons.utils import uuid4
from allure_commons.model2 import TestStepResult
from allure_commons.model2 import Status, StatusDetails
from allure_commons.model2 import Parameter
from allure_commons.utils import format_exception, format_traceback


def get_status(exception):
    if exception and isinstance(exception, AssertionError):
        return Status.FAILED
    elif exception:
        return Status.BROKEN
    return Status.PASSED


def get_status_details(exc_type, exception, exc_traceback):
    if exception:
        return StatusDetails(message=format_exception(exc_type, exception),
                             trace=format_traceback(exc_traceback))


class AllureListener(object):
    def __init__(self, logger):
        self.logger = logger

    @allure_commons.hookimpl
    def attach_data(self, body, name, attachment_type, extension):
        self.logger.attach_data(uuid4(), body, name=name, attachment_type=attachment_type, extension=extension)

    @allure_commons.hookimpl
    def attach_file(self, source, name, attachment_type, extension):
        self.logger.attach_file(uuid4(), source, name=name, attachment_type=attachment_type, extension=extension)

    @allure_commons.hookimpl
    def start_step(self, uuid, title, params):
        parameters = [Parameter(name=name, value=value) for name, value in params.items()]
        step = TestStepResult(name=title, start=now(), parameters=parameters)
        self.logger.start_step(None, uuid, step)

    @allure_commons.hookimpl
    def stop_step(self, uuid, exc_type, exc_val, exc_tb):
        self.logger.stop_step(uuid,
                              stop=now(),
                              status=get_status(exc_val),
                              statusDetails=get_status_details(exc_type, exc_val, exc_tb))
