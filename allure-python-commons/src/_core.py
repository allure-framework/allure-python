import threading
from pluggy import PluginManager
from allure_commons import _hooks


_storage = threading.local()
_storage.plugin_manager = PluginManager('allure')
_storage.plugin_manager.add_hookspecs(_hooks)

plugin_manager = _storage.plugin_manager
register = plugin_manager.register
