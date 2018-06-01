
import os
from setuptools import setup

install_requires = [
    "allure-python-commons==2.3.1b1",
    "robotframework==3.0.2"
]

PACKAGE = "allure-robotframework"
VERSION = "0.1.3"


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


if __name__ == '__main__':
    setup(
        name=PACKAGE,
        version=VERSION,
        description="Allure Robot Framework integration",
        license="Apache-2.0",
        keywords="allure reporting robotframework",
        packages=['allure_robotframework'],
        package_dir={"allure_robotframework": "src"},
        install_requires=install_requires,
        py_modules=['allure_robotframework'],
        url="https://github.com/skhomuti/allure-python",
        author="Sergey Khomutinin",
        author_email="skhomuti@gmail.com",
        long_description=read('README.rst'),
    )
