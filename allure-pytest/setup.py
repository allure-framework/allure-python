import os,sys
from setuptools import setup
from pkg_resources import require, DistributionNotFound, VersionConflict

try:
    require('pytest-allure-adaptor')
    print("""
    You have pytest-allure-adaptor installed.
    You need to remove pytest-allure-adaptor from your site-packages
    before installing allure-pytest, or conflicts may result.
    """)
    sys.exit()
except (DistributionNotFound, VersionConflict):
    pass

PACKAGE = "allure-pytest"
VERSION = "2.5.0"

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Framework :: Pytest',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Software Development :: Quality Assurance',
    'Topic :: Software Development :: Testing',
]

install_requires = [
    "pytest>=3.3.0",
    "six>=1.9.0",
    "allure-python-commons==2.5.0"
]


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def main():
    setup(
        name=PACKAGE,
        version=VERSION,
        description="Allure pytest integration",
        url="https://github.com/allure-framework/allure-python",
        author="QAMetaSoftware, Stanislav Seliverstov",
        author_email="sseliverstov@qameta.io",
        license="Apache-2.0",
        classifiers=classifiers,
        keywords="allure reporting pytest",
        long_description=read('README.rst'),
        packages=["allure_pytest"],
        package_dir={"allure_pytest": "src"},
        entry_points={"pytest11": ["allure_pytest = allure_pytest.plugin"]},
        install_requires=install_requires
    )

if __name__ == '__main__':
    main()

