from pluggy import HookspecMarker, HookimplMarker

hookspec = HookspecMarker("allure")
hookimpl = HookimplMarker("allure")


@hookspec
def decorate_as_label(label_type, labels):
    """ label """


@hookspec
def add_label(label_type, labels):
    """ label """


@hookspec
def decorate_as_link(url, link_type, name):
    """ url """


@hookspec
def add_link(url, link_type, name):
    """ url """


@hookspec
def start_step(uuid, title, params):
    """ step """


@hookspec
def stop_step(uuid, exc_type, exc_val, exc_tb):
    """ step """


@hookspec
def attach_data(body, name, attachment_type, extension):
    """ attach data """


@hookspec
def attach_file(source, name, attachment_type, extension):
    """ attach file """


@hookspec
def start_fixture(parent_uuid, uuid, name):
    """ start fixture"""


@hookspec
def stop_fixture(uuid, exc_type, exc_val, exc_tb):
    """ stop fixture """
