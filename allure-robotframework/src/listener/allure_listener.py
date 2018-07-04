import allure_commons
from allure_commons.utils import uuid4


class AllureListener(object):
    def __init__(self, logger):
        self.logger = logger

    @allure_commons.hookimpl
    def attach_data(self, body, name, attachment_type, extension):
        self.logger.attach_data(uuid4(), body, name=name, attachment_type=attachment_type, extension=extension)

    @allure_commons.hookimpl
    def attach_file(self, source, name, attachment_type, extension):
        self.logger.attach_file(uuid4(), source, name=name, attachment_type=attachment_type, extension=extension)
