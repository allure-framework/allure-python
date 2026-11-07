collect_ignore_glob = []

def pytest_configure(config):
    # Disable the outer playwright plugin to avoid _soft_errors global leaking
    # into nested in-process pytester runs.
    config.pluginmanager.set_blocked("playwright")

