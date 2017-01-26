from enum import Enum

ALLURE_LABEL_PREFIX = 'allure_label'
ALLURE_LINK_PREFIX = 'allure_link'


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


class LinkType(object):
    LINK = 'link'
    ISSUE = 'issue'
    TEST_CASE = 'test_case'


class LabelType(Enum):
    def __init__(self, name, unique):
        self.label_name = name
        self.is_unique = unique

    def __str__(self):
        return self.label_name

    FEATURE = ('feature', False)
    STORY = ('story', False)
    SEVERITY = ('severity', True)
    THREAD = ('thread', True)
    HOST = ('host', True)


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
