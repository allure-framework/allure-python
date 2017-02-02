import pytest


@pytest.hookspec
def pytest_allure_before_step(uuid, title, params):
    """ called before allure step """


@pytest.hookspec
def pytest_allure_after_step(uuid, title, exc_type, exc_val, exc_tb):
    """ called after allure step """


@pytest.hookspec
def pytest_allure_before_finalizer(parent_uuid, uuid, name):
    """ called before finalizer """


@pytest.hookspec
def pytest_allure_after_finalizer(uuid, exc_type, exc_val, exc_tb):
    """ called after finalizer """


@pytest.hookspec
def pytest_allure_attach(name, source, mime_type, extension):
    """ called for attach something to report """
