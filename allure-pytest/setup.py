import sys
from setuptools import setup

PACKAGE = "pytest-allure-adaptor"
VERSION = "2.0.3"

install_requires = [
    "pytest>=2.7.3",
    "attrs>=16.0.0",
]

if sys.version_info < (3, 4):
    install_requires.append("enum34")

def main():
    setup(
        name=PACKAGE,
        version=VERSION,
        packages=['allure'],
        package_dir={'allure': 'src/allure'},
        entry_points={'pytest11': ['allure_adaptor = allure.pytest_plugin']},
        install_requires=install_requires
    )

if __name__ == '__main__':
    main()

