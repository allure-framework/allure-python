import os
from uuid import UUID
from allure_commons.utils import md5
from allure_commons.model2 import StatusDetails
from allure_commons.utils import format_exception


def get_step_name(step):
    return "{step_keyword} {step_name}".format(step_keyword=step.keyword, step_name=step.name)


def get_full_name(feature, scenario):
    feature_path = os.path.normpath(feature.rel_filename)
    return "{feature}:{scenario}".format(feature=feature_path, scenario=scenario.name)


def get_uuid(*args):
    return str(UUID(md5(*args)))


def get_status_details(exception):
    message = str(exception)
    trace = format_exception(type(exception), exception)
    return StatusDetails(message=message, trace=trace) if message or trace else None