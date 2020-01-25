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

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Framework :: Pytest',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Software Development :: Quality Assurance',
    'Topic :: Software Development :: Testing',
]

setup_requires = [
    "setuptools_scm"
]


install_requires = [
    "pytest>=4.5.0",
    "six>=1.9.0",
]


def prepare_version():
    from setuptools_scm import get_version
    configuration = {"root": ".."}
    version = get_version(**configuration)
    install_requires.append("allure-python-commons=={version}".format(version=version))
    return configuration


def get_readme(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def main():
    setup(
        name=PACKAGE,
        use_scm_version=prepare_version,
        description="Allure pytest integration",
        url="https://github.com/allure-framework/allure-python",
        author="QAMetaSoftware, Stanislav Seliverstov",
        author_email="sseliverstov@qameta.io",
        license="Apache-2.0",
        classifiers=classifiers,
        keywords="allure reporting pytest",
        long_description=get_readme('README.rst'),
        packages=["allure_pytest"],
        package_dir={"allure_pytest": "src"},
        entry_points={"pytest11": ["allure_pytest = allure_pytest.plugin"]},
        setup_requires=setup_requires,
        install_requires=install_requires
    )

if __name__ == '__main__':
    main()

