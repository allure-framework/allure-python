from enum import Enum

ALLURE_LABEL_PREFIX = 'allure_label'
ALLURE_LINK_PREFIX = 'allure_link'
ALLURE_UNIQUE_LABELS = ['severity', 'thread', 'host']


class Status(object):
    FAILED = 'failed'
    BROKEN = 'broken'
    PASSED = 'passed'
    CANCELED = 'canceled'
    PENDING = 'pending'


class Severity(Enum):
    BLOCKER = 'blocker'
    CRITICAL = 'critical'
    NORMAL = 'normal'
    MINOR = 'minor'
    TRIVIAL = 'trivial'


class LinkType(Enum):
    def __str__(self):
        return self.value

    LINK = 'link'
    ISSUE = 'issue'
    TEST_CASE = 'test_case'


class LabelType(Enum):
    FEATURE = 'feature'
    STORY = 'story'
    SEVERITY = 'severity'
    THREAD = 'thread'
    HOST = 'host'


class AttachmentType(Enum):

    def __init__(self, mime_type, extension):
        self.mime_type = mime_type
        self.extension = extension

    TEXT = ("text/plain", "txt")
    HTML = ("application/html", "html")
    XML = ("application/xml", "xml")
    JSON = ("application/json", "json")
    PNG = ("image/png", "png")
    JPG = ("image/jpg", "jpg")
    SVG = ("image/svg-xml", "svg")
