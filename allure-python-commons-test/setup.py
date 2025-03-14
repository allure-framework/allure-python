import os
from setuptools import setup

PACKAGE = "allure-python-commons-test"

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Software Development :: Quality Assurance',
    'Topic :: Software Development :: Testing',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Programming Language :: Python :: 3.13',
]

install_requires = [
    "pyhamcrest>=1.9.0"
]


def get_readme(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def main():
    setup(
        name=PACKAGE,
        use_scm_version={"root": "..", "relative_to": __file__},
        setup_requires=['setuptools_scm'],
        description=(
            "A collection of PyHamcrest matchers to test Allure adapters for "
            "Python test frameworks"
        ),
        url="https://allurereport.org/",
        project_urls={
            "Source": "https://github.com/allure-framework/allure-python",
        },
        author="Qameta Software Inc., Stanislav Seliverstov",
        author_email="sseliverstov@qameta.io",
        license="Apache-2.0",
        classifiers=classifiers,
        keywords="allure reporting testing matchers",
        long_description=get_readme("README.md"),
        long_description_content_type="text/markdown",
        packages=["allure_commons_test"],
        package_dir={"allure_commons_test": "src"},
        install_requires=install_requires
    )

if __name__ == '__main__':
    main()
