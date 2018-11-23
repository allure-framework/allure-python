import os
from tempfile import mkdtemp
from robot import run
from multiprocessing import Process
from allure_commons_test.report import AllureReport


def run_robot_with_allure(*args, **kwargs):
    root = os.path.abspath(os.path.join(__file__, "..", ".."))
    targets = map(lambda target: os.path.join(root, target), args)
    tmp_path = mkdtemp(dir=os.environ.get('TEST_TMP', '/tmp'))

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

        listener = allure_robotframework(logger_path=tmp_path)
        stdout_file = os.path.abspath(os.path.join(tmp_path, "..", "stdout.txt"))
        output_path = os.path.abspath(os.path.join(tmp_path, ".."))

        with open(stdout_file, 'w+') as stdout:
            options = {"listener": listener, "outputdir": output_path, "stdout": stdout}
            options.update(kw)
            run(path, **options)

    robot_process = Process(target=run_robot, args=targets, kwargs=kwargs)
    robot_process.start()
    robot_process.join()

    return AllureReport(tmp_path)
