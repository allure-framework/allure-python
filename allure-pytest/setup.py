from setuptools import setup

PACKAGE = "allure-pytest"
VERSION = "2.0.0b1"

classifiers = [
    'Development Status :: 4 - Beta',
    'Framework :: Pytest',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Software Development :: Quality Assurance',
    'Topic :: Software Development :: Testing',
]

install_requires = [
    "pytest>=2.7.3",
    "allure-python-commons==2.0.0b1"
]

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
        keywords="allure reporting pytest",
        packages=["allure"],
        package_dir={"allure": "src/allure"},
        entry_points={"pytest11": ["allure_pytest = allure.pytest_plugin"]},
        install_requires=install_requires
    )

if __name__ == '__main__':
    main()

