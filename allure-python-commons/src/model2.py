import io
import os
import sys
import json
import uuid
from attr import attrs, attrib, asdict
from attr import Factory


TEST_GROUP_PATTERN = "{prefix}-container.json"
TEST_CASE_PATTERN = "{prefix}-result.json"
ATTACHMENT_PATTERN = '{prefix}-attachment.{ext}'
INDENT = 4


def _write(report_dir, item, glob):
    indent = INDENT if os.environ.get("ALLURE_INDENT_OUTPUT") else None
    filename = glob.format(prefix=uuid.uuid4())
    data = asdict(item, filter=lambda attr, value: not (type(value) != bool and not bool(value)))
    with io.open(os.path.join(report_dir, filename), 'w', encoding='utf8') as json_file:
        if sys.version_info.major < 3:
            json_file.write(unicode(json.dumps(data, indent=indent, ensure_ascii=False)))
        else:
            json.dump(data, json_file, indent=indent, ensure_ascii=False)


@attrs
class TestResultContainer(object):
    uuid = attrib(default=None)
    name = attrib(default=None)
    children = attrib(default=Factory(list))
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
    status = attrib(default=None)
    statusDetails = attrib(default=None)
    stage = attrib(default=None)
    description = attrib(default=None)
    descriptionHtml = attrib(default=None)
    steps = attrib(default=Factory(list))
    attachments = attrib(default=Factory(list))
    parameters = attrib(default=Factory(list))
    start = attrib(default=None)
    stop = attrib(default=None)


@attrs
class TestResult(ExecutableItem):
    uuid = attrib(default=None)
    historyId = attrib(default=None)
    fullName = attrib(default=None)
    labels = attrib(default=Factory(list))
    links = attrib(default=Factory(list))

    def write(self, report_dir):
        _write(report_dir, self, TEST_CASE_PATTERN)


@attrs
class TestStepResult(ExecutableItem):
    id = attrib(default=None)


@attrs
class TestBeforeResult(ExecutableItem):
    pass


@attrs
class TestAfterResult(ExecutableItem):
    pass


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
    known = attrib(default=None)
    flaky = attrib(default=None)
    message = attrib(default=None)
    trace = attrib(default=None)


@attrs
class Attachment(object):
    name = attrib(default=None)
    source = attrib(default=None)
    type = attrib(default=None)


class Status(object):
    FAILED = 'failed'
    BROKEN = 'broken'
    PASSED = 'passed'
    SKIPPED = 'skipped'
