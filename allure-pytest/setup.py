from setuptools import setup

PACKAGE = "pytest-allure-adaptor"
VERSION = "2.0.3"

install_requires = [
    "pytest>=2.7.3",
    "allure-python-commons==2.0.3"
]

def main():
    setup(
        name=PACKAGE,
        version=VERSION,
        packages=['allure'],
        package_dir={'allure': 'src/allure'},
        entry_points={'pytest11': ['allure_adaptor = allure.pytest_plugin']},
        install_requires=install_requires
    )

if __name__ == '__main__':
    main()

