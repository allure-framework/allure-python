class RobotStatus(object):
    FAILED = 'FAIL'
    PASSED = 'PASS'
    SKIPPED = 'SKIP'


class RobotKeywordType(object):
    SETUP = 'SETUP'
    TEARDOWN = 'TEARDOWN'
    KEYWORD = 'KEYWORD'
    LOOP = 'FOR'
    LOOP_ITEM = 'FOR ITEM'
    FIXTURES = [SETUP, TEARDOWN]


class RobotLogLevel(object):
    FAIL = 'FAIL'
    ERROR = 'ERROR'
    WARNING = 'WARN'
    INFORMATION = 'INFO'
    DEBUG = 'DEBUG'
    TRACE = 'TRACE'

    CRITICAL_LEVELS = [FAIL, ERROR]
