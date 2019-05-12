import os
from setuptools import setup

PACKAGE = "allure-behave"
VERSION = "2.6.3"

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Software Development :: Quality Assurance',
    'Topic :: Software Development :: Testing',
    'Topic :: Software Development :: Testing :: BDD'
]

install_requires = [
    "behave>=1.2.5",
    "allure-python-commons==2.6.3"
]


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def main():
    setup(
        name=PACKAGE,
        version=VERSION,
        description="Allure behave integration",
        url="https://github.com/allure-framework/allure-python",
        author="QAMetaSoftware, Stanislav Seliverstov",
        author_email="sseliverstov@qameta.io",
        license="Apache-2.0",
        classifiers=classifiers,
        keywords="allure reporting behave",
        long_description=read('README.rst'),
        packages=["allure_behave"],
        package_dir={"allure_behave": "src"},
        install_requires=install_requires
    )

if __name__ == '__main__':
    main()

