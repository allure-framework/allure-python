import os
from setuptools import setup

PACKAGE = "allure-pytest-bdd"

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Framework :: Pytest',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Software Development :: Quality Assurance',
    'Topic :: Software Development :: Testing',
    'Topic :: Software Development :: Testing :: BDD',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Programming Language :: Python :: 3.13',
]

setup_requires = [
    "setuptools_scm"
]

install_requires = [
    "pytest>=4.5.0",
    "pytest-bdd>=5.0.0"
]


def prepare_version():
    from setuptools_scm import get_version
    configuration = {"root": "..", "relative_to": __file__}
    version = get_version(**configuration)
    install_requires.append(f"allure-python-commons=={version}")
    return configuration


def get_readme(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def main():
    setup(
        name=PACKAGE,
        use_scm_version=prepare_version,
        description="Allure pytest-bdd integration",
        url="https://allurereport.org/",
        project_urls={
            "Source": "https://github.com/allure-framework/allure-python",
        },
        author="Qameta Software Inc., Stanislav Seliverstov",
        author_email="sseliverstov@qameta.io",
        license="Apache-2.0",
        classifiers=classifiers,
        keywords="allure reporting pytest",
        long_description=get_readme("README.md"),
        long_description_content_type="text/markdown",
        packages=["allure_pytest_bdd"],
        package_dir={"allure_pytest_bdd": "src"},
        entry_points={"pytest11": ["allure_pytest_bdd = allure_pytest_bdd.plugin"]},
        setup_requires=setup_requires,
        install_requires=install_requires
    )


if __name__ == '__main__':
    main()
