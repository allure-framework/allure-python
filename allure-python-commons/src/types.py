from enum import Enum

ALLURE_UNIQUE_LABELS = ['severity', 'thread', 'host']


class Severity(str, Enum):
    BLOCKER = 'blocker'
    CRITICAL = 'critical'
    NORMAL = 'normal'
    MINOR = 'minor'
    TRIVIAL = 'trivial'


class LinkType(object):
    LINK = 'link'
    ISSUE = 'issue'
    TEST_CASE = 'test_case'


class LabelType(str, Enum):
    EPIC = 'epic'
    FEATURE = 'feature'
    STORY = 'story'
    SEVERITY = 'severity'
    THREAD = 'thread'
    HOST = 'host'
    TAG = 'tag'
    FRAMEWORK = 'framework'
    LANGUAGE = 'language'


class AttachmentType(Enum):

    def __init__(self, mime_type, extension):
        self.mime_type = mime_type
        self.extension = extension

    TEXT = ("text/plain", "txt")
    CSV = ("text/csv", "csv")
    TSV = ("text/tab-separated-values", "tsv")
    URI_LIST = ("text/uri-list", "uri")

    HTML = ("text/html", "html")
    XML = ("application/xml", "xml")
    JSON = ("application/json", "json")
    YAML = ("application/yaml", "yaml")
    PCAP = ("application/vnd.tcpdump.pcap", "pcap")

    PNG = ("image/png", "png")
    JPG = ("image/jpg", "jpg")
    SVG = ("image/svg-xml", "svg")
    GIF = ("image/gif", "gif")
    BMP = ("image/bmp", "bmp")
    TIFF = ("image/tiff", "tiff")

    MP4 = ("video/mp4", "mp4")
    OGG = ("video/ogg", "ogg")
    WEBM = ("video/webm", "webm")
