import os
from setuptools import setup

PACKAGE = "allure-robotframework"

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Framework :: Robot Framework',
    'Framework :: Robot Framework :: Tool',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Software Development :: Quality Assurance',
    'Topic :: Software Development :: Testing',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
]

setup_requires = [
    "setuptools_scm"
]

install_requires = [
]


def prepare_version():
    from setuptools_scm import get_version
    configuration = {"root": "..", "relative_to": __file__}
    version = get_version(**configuration)
    install_requires.append("allure-python-commons=={version}".format(version=version))
    return configuration


def get_readme(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


if __name__ == '__main__':
    setup(
        name=PACKAGE,
        use_scm_version=prepare_version,
        description="Allure Robot Framework integration",
        license="Apache-2.0",
        install_requires=install_requires,
        setup_requires=setup_requires,
        keywords="allure reporting robotframework",
        packages=['allure_robotframework', 'AllureLibrary'],
        package_dir={"allure_robotframework": "src/listener", 'AllureLibrary': 'src/library'},
        py_modules=['allure_robotframework'],
        url="https://github.com/allure-framework/allure-python",
        author="Sergey Khomutinin",
        author_email="skhomuti@gmail.com",
        long_description=get_readme('README.rst'),
        classifiers=classifiers,
    )
