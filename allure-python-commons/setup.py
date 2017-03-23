import sys
from setuptools import setup

PACKAGE = "allure-python-commons"
VERSION = "2.0.4"


install_requires = [
    "attrs>=16.0.0",
]

if sys.version_info < (3, 4):
    install_requires.append("enum34")


def main():
    setup(
        name=PACKAGE,
        version=VERSION,
        packages=['allure_commons'],
        package_dir={'allure_commons': 'src'},
        install_requires=install_requires
    )

if __name__ == '__main__':
    main()
