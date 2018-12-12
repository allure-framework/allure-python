
from robot.libraries.BuiltIn import BuiltIn


def fail_with_traceback(traceback_message):
    BuiltIn().fail(traceback_message)
