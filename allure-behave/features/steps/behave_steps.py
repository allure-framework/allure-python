import os
from tempfile import mkdtemp
from allure_testing.report import AllureReport
from behave.parser import Parser
from behave.runner import ModelRunner
from behave.configuration import Configuration
from behave.formatter._registry import make_formatters
from behave.formatter.base import StreamOpener


@given(u'feature definition')
@given(u'feature definition {lang}')
def feature_definition(context, **kwargs):
    parser = Parser(language=kwargs.get('lang', None))
    context.feature_definition = parser.parse(context.text)


@when(u'I run behave with allure formatter')
@when(u'I run behave with allure formatter with options "{args}"')
def run_behave_with_allure(context, **kwargs):
    cmd_args = '-v -f allure_behave.formatter:AllureFormatter -f pretty'
    cmd = '{options} {cmd}'.format(cmd=cmd_args, options=kwargs.get('args', ''))
    config = Configuration(command_args=cmd)

    result_tmp_dir = mkdtemp(dir=os.environ.get('TEST_TMP', None))
    stream_opener = StreamOpener(filename=result_tmp_dir)

    model_runner = ModelRunner(config, [context.feature_definition])
    model_runner.formatters = make_formatters(config, [stream_opener])
    model_runner.run()

    context.allure_report = AllureReport(result_tmp_dir)
