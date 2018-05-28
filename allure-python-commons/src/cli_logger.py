# -*- coding: utf-8 -*-
import logging
import allure_commons


class AllureLoggingHandler(logging.Handler):
    def emit(self, record):
        allure_commons.log("[Log]   {} ({}, {})".format(record.getMessage(), record.levelname, record.name))
