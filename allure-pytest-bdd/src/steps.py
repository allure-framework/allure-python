from allure_commons.model2 import StatusDetails
from allure_commons.model2 import Status
from allure_commons.model2 import Parameter
from allure_commons.utils import format_exception
from allure_commons.utils import represent

from .storage import save_reported_step
from .utils import get_uuid
from .utils import get_status
from .utils import get_status_details
from .utils import get_test_data


def get_step_name(step):
    return f"{step.keyword} {step.name}"


def get_step_uuid(step):
    return get_uuid(str(id(step)))


def start_step(lifecycle, step_uuid, title, params=None, parent_uuid=None):
     with lifecycle.start_step(uuid=step_uuid, parent_uuid=parent_uuid) as step_result:
        step_result.name = title
        if params:
            step_result.parameters.extend(
                Parameter(
                    name=name,
                    value=represent(value),
                ) for name, value in params.items()
            )


def stop_step(lifecycle, uuid, status=None, status_details=None, exception=None, exception_type=None, traceback=None):
    with lifecycle.update_step(uuid=uuid) as step_result:
        if step_result is None:
            return False
        step_result.status = status or get_status(exception)
        step_result.statusDetails = status_details or get_status_details(exception, exception_type, traceback)
    lifecycle.stop_step(uuid=uuid)
    return True


def start_gherkin_step(lifecycle, item, step, step_uuid=None):
    if step_uuid is None:
        step_uuid = get_step_uuid(step)

    start_step(
        lifecycle,
        step_uuid=step_uuid,
        title=get_step_name(step),
        parent_uuid=get_uuid(item.nodeid),
    )


def stop_gherkin_step(lifecycle, item, step_uuid, **kwargs):
    res = stop_step(lifecycle, step_uuid, **kwargs)
    if res:
        save_reported_step(item, step_uuid)
    return res


def ensure_gherkin_step_reported(lifecycle, item, step, step_uuid=None, **kwargs):

    if not step_uuid:
        step_uuid = get_step_uuid(step)

    if stop_gherkin_step(lifecycle, item, step_uuid, **kwargs):
        return

    start_gherkin_step(lifecycle, item, step, step_uuid)
    stop_gherkin_step(lifecycle, item, step_uuid, **kwargs)


def report_undefined_step(lifecycle, item, step, exception):
    ensure_gherkin_step_reported(
        lifecycle,
        item,
        step,
        status=Status.BROKEN,
        status_details=StatusDetails(
            message=format_exception(type(exception), exception),
        ),
    )


def report_remaining_steps(lifecycle, item):
    test_data = get_test_data(item)
    scenario = test_data.scenario
    excinfo = test_data.excinfo
    reported_steps = test_data.reported_steps

    for step in scenario.steps:
        step_uuid = get_step_uuid(step)
        if step_uuid not in reported_steps:
            __report_remaining_step(lifecycle, item, step, step_uuid, excinfo)
            excinfo = None # Only show the full message and traceback once


def __report_remaining_step(lifecycle, item, step, step_uuid, excinfo):
    args = [lifecycle, item, step, step_uuid]
    kwargs = {
        "exception": excinfo.value,
        "exception_type": excinfo.type,
        "traceback": excinfo.tb,
    } if __is_step_running(lifecycle, step_uuid) and excinfo else { "status": Status.SKIPPED }

    ensure_gherkin_step_reported(*args, **kwargs)


def __is_step_running(lifecycle, step_uuid):
    with lifecycle.update_step(uuid=step_uuid) as step_result:
        return step_result is not None
