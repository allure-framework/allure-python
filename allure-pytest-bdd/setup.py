import os
from setuptools import setup

PACKAGE = "allure-pytest-bdd"
VERSION = "2.8.6b"

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Framework :: Pytest',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Software Development :: Quality Assurance',
    'Topic :: Software Development :: Testing',
]

install_requires = [
    "pytest>=4.5.0",
    "pytest-bdd>=3.0.0",
    "six>=1.9.0",
    "allure-python-commons==2.8.6"
]


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def main():
    setup(
        name=PACKAGE,
        version=VERSION,
        description="Allure pytest-bdd integration",
        url="https://github.com/allure-framework/allure-python",
        author="QAMetaSoftware, Stanislav Seliverstov",
        author_email="sseliverstov@qameta.io",
        license="Apache-2.0",
        classifiers=classifiers,
        keywords="allure reporting pytest",
        long_description=read('README.rst'),
        packages=["allure_pytest_bdd"],
        package_dir={"allure_pytest_bdd": "src"},
        entry_points={"pytest11": ["allure_pytest_bdd = allure_pytest_bdd.plugin"]},
        install_requires=install_requires
    )

if __name__ == '__main__':
    main()

