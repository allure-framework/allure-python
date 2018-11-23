class RobotStatus(object):
    FAILED = 'FAIL'
    PASSED = 'PASS'


class RobotKeywordType(object):
    SETUP = 'Setup'
    TEARDOWN = 'Teardown'
    KEYWORD = 'Keyword'
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
