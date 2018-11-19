from setuptools import setup

PACKAGE = "allure-python-commons"
VERSION = "2.5.4"

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Software Development :: Quality Assurance',
    'Topic :: Software Development :: Testing',
]

install_requires = [
    "attrs>=16.0.0",
    "six>=1.9.0",
    "pluggy>=0.4.0",
    "enum34;python_version<'3.4'",
]


def main():
    setup(
        name=PACKAGE,
        version=VERSION,
        description="Common module for integrate allure with python-based frameworks",
        url="https://github.com/allure-framework/allure-python",
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
