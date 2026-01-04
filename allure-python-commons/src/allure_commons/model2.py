from __future__ import annotations

from attr import attrs, attrib
from attr import Factory

TEST_GROUP_PATTERN = "{prefix}-container.json"
TEST_CASE_PATTERN = "{prefix}-result.json"
ATTACHMENT_PATTERN = "{prefix}-attachment.{ext}"
INDENT = 4


@attrs
class TestResultContainer:
    file_pattern = TEST_GROUP_PATTERN

    uuid: str = attrib(default=None)
    name: str | None = attrib(default=None)
    children: list[str] = attrib(default=Factory(list))
    description: str | None = attrib(default=None)
    descriptionHtml: str | None = attrib(default=None)
    befores: list[TestBeforeResult] = attrib(default=Factory(list))
    afters: list[TestAfterResult] = attrib(default=Factory(list))
    links: list[Link] = attrib(default=Factory(list))
    start: int | None = attrib(default=None)
    stop: int | None = attrib(default=None)


@attrs
class ExecutableItem:
    name: str | None = attrib(default=None)
    status: str | None = attrib(default=None)
    statusDetails: StatusDetails | None = attrib(default=None)
    stage: str | None = attrib(default=None)
    description: str | None = attrib(default=None)
    descriptionHtml: str | None = attrib(default=None)
    steps: list[TestStepResult] = attrib(default=Factory(list))
    attachments: list[Attachment] = attrib(default=Factory(list))
    parameters: list[Parameter] = attrib(default=Factory(list))
    start: int | None = attrib(default=None)
    stop: int | None = attrib(default=None)


@attrs
class TestResult(ExecutableItem):
    file_pattern = TEST_CASE_PATTERN

    uuid: str = attrib(default=None)
    historyId: str | None = attrib(default=None)
    testCaseId: str | None = attrib(default=None)
    fullName: str | None = attrib(default=None)
    labels: list[Label] = attrib(default=Factory(list))
    links: list[Link] = attrib(default=Factory(list))
    titlePath: list[str] = attrib(default=Factory(list))


@attrs
class TestStepResult(ExecutableItem):
    id: str | None = attrib(default=None)


@attrs
class TestBeforeResult(ExecutableItem):
    pass


@attrs
class TestAfterResult(ExecutableItem):
    pass


@attrs
class Parameter:
    name: str = attrib(default=None)
    value: str = attrib(default=None)
    excluded: bool | None = attrib(default=None)
    mode: str | None = attrib(default=None)


@attrs
class Label:
    name: str = attrib(default=None)
    value: str = attrib(default=None)


@attrs
class Link:
    type: str | None = attrib(default=None)
    url: str = attrib(default=None)
    name: str | None = attrib(default=None)


@attrs
class StatusDetails:
    known: bool | None = attrib(default=None)
    flaky: bool | None = attrib(default=None)
    message: str | None = attrib(default=None)
    trace: str | None = attrib(default=None)

@attrs
class Attachment:
    name: str = attrib(default=None)
    source: str = attrib(default=None)
    type: str | None = attrib(default=None)


class Status:
    FAILED = "failed"
    BROKEN = "broken"
    PASSED = "passed"
    SKIPPED = "skipped"
    UNKNOWN = "unknown"
