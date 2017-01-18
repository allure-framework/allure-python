from setuptools import setup

PACKAGE = "pytest-allure-adaptor"
VERSION = "2.0.0"

install_requires = [
]

def main():
    setup(
        name=PACKAGE,
        version=VERSION,
        packages=['allure'],
        package_dir={'allure': 'src'},
        entry_points={'pytest11': ['allure_adaptor = allure.pytest_plugin']},
        install_requires=install_requires
    )

if __name__ == '__main__':
    main()

