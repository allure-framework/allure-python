Dynamic BDD labels
------------------

    >>> import allure
    >>> import pytest

    >>> @allure.feature('first feature')
    ... @allure.epic('first epic')
    ... @allure.story('first story')
    ... def test_dynamic_labels():
    ...     allure.dynamic.feature('second feature')
    ...     allure.dynamic.epic('second epic')
    ...     allure.dynamic.story('second story')

    >>> @pytest.mark.parametrize('feature, epic, story', [('first feature', 'first epic', 'first story'),
    ...                                                   ('second feature', 'second epic', 'second story')])
    ... def test_parametrized_dynamic_labels(feature, epic, story):
    ...     allure.dynamic.feature(feature)
    ...     allure.dynamic.epic(epic)
    ...     allure.dynamic.story(story)

    >>> def test_multiple_dynamic_labels():
    ...     allure.dynamic.feature('first feature', 'second feature')
    ...     allure.dynamic.epic('first epic', 'second epic')
    ...     allure.dynamic.story('first story', 'second story')
