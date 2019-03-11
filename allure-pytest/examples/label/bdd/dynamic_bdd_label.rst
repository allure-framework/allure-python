Dynamic BDD labels
------------------

    >>> import allure
    >>> import pytest

    >>> @allure.feature('first feature')
    ... def test_dynamic_feature():
    ...     allure.dynamic.feature('second feature')

    >>> @pytest.mark.parametrize('feature', ['first feature', 'second feature'])
    ... def test_parametrized_dynamic_feature(feature):
    ...     allure.dynamic.feature(feature)
