from enum import Enum

ALLURE_LABEL_PREFIX = 'allure_label'
ALLURE_LINK_PREFIX = 'allure_link'


class Status(object):
    FAILED = 'failed'
    BROKEN = 'broken'
    PASSED = 'passed'
    CANCELED = 'canceled'
    PENDING = 'pending'


class Link(object):
    LINK = 'link'
    ISSUE = 'issue'
    TEST_CASE = 'test_case'


class Label(object):
    FEATURE = 'feature'
    STORY = 'story'
    SEVERITY = 'severity'
    THREAD = 'thread'
    HOST = 'host'


class Severity(Enum):
    BLOCKER = 'blocker'
    CRITICAL = 'critical'
    NORMAL = 'normal'
    MINOR = 'minor'
    TRIVIAL = 'trivial'


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
