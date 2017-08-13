from setuptools import setup

setup(
    name='allure-nose',
    version='2.1.0b1',
    description='Nose plugin for Allure framework',
    #long_description=open('README.rst').read(),
    author='Borisov Egor',
    author_email='ehborisov@gmail.com',
    packages=["allure_nose"],
    package_dir={"allure_nose": 'src'},
    url="https://github.com/allure-framework/allure-python2",
    install_requires=[
        'nose',
        'unittest2',
        'allure-pytest==2.1.0b1',
        'allure-python-commons==2.1.0b1'
    ],
    entry_points={
        'nose.plugins.0.10': [
            'allure = allure_nose:Allure'
        ]
    }
)
