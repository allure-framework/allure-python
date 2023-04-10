from enum import Enum

ALLURE_UNIQUE_LABELS = ['severity', 'thread', 'host']


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
    CSV = ("text/csv", "csv")
    TSV = ("text/tab-separated-values", "tsv")

    HTML = ("application/html", "html")
    XML = ("application/xml", "xml")
    JSON = ("application/json", "json")
    YAML = ("application/yaml", "yaml")

    PNG = ("image/png", "png")
    JPG = ("image/jpg", "jpg")
    SVG = ("image/svg-xml", "svg")
    GIF = ("image/gif", "gif")
    BMP = ("iamge/bmp", "bmp")
    TIFF = ("image/tiff", "tiff")

    MP4 = ("video/mp4", "mp4")
    OGG = ("video/ogg", "ogg")
    WEBM = ("video/webm", "webm")
