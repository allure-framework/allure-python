import io
import os
import json
from attr import attrs, attrib, asdict, Factory

import uuid


TEST_GROUP_PATTERN = "{prefix}-testgroup.json"
TEST_CASE_PATTERN = "{prefix}-testcase.json"
ATTACHMENT_PATTERN = '{prefix}-attachment.{ext}'


def _write(report_dir, item, glob):
    filename = glob.format(prefix=uuid.uuid4())
    data = asdict(item)
    with io.open(os.path.join(report_dir, filename), 'w', encoding='utf-8') as file:
        file.write(unicode(json.dumps(data, indent=4, ensure_ascii=False)))


@attrs
class TestGroupResult(object):
    id = attrib(default=None)
    parentIds = attrib(default=Factory(list))
    type = attrib(default=None)
    name = attrib(default=None)
    description = attrib(default=None)
    descriptionHtml = attrib(default=None)
    befores = attrib(default=Factory(list))
    afters = attrib(default=Factory(list))
    links = attrib(default=Factory(list))
    start = attrib(default=None)
    stop = attrib(default=None)

    def write(self, report_dir):
        _write(report_dir, self, TEST_GROUP_PATTERN)


@attrs
class ExecutableItem(object):
    name = attrib(default=None)
    description = attrib(default=None)
    descriptionHtml = attrib(default=None)
    steps = attrib(default=Factory(list))
    attachments = attrib(default=Factory(list))
    parameters = attrib(default=Factory(list))
    start = attrib(default=None)
    stop = attrib(default=None)


@attrs
class TestCaseResult(ExecutableItem):
    id = attrib(default=None)
    fullName = attrib(default=None)
    parentIds = attrib(default=Factory(list))
    status = attrib(default=None)
    statusDetails = attrib(default=None)
    befores = attrib(default=Factory(list))
    afters = attrib(default=Factory(list))
    labels = attrib(default=Factory(list))
    links = attrib(default=Factory(list))

    def write(self, report_dir):
        _write(report_dir, self, TEST_CASE_PATTERN)


@attrs
class TestStepResult(ExecutableItem):
    id = attrib(default=None)
    status = attrib(default=None)
    statusDetails = attrib(default=None)


@attrs
class Parameter(object):
    name = attrib(default=None)
    value = attrib(default=None)


@attrs
class Label(object):
    name = attrib(default=None)
    value = attrib(default=None)


@attrs
class Link(object):
    type = attrib(default=None)
    url = attrib(default=None)
    name = attrib(default=None)


@attrs
class StatusDetails(object):
    message = attrib(default=None)
    trace = attrib(default=None)


@attrs
class Attachment(object):
    name = attrib(default=None)
    source = attrib(default=None)
    type = attrib(default=None)
