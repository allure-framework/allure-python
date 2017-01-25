import os
import shutil
from collections import OrderedDict

from allure.model2 import ExecutableItem
from allure.model2 import Attachment, ATTACHMENT_PATTERN
from allure.utils import now


class AllureLogger(object):
    def __init__(self, report_dir):
        self._items = OrderedDict()
        self._report_dir = report_dir

    def _update_item(self, uuid, **kwargs):
        item = self._items[uuid]
        for name, value in kwargs.items():
            attr = getattr(item, name)
            if isinstance(attr, list):
                attr.append(value)
            else:
                setattr(item, name, value)

    def get_item(self, uuid):
        return self._items.get(uuid)

    def start_group(self, uuid, group):
        self._items[uuid] = group

    def stop_group(self, uuid):
        group = self._items.pop(uuid)
        group.write(self._report_dir)

    def start_before_fixture(self, parent_uuid, uuid, fixture):
        self._items.get(parent_uuid).befores.append(fixture)
        self._items[uuid] = fixture

    def stop_before_fixture(self, uuid, **kwargs):
        self._update_item(uuid, **kwargs)
        self._items.pop(uuid)

    def start_after_fixture(self, parent_uuid, uuid, **kwargs):
        fixture = ExecutableItem(start=now(), **kwargs)
        self._items.get(parent_uuid).afters.append(fixture)
        self._items[uuid] = fixture

    def stop_after_fixture(self, uuid):
        fixture = self._items.pop(uuid)
        fixture.stop = now()

    def schedule_test(self, uuid, test_case):
        self._items[uuid] = test_case

    def update_test(self, uuid, **kwargs):
        self._update_item(uuid, **kwargs)

    def close_test(self, uuid):
        test_case = self._items.pop(uuid)
        test_case.write(self._report_dir)

    def start_step(self, uuid, step):
        last_uuid = next(reversed(self._items))
        self._items[last_uuid].steps.append(step)
        self._items[uuid] = step

    def stop_step(self, uuid, **kwargs):
        self._update_item(uuid, **kwargs)
        self._items.pop(uuid)

    def attach(self, uuid, name, source, mime_type, extension):
        attach_file = ATTACHMENT_PATTERN.format(prefix=uuid, ext=extension)
        destination = os.path.join(self._report_dir, attach_file)
        shutil.copy2(source, destination)
        attachment = Attachment(name, attach_file, mime_type)
        last_uuid = next(reversed(self._items))
        self._items[last_uuid].attachments.append(attachment)
