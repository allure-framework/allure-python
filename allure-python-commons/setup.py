import sys
from setuptools import setup

PACKAGE = "allure-python-commons"
VERSION = "2.2.2b2"

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Software Development :: Quality Assurance',
    'Topic :: Software Development :: Testing',
]

install_requires = [
    "attrs>=16.0.0",
    "six>=1.9.0",
    "pluggy>=0.4.0"
]

if sys.version_info < (3, 4):
    install_requires.append("enum34")


def main():
    setup(
        name=PACKAGE,
        version=VERSION,
        description="Common module for integrate allure with python-based frameworks",
        url="https://github.com/allure-framework/allure-python2",
        author="QAMetaSoftware, Stanislav Seliverstov",
        author_email="sseliverstov@qameta.io",
        license="Apache-2.0",
        classifiers=classifiers,
        keywords="allure reporting report-engine",
        packages=["allure_commons"],
        package_dir={"allure_commons": 'src'},
        install_requires=install_requires,
        py_modules=['allure', 'allure_commons']
    )

if __name__ == '__main__':
    main()
