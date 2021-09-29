import os
from tempfile import mkdtemp
import allure_commons
from allure_commons_test.report import AllureReport
from behave.parser import Parser
from behave.runner import ModelRunner
from behave.configuration import Configuration
from behave.formatter._registry import make_formatters
from behave.formatter.base import StreamOpener
import tempfile
from contextlib import contextmanager


@given(u'feature definition')
@given(u'feature definition {lang}')
def feature_definition(context, **kwargs):
    parser = Parser(language=kwargs.get('lang', None))
    feature = parser.parse(context.text)
    if hasattr(context, "feature_definition"):
        context.feature_definition.append(feature)
    else:
        context.feature_definition = [feature]


@given(u'hooks implementation')
def hooks_implementations(context):
    context.globals = {}
    exec(context.text, context.globals)


@given(u'test plan')
def test_plan_helper(context):
    tmp_dir = os.environ.get("TEST_TMP")
    file, filename = tempfile.mkstemp(suffix=".json", dir=tmp_dir)
    os.environ["ALLURE_TESTPLAN_PATH"] = filename
    with os.fdopen(file, 'w') as tmp:
        tmp.write(context.text)
    context.test_plan = filename


@when(u'I run behave with allure formatter')
@when(u'I run behave with allure formatter with options "{args}"')
def run_behave_with_allure(context, **kwargs):
    with test_context():
        cmd_args = '-f allure_behave.formatter:AllureFormatter'
        cmd = '{options} {cmd}'.format(cmd=cmd_args, options=kwargs.get('args', ''))
        config = Configuration(command_args=cmd)
        result_tmp_dir = mkdtemp(dir=os.environ.get('TEST_TMP', None))
        stream_opener = StreamOpener(filename=result_tmp_dir)
        model_runner = ModelRunner(config, context.feature_definition)
        model_runner.formatters = make_formatters(config, [stream_opener])
        model_runner.hooks = getattr(context, 'globals', dict())
        model_runner.run()
        context.allure_report = AllureReport(result_tmp_dir)

    os.environ.pop("ALLURE_TESTPLAN_PATH", None)


@contextmanager
def test_context():
    def _unregister_plugins():
        plugins = []
        for name, plugin in allure_commons.plugin_manager.list_name_plugin():
            allure_commons.plugin_manager.unregister(plugin=plugin, name=name)
            plugins.append(plugin)
        return plugins

    plugins = _unregister_plugins()
    yield
    _unregister_plugins()
    for plugin in plugins:
        allure_commons.plugin_manager.register(plugin)
