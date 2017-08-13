import os
from tempfile import mkdtemp

from nose import run
from nose.plugins import multiprocess

from allure_nose.plugin import Allure
import allure


def launch( argv=[]):
    test_dir = '../demo_tests'
    result_dir = mkdtemp()


    multiprocess._instantiate_plugins = [Allure]
    run(defaultTest=test_dir, addplugins=[Allure()],
        argv=['', '--processes=2', '--debug', '-v', '-s', '--with-allure',
              '--results-dir=%s' % result_dir] + argv)

    return [os.path.join(result_dir, name) for name in os.listdir(result_dir)]

def test_all():
    report = launch()
    print("In test finish")
    print(report)
    assert True