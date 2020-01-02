from collections import OrderedDict
from contextlib import contextmanager
from ._core import plugin_manager
from .model2 import TestResult
from .model2 import TestStepResult
from .model2 import ExecutableItem
from .utils import uuid4
from .utils import now


class AllureLifecycle(object):
    def __init__(self):
        self._items = OrderedDict()

    def _get_item(self, uuid=None, item_type=None):
        uuid = uuid or self._last_item_uuid(item_type=item_type)
        return self._items.get(uuid)

    def _pop_item(self, uuid=None, item_type=None):
        uuid = uuid or self._last_item_uuid(item_type=item_type)
        return self._items.pop(uuid, None)

    def _last_item_uuid(self, item_type=None):
        for uuid in reversed(self._items):
            item = self._items.get(uuid)
            if item_type is None:
                return uuid
            elif type(item) == item_type or isinstance(item, item_type):
                return uuid

    @contextmanager
    def schedule_test_case(self, uuid=None):
        test_result = TestResult()
        test_result.uuid = uuid or uuid4()
        self._items[test_result.uuid] = test_result
        yield test_result

    @contextmanager
    def update_test_case(self, uuid=None):
        yield self._get_item(uuid=uuid, item_type=TestResult)

    def write_test_case(self, uuid=None):
        test_result = self._pop_item(uuid=uuid, item_type=TestResult)
        if test_result:
            plugin_manager.hook.report_result(result=test_result)

    @contextmanager
    def start_step(self, parent_uuid=None, uuid=None):
        parent = self._get_item(uuid=parent_uuid, item_type=ExecutableItem)
        step = TestStepResult()
        step.start = now()
        parent.steps.append(step)
        self._items[uuid or uuid4()] = step
        yield step

    @contextmanager
    def update_step(self, uuid=None):
        yield self._get_item(uuid=uuid, item_type=TestStepResult)

    def stop_step(self, uuid=None):
        step = self._pop_item(uuid=uuid, item_type=TestStepResult)
        if step and not step.stop:
            step.stop = now()
