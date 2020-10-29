import io
import sys
from contextlib import ContextDecorator, redirect_stdout, redirect_stderr
from nose2 import main
from allure_commons import plugin_manager
from allure_commons.logger import AllureMemoryLogger
from allure_commons.logger import AllureFileLogger
from .example_loader import CurrentExample

_Allure = sys.modules['allure_nose2.plugin'].Allure


class TestAllure(_Allure):
    commandLineSwitch = (None, "test-allure", "Generate an Allure report")

    def register_allure_plugins(self):
        self.fileLoger = AllureFileLogger("examples")
        self.logger = AllureMemoryLogger()
        plugin_manager.register(self.fileLoger)
        plugin_manager.register(self.listener)
        plugin_manager.register(self.logger)

    def unregister_allure_plugins(self):
        plugin_manager.unregister(plugin=self.fileLoger)
        plugin_manager.unregister(plugin=self.listener)
        plugin_manager.unregister(plugin=self.logger)


def get_plugin(instance, plugin):
    return next(iter([p for p in instance.getCurrentSession().plugins if isinstance(p, plugin)]))


class test_context(ContextDecorator):
    def __enter__(self):
        get_plugin(main, _Allure).unregister_allure_plugins()

    def __exit__(self, exc_type, exc_val, exc_tb):
        get_plugin(main, _Allure).register_allure_plugins()


@test_context()
def run_docstring_example(**kwargs):
    kwargs['exit'] = False
    # kwargs['plugins'] = ["test.common", "nose2.plugins.mp"]
    # kwargs['argv'] = ('nose2', '--test-allure', '--processes=2')

    kwargs['plugins'] = ["test.example_runner"]
    kwargs['argv'] = ('nose2', '--test-allure')

    kwargs['module'] = get_plugin(main, CurrentExample).get_example_module()

    test_nose2 = type("TestNose2", (main,), {})
    stdout = io.StringIO()
    stderr = io.StringIO()

    with redirect_stderr(stderr):
        with redirect_stdout(stdout):
            test_nose2_instance = test_nose2(**kwargs)

    #test_nose2_instance = test_nose2(**kwargs)

    return get_plugin(test_nose2_instance, _Allure).logger

