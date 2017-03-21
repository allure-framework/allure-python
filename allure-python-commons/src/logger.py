import os
import shutil
from six import text_type
from collections import OrderedDict

from allure_commons.constants import AttachmentType
from allure_commons.model2 import ExecutableItem
from allure_commons.model2 import Attachment, ATTACHMENT_PATTERN
from allure_commons.utils import now


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

    def stop_group(self, uuid, **kwargs):
        self._update_item(uuid, **kwargs)
        group = self._items.pop(uuid)
        group.write(self._report_dir)

    def update_group(self, uuid, **kwargs):
        self._update_item(uuid, **kwargs)

    def start_before_fixture(self, parent_uuid, uuid, fixture):
        self._items.get(parent_uuid).befores.append(fixture)
        self._items[uuid] = fixture

    def stop_before_fixture(self, uuid, **kwargs):
        self._update_item(uuid, **kwargs)
        self._items.pop(uuid)

    def start_after_fixture(self, parent_uuid, uuid, fixture):
        self._items.get(parent_uuid).afters.append(fixture)
        self._items[uuid] = fixture

    def stop_after_fixture(self, uuid, **kwargs):
        self._update_item(uuid, **kwargs)
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
        parent_uuid = None
        for _uuid in reversed(self._items):
            if isinstance(self._items[_uuid], ExecutableItem):
                parent_uuid = _uuid
                break
        if parent_uuid:
            self._items[parent_uuid].steps.append(step)
        self._items[uuid] = step

    def stop_step(self, uuid, **kwargs):
        self._update_item(uuid, **kwargs)
        self._items.pop(uuid)

    def _attach(self, uuid, name=None, attachment_type=None, extension=None):
        mime_type = attachment_type
        extension = extension if extension else 'attach'

        if type(attachment_type) is AttachmentType:
            extension = attachment_type.extension
            mime_type = attachment_type.mime_type

        file_name = ATTACHMENT_PATTERN.format(prefix=uuid, ext=extension)
        destination = os.path.join(self._report_dir, file_name)
        attachment = Attachment(source=file_name, name=name, type=mime_type)
        last_uuid = next(reversed(self._items))
        self._items[last_uuid].attachments.append(attachment)

        return file_name, destination

    def attach_file(self, uuid, source, name=None, attachment_type=None, extension=None):
        file_name, destination = self._attach(uuid, name=name, attachment_type=attachment_type, extension=extension)
        shutil.copy2(source, destination)

    def attach_data(self, uuid, body, name=None, attachment_type=None, extension=None):
        file_name, destination = self._attach(uuid, name=name, attachment_type=attachment_type, extension=extension)

        with open(destination, 'wb') as attached_file:
            if isinstance(body, text_type):
                attached_file.write(body.encode('utf-8'))
            else:
                attached_file.write(body)
