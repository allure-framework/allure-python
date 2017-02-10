
def pytest_generate_tests(metafunc):

    if 'metafunc_param' in metafunc.fixturenames:
        metafunc.parametrize("metafunc_param", [True])
    elif 'metafunc_param_with_ids' in metafunc.fixturenames:
        metafunc.parametrize("metafunc_param_with_ids", [True], ids=['metafunc_param_id'])

