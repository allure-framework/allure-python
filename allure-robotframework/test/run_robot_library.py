import os
from tempfile import mkdtemp
from robot import run
from robot.libraries.BuiltIn import BuiltIn
from multiprocessing import Process
from allure_commons_test.report import AllureReport


def get_example_file():
    suite_source = BuiltIn().get_variable_value("${SUITE SOURCE}")
    root = os.path.abspath(os.path.join(__file__, "..", ".."))
    examples = os.path.join(root, "examples")
    test = os.path.join(root, "test")
    return "{path}.rst".format(path=os.path.splitext(os.path.join(examples, os.path.relpath(suite_source, test)))[0])


def run_robot_with_allure(*args, **kwargs):

    allure_path = mkdtemp(dir=os.environ.get('TEST_TMP', '/tmp'))

    def run_robot(path, **kw):

        # ToDo: fix it (_core not works correctly with multiprocessing)
        # import six
        # import allure_commons
        # if six.PY2:
        #     reload(allure_commons._core)
        # else:
        #     import importlib
        #     importlib.reload(allure_commons._core)
        #
        #

        from allure_robotframework import allure_robotframework

        listener = allure_robotframework(logger_path=allure_path)
        stdout_file = os.path.abspath(os.path.join(allure_path, "..", "stdout.txt"))
        output_dir = os.path.abspath(os.path.join(allure_path, ".."))

        with open(stdout_file, 'w+') as stdout:
            options = {"listener": listener, "outputdir": output_dir, "stdout": stdout}
            options.update(kw)
            run(path, **options)

    robot_process = Process(target=run_robot, args=args, kwargs=kwargs)
    robot_process.start()
    robot_process.join()

    return AllureReport(allure_path)
