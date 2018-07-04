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


class RobotBasicKeywords(object):
    BUILTIN_LIB = 'BuiltIn'
    NO_OPERATION = BUILTIN_LIB + '.No Operation'
    FAIL = BUILTIN_LIB + '.Fail'
    LOG = BUILTIN_LIB + '.Log'
