import allure_commons
from allure_commons.utils import uuid4


class AllureListener(object):
    def __init__(self, logger):
        self.logger = logger

    @allure_commons.hookimpl
    def decorate_as_label(self, label_type, labels):
        def deco(func):
            def wrapper(*args, **kwargs):
                self.add_label(label_type, labels)
                func(*args, **kwargs)
            return wrapper
        return deco

    @allure_commons.hookimpl
    def add_label(self, label_type, labels):
        with self.lifecycle.update_test_case() as case:
            for label in labels if case else ():
                case.labels.append(Label(label_type, label))

    @allure_commons.hookimpl
    def attach_data(self, body, name, attachment_type, extension):
        self.logger.attach_data(uuid4(), body, name=name, attachment_type=attachment_type, extension=extension)

    @allure_commons.hookimpl
    def attach_file(self, source, name, attachment_type, extension):
        self.logger.attach_file(uuid4(), source, name=name, attachment_type=attachment_type, extension=extension)
