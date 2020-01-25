from setuptools import setup

PACKAGE = "allure-python-commons-test"

install_requires = [
    "pyhamcrest>=1.9.0",
    "six>=1.9.0"
]


def main():
    setup(
        name=PACKAGE,
        use_scm_version={"root": "..", "relative_to": __file__},
        setup_requires=['setuptools_scm'],
        description="Common module for self-testing allure integrations with python-based frameworks",
        url="https://github.com/allure-framework/allure-python",
        author="QAMetaSoftware, Stanislav Seliverstov",
        author_email="sseliverstov@qameta.io",
        license="Apache-2.0",
        packages=["allure_commons_test"],
        package_dir={"allure_commons_test": "src"},
        install_requires=install_requires
    )

if __name__ == '__main__':
    main()
