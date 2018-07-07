
def pytest_ignore_collect(path, config):
    return config.pluginmanager.hasplugin('xdist')
